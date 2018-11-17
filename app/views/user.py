from flask import Flask, jsonify, request
from app.models.user import User
from re import match
import datetime

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity,jwt_optional)

app2 = Flask(__name__)
user = User()
jwt = JWTManager(app2)
app2.config['JWT_SECRET_KEY'] = 'super-secret'

@app2.route('/api/v1/parcels/<int:parcel_id>/destination', methods=["PUT"])
@jwt_required
def update_destination(orders_id):
    current_user = get_jwt_identity()
    if current_user[5] != "user":
        return jsonify({"msg":"unauthorised access"}), 401
    else:
        get_input = request.get_json()
        if not get_input.get("destination").strip():
            return jsonify({"error" : "destination is required"}), 400
        return jsonify({"parcel" : user.update_order_destination(parcel_id, get_input["destination"])}), 200