from flask import Flask, jsonify, request
from app.models.user import User
from re import match
import datetime

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity,jwt_optional)

app2 = Flask(__name__)
user = User()
jwt = JWTManager(app2)
app2.config['JWT_SECRET_KEY'] = 'super-secret'

@app2.route('/api/v1/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    required = ('first_name', 'last_name', 'email', 'password')
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

    new_user = ('first_name', 'last_name', 'email', 'password', 'role')
    resp = User().add_user(new_user)
    if resp == "failed":
        return jsonify({"message": "failed"}), 400
    elif resp == "user exists":
        return jsonify({"message": "email registered alreADY"}), 400
    else:
        return jsonify({"msg": user.register_user(
            data["first_name"].strip(),
            data["last_name"].strip(),
            data["email"].strip(),
            data["password"].strip(),
            "user"
            )}), 201


@app2.route('/api/v1/users/login', methods=['POST'])
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

    check_user = User().user_signin(email, password)
    if not check_user:
        return jsonify({"msg":"register first"}), 406

    access_token = create_access_token(identity=check_user)
    return jsonify(access_token=access_token, msg="Login successful"), 200

            
@app2.route('/api/v1/parcels/<int:parcel_id>', methods=["PUT"])
@jwt_required
def update_destination(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "user":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        get_input = request.get_json()
        if not get_input.get("destination").strip():
            return jsonify({"error" : "destination is required"}), 400
        return jsonify({"parcel" : user.update_order_destination(parcel_id, get_input["destination"])}), 200





@app2.route('/api/v1/parcels/<int:parcel_id>/status', methods=["PUT"])
@jwt_required
def update_status(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        parcel_status = data['status']
        parcels_status = ['delivered', 'cancelled']
        if parcel_status not in parcels_status:
            return jsonify({"error": " status {} doesnot exist".format(status)}), 200

        get_input = request.get_json()
        if not get_input.get("status").strip():
            return jsonify({"error" : "status is required"}), 400
        return jsonify({"parcel" : user.update_status(parcel_id, get_input["status"])}), 20

@app2.route('/api/v1/admins/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    if not data.get("first_name"):
            return jsonify({"error": "first_name is required"}), 200
    elif not data.get("last_name"):
        return jsonify({"error": "last_name is required"}), 200
    elif not data.get('email'):
        return jsonify({"error": "email is required"}), 200
    elif not data.get('password'):
        return jsonify({"error":"password is required"})

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

    new_user = ("first_name", 'last_name' , 'email', 'password', 'role')
    resp = User().add_user(new_user)
    if resp == "failed":
        return jsonify({"message": "failed"}), 400
    elif resp == "user exists":
        return jsonify({"message": "email is already being used"}), 400
    else:
        return jsonify({"msg": user.register_user(
            data["first_name"],
            data["last_name"],
            data["email"],
            data["password"],
            "admin"
            )}), 201
        

@app2.route('/api/v1/admins/login', methods=['POST'])
def admin_login():
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

    check_user = user.admin_signin(email, password)
    if not check_user:
        return jsonify({"msg":"register first"}), 406

    access_token = create_access_token(identity=check_user)
    return jsonify(access_token=access_token, msg="Login successful"), 200
   
@app2.route('/api/v1/parcels/users/<int:user_id>', methods=['GET'])
def view_user_parcels_history(user_id):
    user_parcels = user.view_parcel_history(user_id)
    return jsonify({'parcels': user_parcels})

  
@app2.route('/api/v1/parcels/admin', methods=['GET'])
def get_all_parcels():
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        return jsonify({'parcels': parcel.get_all_parcels()}), 200

@app2.route('/api/v1/parcels', methods=['POST])
def user_place_order():
    current_user = get_jwt_identity()
    if current_user[5] != "user":
        return jsonify({"msg":"unauthorised access"}), 401
    else:

        data = request.get_json()
        required = (user_id, sender_name, sender_phone, pickup_location, recepient_name, recepient_phone, 
        recepient_country, destination, weight, price, status, created_at)
        if not set(required).issubset(set(data)):
            return jsonify({"error": "missing fields"}), 200
        else:
            return jsonify({"parcels": user.place_parcel_delivery_order(
                data["user_id"].strip(),
                data["sender_name"].strip(),
                data["sender_phone"].strip(),
                data["pickup_location"].strip(),
                data["recepient_name"].strip(),
                data["recepient_phone"].strip(),
                data["recepient_country"].strip(),
                data["destination"].strip(),
                data["weight"].strip()
                data["price"].strip()
                data["status"].strip()
                datetime.datetime.now()
                )}), 201        
                                        
@app2.route('/api/v1/parcels/<int:parcel_id>/current_location', methods=["PUT"])
@jwt_required
def update_curremt_location(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        get_input = request.get_json()
        if not get_input.get("current_location").strip():
            return jsonify({"error" : "current_location is required"}), 400
        return jsonify({"parcel" : user.current_location(parcel_id, get_input["current_location"])}), 200                                        
                                        
              
