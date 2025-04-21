from flask import Blueprint, render_template, request, redirect, url_for, jsonify,session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .database import db
from .models import User,Cattle,FeedRecord,PredictionRecord
import joblib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

auth = Blueprint('auth', __name__)

# Route for rendering the signup page
@auth.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

# API route for user registration (handles form submission via fetch)
@auth.route('/signup', methods=['POST'])
def signup_api():
    print(" Received request at /signup")  # Debugging

    try:
        data = request.get_json()  # Correct way to handle JSON input
        print(" Received data:", data)  # Debugging

        if not data:
            return jsonify({"success": False, "message": "No data received!"}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        contact=data.get('contact')
        location=data.get('location')
        size=data.get('size')


        if not username or not email or not password:
            return jsonify({"success": False, "message": "Missing fields!"}), 400

        # Save to database
        new_user = User(username=username, email=email, password=password, contact=contact, location=location, size=size)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "message": "Signup successful!"})

    except Exception as e:
        print("ERROR:", str(e))  # Debugging
        return jsonify({"success": False, "message": "Server error!"}), 500

# API route to fetch users
@auth.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found!"}), 404

    user_list = [{"id": user.id, "username": user.username, "email": user.email ,"password": user.password, "contact": user.contact} for user in users]
    return jsonify(user_list), 200



# Render the login page
@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Handle login authentication
@auth.route('/logging', methods=['POST'])
def login_api():
    try:
        data = request.get_json()
        email_or_username = data.get('email')
        password = data.get('password')

        

        # Check if user exists (by email or username)
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        #  Compare passwords directly (Plain Text)
        if not user or user.password != password:
            return jsonify({"success": False, "message": "Invalid credentials!"}), 401
        session["user_email"] = user.email
        print(session["user_email"])
        return jsonify({"success": True, "message": "Login successful!"})

    except Exception as e:
        print(" ERROR:", str(e))
        return jsonify({"success": False, "message": "Server error!"}), 500
    

@auth.route('/delete')
def home():
    return render_template('delete.html')

@auth.route('/delete', methods=['DELETE'])
def delete_user():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"success": False, "message": "Email is required!"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"success": False, "message": "User not found!"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"success": True, "message": f"User {email} deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error!", "error": str(e)}), 500
    








@auth.route('/deletecattle')
def cat():
    return render_template('deletecattle.html')

@auth.route('/deletecattle', methods=['DELETE'])
def delete_cattle():
    try:
        data = request.get_json()
        cattleid = data.get('cattleid')

        if not cattleid:
            return jsonify({"success": False, "message": "cattleid is required!"}), 400

        
        cattle_to_delete = Cattle.query.filter_by(cattle_id=cattleid).first()

        if not cattle_to_delete:
            return jsonify({"success": False, "message": "Cattle not found!"}), 404

        db.session.delete(cattle_to_delete)
        db.session.commit()

        return jsonify({"success": True, "message": f"Cattle {cattleid} deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error!", "error": str(e)}), 500





    
@auth.route('/cattleupdate')
def cattle_update():
    return render_template('cattle_update.html')


@auth.route('/cattle')
def cattle_data():
    return render_template('cattle_data.html')


