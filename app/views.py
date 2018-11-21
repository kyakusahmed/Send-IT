from flask import Flask, jsonify, request
from re import match
import datetime
from .models.parcel import User


from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity,jwt_optional)

app2 = Flask(__name__)
# Swagger(app2)
user = User()
jwt = JWTManager(app2)
app2.config['JWT_SECRET_KEY'] = 'super-secret'

@app2.route('/api/v1/parcels/<int:parcel_id>', methods=["PUT"])
@jwt_required
def admin_update_status(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"message":"unauthorised access"}), 401
    else:
        parcel = user.find_parcel(parcel_id)
        if not parcel:
            return jsonify({"message" : "parcel not found"}), 400
        data = request.get_json()    
        status = data['status']
        status_list = ["delivered", "cancelled"]
        if not status in status_list:
            return jsonify({"message":"status doesnot exist, use cancelled or delivered"}) 
        if parcel[11]== "delivered":
            return jsonify({"message": 'parcel already delivered'}), 200      
        else:
            get_input = request.get_json()
            if not get_input.get("status"):
                return jsonify({"error" : "status is required"}), 400
            return jsonify({"parcel" : user.update_status(parcel_id, get_input["status"])}), 200

@app2.route('/api/v1/parcels/<int:parcel_id>', methods=["PUT"])
@jwt_required
def update_current_location(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"message":"unauthorised access"}), 401
    else:
        parcel = user.find_parcel(parcel_id)
        if not parcel:
            return jsonify({"message" : "parcel not found"}), 400
        else:
            get_input = request.get_json()
            if not get_input.get("current_location"):
                return jsonify({"error" : "current_location is required"}), 400
            return jsonify({"parcel" : user.update_current_location(parcel_id, get_input["current_location"])}), 200

@app2.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def get_all_parcels():
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"message":"unauthorised access"}), 401
    else:
        parcels = user.view_all_parcels()
        new_list = []
        for key in range(len(parcels)):
            new_list.append({   
                    'parcel_id':parcels[key][0],
                    'user_id':parcels[key][1],
                    'sender_name':parcels[key][2],
                    'sender_phone':parcels[key][3],
                    'pickup_location':parcels[key][4],
                    'recepient_name':parcels[key][5],
                    'recepient_phone':parcels[key][6],
                    'recepient_location':parcels[key][7],
                    'recepient_country':parcels[key][8],
                    'weight':parcels[key][9],
                    'price':parcels[key][10],
                    'status':parcels[key][11],
                    'current_location':parcels[key][12],
                    'created_at':parcels[key][13]
                })
        return jsonify({"parcels": new_list}), 200

