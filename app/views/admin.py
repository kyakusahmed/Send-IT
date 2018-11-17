from flask import Flask, jsonify, request
from app.models.user import User
from re import match
import datetime

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity,jwt_optional)

app2 = Flask(__name__)
user = User()
jwt = JWTManager(app2)
app2.config['JWT_SECRET_KEY'] = 'super-secret'

@app2.route('/api/v1/parcels/<int:parcel_id>/status', methods=["PUT"])
@jwt_required
def update_destination(parcel_id):
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
        return jsonify({"parcel" : user.update_status(parcel_id, get_input["status"])}), 200