@auth.route('/cattleupdate', methods=['POST'])
def submit_cattle():
    data = request.get_json()
    email=session.get("user_email")

    if not data:
        return jsonify({"success": False, "message": "No data received!"}), 400

    print("Received Data:", data)  # Debugging

    # # Check if required fields exist
    # required_fields = ["cattleId", "breed", "gender", "lifeStage", "age", "weight", "feedIntake"]
    # for field in required_fields:
    #     if field not in data or data[field] == "":
    #         return jsonify({"success": False, "message": f"Missing field: {field}"}), 400

    try:
        # Convert birth_date from string to Python date object
        # birth_date = None
        # if data.get('birthDate'):
        #     birth_date = datetime.strptime(data['birthDate'], "%Y-%m-%d").date()

        new_cattle = Cattle(
            cattle_id=data['cattleId'],
            name=data.get('name', None),
            email=email,
            breed=data['breed'],
            type=data['type'],
            life_stage=data['lifeStage'],
            age=int(data['age']),
            #birth_date=birth_date,
            weight=float(data['weight']),
            #height=float(data.get('height', 0)),  # Handle None case
            feed_intake=float(data['feedIntake']),
            feed_type=data.get('feedType', None),
            health=data.get('health', None),
            #notes=data.get('notes', None)
        )

        db.session.add(new_cattle)
        db.session.commit()
        print("Cattle successfully added to DB!")  # Debugging
        return jsonify({'message': 'Cattle details saved successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))  # Debugging
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500




@auth.route('/cattledb', methods=['GET'])
def get_cattledb():
    cattle_list = Cattle.query.all()
    return jsonify([{
            "id": c.cattle_id,
            "name": c.name,
            "breed": c.breed,
            "age": c.age,
            "weight": c.weight,
            "feed_intake":c.feed_intake,
            "health":c.health
    } for c in cattle_list])


@auth.route('/get_user', methods=['GET'])
def get_user():
    email=session.get("user_email")
    print(email)

    user = User.query.filter_by(email=email).first()

    if user:
            print(user.email,"",user.id)
            return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "contact": user.contact,
            "location": user.location,
            "size": user.size
            })
    else:
        return jsonify({"error": "User not found"}), 404

@auth.route('/get_cattle', methods=['GET'])
def get_cattle():
    email=session.get("user_email")

    cattle=Cattle.query.filter_by(email=email).all()
    cows = Cattle.query.filter(Cattle.email == email, Cattle.type == "cow").count()
    goat = Cattle.query.filter(Cattle.email == email, Cattle.type == "goat").count()
    buffalo = Cattle.query.filter(Cattle.email == email, Cattle.type == "buffalo").count()

    print('cow',cows,"    ",buffalo,"    ",goat)


    if cattle:
        cattle_data = [{
            "id": c.id,
            "name": c.name,
            "breed": c.breed,
            "age": c.age,
            "type":c.type,
            "weight": c.weight,
            "feed_intake":c.feed_intake,
            "health":c.health
        } for c in cattle]

        return jsonify({"status": "success", "cattle": cattle_data, "cows": cows, "buffalo": buffalo, "goat":goat})
    else:
        return jsonify({"status": "empty", "cattle": []})


@auth.route('/verthe')
def verthe():
    return render_template('vertheoruPage.html')





@auth.route('/pform')
def predict_form():
    return render_template('predict_form.html')

@auth.route('/pmarket', methods=['POST'])
def predict_market():
    weight = float(request.form['weight'])
    age = int(request.form['age'])
    milk_yield = float(request.form['milk_yield'])
    feed_type = request.form['feed_type']

    feed_map = {'dry': 0, 'green': 1, 'mixed': 2}
    feed_encoded = feed_map.get(feed_type, 0)
    X_input = [[weight, age, milk_yield, feed_encoded,0,0]]

    # Load models
    classifier = joblib.load('models/market_classifier.pkl')
    regressor = joblib.load('models/days_regressor.pkl')

    market_ready = "Yes" if classifier.predict(X_input)[0] == 1 else "No"
    days_predicted = int(regressor.predict(X_input)[0])

    prediction = PredictionRecord(
        weight=weight,
        age=age,
        milk_yield=milk_yield,
        bcs=0,  # Optional: add field to form and use it
        market_ready=market_ready,
        predicted_days=days_predicted
    )
    db.session.add(prediction)
    db.session.commit()

    return render_template('predict_result.html',
                           weight=weight,
                           age=age,
                           milk_yield=milk_yield,
                           feed_type=feed_type,
                           market_ready=market_ready,
                           days_to_ready=days_predicted)


@auth.route('/viewrecord')
def viewrec():
    viewreco = FeedRecord.query.all()
    if not viewreco:
        return jsonify({"message": "No viewreco found!"}), 404

    user_list = [{"id": i.id, "weight": i.weight, "milk_yield": i.milk_yield} for i in viewreco]
    return jsonify(user_list), 200



