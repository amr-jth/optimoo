from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .database import db
from .models import User,Cattle

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

        if not username or not email or not password:
            return jsonify({"success": False, "message": "Missing fields!"}), 400

        # Save to database
        new_user = User(username=username, email=email, password=password)
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

    user_list = [{"id": user.id, "username": user.username, "email": user.email ,"password": user.password} for user in users]
    return jsonify(user_list), 200



# Render the login page
@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Handle login authentication
@auth.route('/login', methods=['POST'])
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
    
@auth.route('/cattleupdate')
def cattle_update():
    return render_template('cattle_update.html')


@auth.route('/cattle')
def cattle_data():
    return render_template('cattkle_data.html')



@auth.route('/cattleupdate', methods=['POST'])
def submit_cattle():
    data = request.get_json()  # Get JSON data from frontend

    if not data:
        return jsonify({"success": False, "message": "No data received!"}), 400
    
    new_cattle = Cattle(
        cattle_id=data['cattleId'],
        name=data.get('name', None),
        #photo=data.get('photo', None),
        breed=data['breed'],
        #gender=data['gender'],
        life_stage=data['lifeStage'],
        age=data['age'],
        #birth_date=data.get('birthDate', None),
        weight=data['weight'],
        #height=data.get('height', None),
        feed_intake=data['feedIntake'],
        feed_type=data.get('feedType', None),
        health=data.get('health', None),
        #notes=data.get('notes', None)
    )

    db.session.add(new_cattle)
    db.session.commit()

    return jsonify({'message': 'Cattle details saved successfully!'}), 201




@auth.route('/cattledb', methods=['GET'])
def get_cattle():
    cattle_list = Cattle.query.all()
    return jsonify([{
        'cattleId': c.cattle_id,
        'name': c.name,
        'breed': c.breed,
        'gender': c.gender,
        'weight': c.weight
    } for c in cattle_list])
