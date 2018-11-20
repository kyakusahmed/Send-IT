from flask import Flask, jsonify, request
from app.models.user import User
from re import match
import datetime
from app.views.user import app2

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity,jwt_optional)

user = User()
jwt = JWTManager(app2)
app2.config['JWT_SECRET_KEY'] = 'super-secret'


@app2.route('/api/v1/parcels/<int:parcel_id>/status', methods=["PUT"])
@jwt_required
def update_status(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        parcel = user.find_parcel(parcel_id)
        if not parcel:
            return jsonify({"msg" : "parcel not found"}), 400
        else:
            get_input = request.get_json()
            if not get_input.get("status"):
                return jsonify({"error" : "status is required"}), 400
            return jsonify({"parcel" : user.update_status(parcel_id, get_input["status"])}), 200

@app2.route('/api/v1/parcels/<int:parcel_id>/current_location', methods=["PUT"])
@jwt_required
def update_curremt_location(parcel_id):
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        parcel = user.find_parcel(parcel_id)
        if not parcel:
            return jsonify({"msg" : "parcel not found"}), 400
        else:
            get_input = request.get_json()
            if not get_input.get("current_location"):
                return jsonify({"error" : "current_location is required"}), 400
            return jsonify({"parcel" : user.update_current_location(parcel_id, get_input["current_location"])}), 200

@app2.route('/api/v1/parcels/admin', methods=['GET'])
@jwt_required
def get_all_parcels():
    current_user = get_jwt_identity()
    if current_user[5] != "admin":
        return jsonify({"msg":"unauthorised access"}), 401
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

@app2.route('/api/v1/users/roles/<int:user_id>', methods=['PUT'])
def update_user_to_admin(user_id):
    get_user = user.get_user_by_ID(user_id)
    if not get_user:
        return jsonify(msg="User Not Found"), 401
    else:
        get_input = request.get_json()
        role = get_input.get('role')
        if not role:
            return jsonify(msg="Role is required"), 400
        else:
            user.update_user_to_admin(user_id, role)
            return jsonify(massege = "User role updated successfuly"), 200