@auth.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        # Collect form inputs
        cow_type = request.form['cow_type']
        weight = float(request.form['weight'])
        milk_yield = float(request.form['milk_yield'])
        lactation_stage = request.form['lactation_stage']
        age = int(request.form['age'])
        
        # Optional inputs
        current_dry = float(request.form['current_dry']) if request.form.get('current_dry') else 0
        current_green = float(request.form['current_green']) if request.form.get('current_green') else 0
        current_concentrate = float(request.form['current_concentrate']) if request.form.get('current_concentrate') else 0
        
        cost_dry = float(request.form['cost_dry']) if request.form.get('cost_dry') else 0
        cost_green = float(request.form['cost_green']) if request.form.get('cost_green') else 0
        cost_concentrate = float(request.form['cost_concentrate']) if request.form.get('cost_concentrate') else 0

        # Feed requirement logic
        total_feed = round(weight * 0.025 + milk_yield * 0.4, 2)
        dry = round(weight * 0.01, 2)
        green = round(weight * 0.03, 2)
        concentrate = round(milk_yield * 0.4, 2)

        # Feed gap
        current_total_feed = current_dry + current_green + current_concentrate
        feed_gap = round(total_feed - current_total_feed, 2)

        # Ideal cost
        ideal_cost = round(dry * cost_dry + green * cost_green + concentrate * cost_concentrate, 2)

        # Current cost (user-inputted current feed and prices)
        current_cost = round(current_dry * cost_dry + current_green * cost_green + current_concentrate * cost_concentrate, 2)

        #original feed:

        previous_feed=round(total_feed-feed_gap)
        # Suggestions
        suggestions = []
        if feed_gap > 0:
            suggestions.append(f"Increase total feed by {feed_gap} kg/day.")
        if current_cost > ideal_cost:
            suggestions.append("Current feeding is more expensive than optimized. Consider adjusting feed mix.")
        if current_cost < ideal_cost:
            suggestions.append("Current cost is lower than ideal – check if nutrient requirements are met.")
        if not suggestions:
            suggestions.append("Feeding strategy looks optimal.")

        # Save to database
        optimized_feed_str = f"Dry: {dry} kg, Green: {green} kg, Concentrate: {concentrate} kg"
        result = FeedRecord(
            # user_id=current_user.id,
            email=session.get("user_email"),
            cow_type=cow_type,
            weight=weight,
            milk_yield=milk_yield,
            feed_type='green',
            optimized_feed=optimized_feed_str,
            total_cost=current_cost,
            dmi_gap=feed_gap
        )
        db.session.add(result)
        db.session.commit()

        return render_template('feedresult.html',
                               cow_type=cow_type,
                               weight=weight,
                               age=age,
                               milk_yield=milk_yield,
                               lactation_stage=lactation_stage,
                               total_feed=total_feed,
                               dry=dry,
                               green=green,
                               concentrate=concentrate,
                               previous_feed=previous_feed,
                               feed_gap=feed_gap,
                               ideal_cost=ideal_cost,
                               current_cost=current_cost,
                               suggestions=suggestions)

    return render_template('feedform.html')


@auth.route("/dashboard", methods=['GET'])
def dashboard():
    if request.args.get('json') == 'true':
        email = session.get("user_email")
        print("hiii     iiih", session.get("user_email"))

        if not email:
            return jsonify({"status": "error", "message": "Not logged in"}), 401

        feed = FeedRecord.query.filter_by(email=email).order_by(FeedRecord.timestamp.desc()).all()

        if feed:
            feed_data = [{
                "timestamp": record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "cow_type": record.cow_type,
                "weight": record.weight,
                "milk_yield": record.milk_yield,
                "cost": record.total_cost
            } for record in feed]

            print(feed_data)
            return jsonify({"status": "success", "feedrecord": feed_data})
        else:
            return jsonify({"status": "success", "feedrecord": []})
    
    # Default: render the dashboard page
    return render_template('dash.html')
