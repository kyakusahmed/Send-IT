from flask import Flask, jsonify, request, render_template
from flasgger import Swagger, swag_from
from re import match
import datetime
from .models.parcel import User



from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity,jwt_optional)

app2 = Flask(__name__)
Swagger(app2)
user = User()
jwt = JWTManager(app2)
app2.config['JWT_SECRET_KEY'] = 'super-secret'


@app2.route('/user/login', methods=['GET'])
def user_login():
    """Render user login page"""
    return render_template('index.html')

@app2.route('/user/register', methods=['GET'])
def user_register():
    """Render user register page."""
    return render_template('SignUp.html')

@app2.route('/user/status', methods=['GET'])
def user_change_status():
    """Render admin orders page."""
    return render_template('orders.html')

# @app2.route('/admin/menus', methods=['GET'])
# def admin_get_all_menus_page():
#     """Render admin menus page."""
#     return render_template('admin/menus/index.html')

# @app.route('/admin/menus/create', methods=['GET'])
# def admin_add_menu_page():
#     """Render admin add menu page."""
#     return render_template('admin/menus/create.html')

# @app.route('/admin/menus/<int:menu_id>/edit', methods=['GET'])
# def admin_edit_specific_menu_page(menu_id):
#     """Render admin edit a menu page."""
#     return render_template('admin/menus/edit.html', menu_id=menu_id)

# @app.route('/admin/menus/<int:menu_id>', methods=['GET'])
# def admin_get_specific_menu_page(menu_id):
#     """Render admin get a menu page."""
#     return render_template('admin/menus/show.html', menu_id=menu_id)

# @app.route('/admin/orders/history', methods=['GET'])
# def admin_get_menu_history_page():
#     """Render admin get menu history page."""
#     return render_template('admin/history.html')

# @app.route('/user/orders/history', methods=['GET'])
# def user_get_order_history_page():
#     """Render user order history page."""
#     return render_template('history.html')






@app2.route('/api/v1/parcels/<int:parcel_id>', methods=["PUT"])
@jwt_required
def admin_update_status(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"message":"unauthorised access"}), 401
    
    parcel = user.find_parcel(parcel_id)
    if not parcel:
        return jsonify({"message" : "parcel not found"}), 404 
    if parcel[11]== "delivered":
        return jsonify({"message": 'parcel already delivered'}), 200      
    else:
        data = request.get_json()
        status = data['status']
        status_list = ["cancelled", "delivered", "accepted"]
        if not status in status_list:
            return jsonify({"message":"status doesnot exist, use cancelled, delivered or accepted"})

        if not data.get("status"):
            return jsonify({"error" : "status is required"}), 406
        return jsonify({"parcel" : user.update_status(parcel_id, data["status"])}), 200

@app2.route('/api/v1/parcels/<int:parcel_id>/location', methods=["PUT"])
@jwt_required
def update_current_location(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"message":"unauthorised access"}), 401
    else:
        parcel = user.find_parcel(parcel_id)
        if not parcel:
            return jsonify({"message" : "parcel not found"}), 404
        else:
            get_input = request.get_json()
            if not get_input.get("current_location"):
                return jsonify({"error" : "current_location is required"}), 406
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
                    'recepient_country':parcels[7],
                    'destination':parcels[8],
                    'weight':parcels[key][9],
                    'price':parcels[key][10],
                    'status':parcels[key][11],
                    'current_location':parcels[key][12],
                    'created_at':parcels[key][13]
                })
        return jsonify({"parcels": new_list}), 200

