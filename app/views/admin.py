from flask import Flask, jsonify, request
from app.models.admin import Admin
from re import match
import datetime


app2 = Flask(__name__)
user = User()
admin = Admin()

@app2.route('/api/v1/admin/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    required = ("first_name", "last_name", 'email', 'password', 'role')
    if not set(required).issubset(set(data)):
        return jsonify({"error": "some fields are missing"}), 200
    if not bool(
            match(
                r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                data["email"])):
        return jsonify({"msg":"invalid email"}), 406

    if len(data["password"].strip()) < 5:
        return jsonify({"msg":"passowrd is too short"}), 406
    
    user_role = data['role']
    user_roles = ['admin', 'user']
    if user_role not in user_roles:
        return jsonify({"error": " role {} doesnot exist".format(user_role)}), 200

    new_user = (first_name, last_name , email, password, role, "")
    resp = Admin().add_user(new_user)
        if response == "failed":
            return jsonify({"message": "failed"}), 400
        elif resp == "user exists":
            return jsonify({"message": "email is already being used"}), 400
        else:
            return jsonify({"msg": admin.register_admin(
                data["first_name"].strip(),
                data["last_name"].strip(),
                data["email"].strip(),
                data["password"].strip(),
                data["role"].strip()
                )}), 201
            

@app2.route('/api/v1/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    if not bool(
            match(
                r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                data["email"])):
        return jsonify({"msg":"invalid email"}), 406

    if len(data["password"]) < 5:
        return jsonify({"msg":"passowrd is too short"}), 406 

    check_user = user.login_user(email, password)
    if not check_user:
        return jsonify({"msg":"register first"}), 406

    access_token = create_access_token(identity=check_user)
    return jsonify(access_token=access_token, msg="Login successful"), 200
   