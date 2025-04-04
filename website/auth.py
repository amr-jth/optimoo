from flask import Blueprint, render_template, request, redirect, url_for, jsonify,session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .database import db
from .models import User,Cattle
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
    return render_template('cattkle_data.html')


@auth.route('/cattleupdate', methods=['POST'])
def submit_cattle():
    data = request.get_json()

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
            #photo=data.get('photo', None),
            breed=data['breed'],
            #gender=data['gender'],
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
def get_cattle():
    cattle_list = Cattle.query.all()
    return jsonify([{
        'cattleId': c.cattle_id,
        'name': c.name,
        'breed': c.breed,
        'weight': c.weight
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