@app2.route('/api/v1/parcels/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user_to_admin(user_id):
    get_user = user.get_user_by_ID(user_id)
    if not get_user:
        return jsonify(message="User Not Found"), 401
    else:
        get_input = request.get_json()
        role = get_input.get('role')
        if not role:
            return jsonify(message="Role is required"), 400
        else:
            user.update_user_to_admin(user_id, role)
            return jsonify(message = "User role updated successfuly"), 200


@app2.route('/api/v1/users/register', methods=['POST'])
# @swag_from("../docs/user/signup.yaml")
def register_user():
    data = request.get_json()
    required = ('first_name', 'last_name', 'email', 'password')
    if not set(required).issubset(set(data)):
        return jsonify({"error": "some fields are missing"}), 400
    if not bool(
            match(
                r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                data["email"])):
        return jsonify({"message":"invalid email"}), 406

    if len(data["password"].strip()) < 5:
        return jsonify({"error":"passowrd is too short"}), 406

    new_user = ('first_name', 'last_name', 'email', 'password', "")
    resp = User().add_user(new_user)
    registered = user.get_user_by_email(data['email'])
    if registered:
        return jsonify(message="User already registered.")
    if resp == "failed":
        return jsonify({"message": "failed"}), 400
    elif resp == "user exists":
        return jsonify({"message": "user registered already"}), 400
    else:
        return jsonify({"status": user.register_user(
            data["first_name"].strip(),
            data["last_name"].strip(),
            data["email"].strip(),
            data["password"].strip(),
            "user"
            )}), 201


@app2.route('/api/v1/users/login', methods=['POST'])
# @swag_from("../docs/user/login.yaml")
def login():
    data = request.get_json()
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"message": "Missing email parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400
    
    if not bool(
            match(
                r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                data["email"])):
        return jsonify({"message":"invalid email"}), 406

    if len(data["password"]) < 5:
        return jsonify({"message":"passowrd is too short"}), 406 

    check_user = User().user_signin(email, password)
    if not check_user:
        return jsonify({"message":"register first"}), 406

    access_token = create_access_token(identity=check_user)
    return jsonify({'message':"Login successful", 'access_token':access_token}), 200

            
@app2.route('/api/v1/parcels/<int:parcel_id>', methods=["PUT"])
@jwt_required
def update_destination(parcel_id):
    get_input = request.get_json()
    if not get_input.get("destination"):
        return jsonify({"error" : "destination is required"}), 400
    return jsonify({"parcel" : user.update_parcel_destination(parcel_id, get_input["destination"])}), 200
   
@app2.route('/api/v1/parcels/users/<int:user_id>', methods=['GET'])
@jwt_required
def view_user_parcels_history(user_id):
    parcels = user.view_parcel_history(user_id)
    new_list = []
    for key in range(len(parcels)):
        new_list.append({   
                'parcel_id':parcels[key][0],
                'user_id':parcels[key][1],
                'sender_name':parcels[key][2],
                'sender_phone':parcels[key][3],
                'pickup_location':parcels[key][4],
                'recepient_name':parcels[key][5],
                'recepient_phone':parcels[key][6],
                'recepient_location':parcels[key][7],
                'recepient_country':parcels[key][8],
                'weight':parcels[key][9],
                'price':parcels[key][10],
                'status':parcels[key][11],
                'current_location':parcels[key][12],
                'created_at':parcels[key][13]
            })
    return jsonify({"parcels": new_list}), 200

@app2.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def user_place_parcel():
    current_user = get_jwt_identity()
    data = request.get_json()
    required = ("sender_name", "sender_phone", "pickup_location", "recepient_name", "recepient_phone", 
    "recepient_country", "destination", "weight")
    if not set(required).issubset(set(data)):
        return jsonify({"error": "missing fields"}), 200    
    else:
        price = 0
        weight = data["weight"].strip()
        if weight < 1:
            price = 2000
        elif weight < 5:
            price = 5000
        elif weight <= 20:
            price = 10000
        else:
            weight <= 60
            price = 30000 
                      
        return jsonify({"status": user.place_parcel_delivery_order(
            current_user[0],
            data["sender_name"].strip(),
            data["sender_phone"].strip(),
            data["pickup_location"].strip(),
            data["recepient_name"].strip(),
            data["recepient_phone"].strip(),
            data["recepient_country"].strip(),
            data["destination"].strip(),
            data["weight"].strip(),
            price,
            "pending"
            )}), 201     



@app2.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
@jwt_required
def get_parcel(parcel_id):
    """get specific parcel."""
    parcel2 = user.find_parcel(parcel_id)
    if not parcel2:
        return jsonify({"status": 'parcel not found'}), 404
    return jsonify({"parcel": parcel2}), 200  

@app2.route('/api/v1/parcel/<int:parcel_id>', methods=['PUT'])
@jwt_required
def user_update_status(parcel_id):
    data = request.get_json()
    parcel2 = user.find_parcel(parcel_id)
    required = ('parcel_id','status')
    if not set(required).issubset(set(data)):
        return jsonify({"message": "status missing"}), 400
    if not parcel2:
        return jsonify({"message": 'parcel not found'}), 404
    status = data['status']
    status_list = ["cancelled"]
    if not status in status_list:
        return jsonify({"message":"status doesnot exist, use cancelled or delivered"})
    else:
        if parcel2[11]== "delivered":
            return jsonify({"message": 'parcel already delivered'}), 200   
        return jsonify({"parcel" : user.update_status(parcel_id, data["status"].lower)}), 200           
                                