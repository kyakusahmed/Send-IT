from flask import Flask, jsonify, request
from app.manage import Parcel

app2 = Flask(__name__)
parcel = Parcel()

@app2.route('/api/v1/parcels', methods=['POST'])
def add_parcel():
    data = request.get_json()
    if not data.get("recepient_name"):
        return jsonify({"error": "recipient name is required"}), 200
    elif not data.get("recepient_phone"):
        return jsonify({"error": "recipient phone is required"}), 200
    elif not data.get("recepient_country"):
        return jsonify({"error": "recipient country is required"}), 200
    elif not data.get("recepient_destination"):
        return jsonify({"error": "recipient destination is required"}), 200
    elif not data.get("sender_id"):
        return jsonify({"error": "sender is required"}), 200
    elif not data.get("location"):
        return jsonify({"error": "sender location is required"}), 200
    elif not data.get('weight'):
        return jsonify({"error": "weight required"}), 200
    elif not data.get('price'):
        return jsonify({"error": "price required"}), 200

    save_parcel = parcel.add_parcel(data['sender_id'], 
        data['location'], 
        data['recepient_name'],
        data['recepient_phone'],
        data['recepient_country'],
        data['recepient_destination'],
        data['weight'],
        data['price'],
    )
    return jsonify({"parcel": save_parcel}), 201