@app2.route('/api/v1/users/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user_to_admin(user_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"message":"unauthorised access"}), 401
    get_user = user.get_user_by_ID(user_id)
    if not get_user:
        return jsonify(message="User Not Found"), 404
    else:
        get_input = request.get_json()
        role = get_input.get('role')
        roles = ["user","admin"]
        if not role in roles:
            return jsonify(message="role doesnt exist"), 406
        if not role:
            return jsonify(message="Role is required"), 406
        else:
            user.update_user_to_admin(get_user[0], role)
            return jsonify(message = "User role updated successfuly"), 200


@app2.route('/api/v1/users/register', methods=['POST'])
@swag_from("docs/signup.yaml")
def register_user():
    # data = request.get_json()
    # required = ('first_name', 'last_name', 'email', 'password')
    # if not set(required).issubset(set(data)):
    #     return jsonify({"error": "some fields are missing"}), 400
    data = request.get_json()
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    if not email:
        return jsonify({"message": "Missing email parameter"}), 406
    if not password:
        return jsonify({"message": "Missing password parameter"}), 406
    if not first_name:
        return jsonify({"message": "Missing first_name parameter"}), 406    
    if not last_name:
        return jsonify({"message": "Missing last_name parameter"}), 406    
    if not bool(
            match(
                r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                data["email"])):
        return jsonify({"message":"invalid email"}), 406

    if len(data["password"].strip()) < 5:
        return jsonify({"error":"passowrd is too short"}), 406

    new_user = ('first_name', 'last_name', 'email', 'password')
    resp = user.add_user(new_user)
    registered = user.get_user_by_email(data['email'])
    if registered:
        return jsonify({"message": "user registered already"}), 201
    else:
        return jsonify({"status": user.register_user(
            data["first_name"].strip(),
            data["last_name"].strip(),
            data["email"].strip(),
            data["password"].strip(),
            "user"
            )}), 201


@app2.route('/api/v1/users/login', methods=['POST'])
@swag_from("docs/login.yaml")
def login():
    data = request.get_json()
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"message": "Missing email parameter"}), 406
    if not password:
        return jsonify({"message": "Missing password parameter"}), 406
    
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

            
@app2.route('/api/v1/parcels/<int:parcel_id>/destination', methods=["PUT"])
@jwt_required
def update_destination(parcel_id):
    get_input = request.get_json()
    if not get_input.get("destination"):
        return jsonify({"error" : "destination is required"}), 406
    return jsonify({"parcel" : user.update_parcel_destination(parcel_id, get_input["destination"])}), 200
   
@app2.route('/api/v1/parcels/users/<int:user_id>', methods=['GET'])
@jwt_required
@swag_from('docs/get_parcels_by_user.yaml')
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
                'recepient_country':parcels[key][7],
                'destination':parcels[key][8],
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
        return jsonify({"error": "missing fields"}), 406
    else:
        return jsonify({"message": user.place_parcel_delivery_order(
            current_user[0],
            data["sender_name"].strip(),
            data["sender_phone"].strip(),
            data["pickup_location"].strip(),
            data["recepient_name"].strip(),
            data["recepient_phone"].strip(),
            data["recepient_country"].strip(),
            data["destination"].strip(),
            data["weight"],
            50,
            "pending"
            )}), 201     



@app2.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
@jwt_required
@swag_from('docs/get_one_parcel.yaml')
def get_parcel(parcel_id):
    parcels2 = user.find_parcel(parcel_id)
    print(parcels2)
    if not parcels2:
        return jsonify({"status": 'parcel not found'}), 404
    parcels = user.find_parcel(parcel_id)
    return jsonify({"parcel": { 'parcel_id':parcels[0],
                                'user_id':parcels[1],
                                'sender_name':parcels[2],
                                'sender_phone':parcels[3],
                                'pickup_location':parcels[4],
                                'recepient_name':parcels[5],
                                'recepient_phone':parcels[6], 
                                'recepient_country':parcels[7],
                                'destination':parcels[8],
                                'weight':parcels[9],
                                'price':parcels[10],
                                'status':parcels[11],
                                'current_location':parcels[12],
                                'created_at':parcels[13]
                            }}), 200

  

@app2.route('/api/v1/parcel/<int:parcel_id>/user', methods=['PUT'])
@jwt_required
def user_update_status(parcel_id):
    data = request.get_json()
    parcel2 = user.find_parcel(parcel_id)
    required = ('status')
    if not required:
        return jsonify({"message": "status missing"}), 406
    if not parcel2:
        return jsonify({"message": 'parcel not found'}), 404
    status = data['status']
    status_list = ["cancelled"]
    if not status in status_list:
        return jsonify({"message":"status doesnot exist, use cancelled or delivered"}), 406
    else:
        if parcel2[11]== "delivered":
            return jsonify({"message": 'parcel already delivered'}), 200   
        return jsonify({"parcel" : user.update_status(parcel2[0], data["status"])}), 200           
                                