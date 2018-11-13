from flask import Flask, jsonify, request
from app.manage import Parcel

app2 = Flask(__name__)
parcel = Parcel()

@app2.route('/api/v1/parcels/<int:id>', methods=['PUT'])
def update_status(id):
    get_input = request.get_json()
    if not get_input.get("status"):
        return jsonify({"error" : "status is required"}), 200
    if not get_input.get("sender"):
        return jsonify({"error" : "sender is required"}), 200
    parcel2 = parcel.search_parcel(id)
    if not parcel2:
        return jsonify({"message": 'parcel not found'}), 404
    else:
        if parcel2[0]['sender_id'] != get_input["sender"]:
            return jsonify({"message": 'parcel not yours'}), 400
        if parcel2[0]['status'] == "Delivered":
            return jsonify({"message": 'parcel already delivered'}), 400
        return jsonify({"parcel" : parcel.update_parcel_status(id, get_input["status"])}), 200