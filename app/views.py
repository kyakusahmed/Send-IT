from flask import Flask, jsonify, request
from app.parcel import Parcel

app2 = Flask(__name__)
parcel = Parcel()


from flask import Flask, jsonify, request
from app.parcel import Parcel

app2 = Flask(__name__)
parcel = Parcel()

@app2.route('/api/v1/parcels', methods=['GET'])
def get_all_orders():
    return jsonify({'parcels': parcel.get_all_parcels()}), 200

@app2.route('/api/v1/parcels', methods=['POST'])
def add_parcel():
    data = request.get_json()
    if not data.get("recepient_name"):
        return jsonify({"error": "recipient name is required"}), 400
    elif not data.get("recepient_phone"):
        return jsonify({"error": "recipient phone is required"}), 400
    elif not data.get("recepient_country"):
        return jsonify({"error": "recipient country is required"}), 400
    elif not data.get("recepient_destination"):
        return jsonify({"error": "recipient destination is required"}), 406
    elif not data.get("sender_id"):
        return jsonify({"error": "sender is required"}), 400
    elif not data.get("location"):
        return jsonify({"error": "sender location is required"}), 400
    elif not data.get('weight'):
        return jsonify({"error": "weight required"}), 400
    elif not data.get('price'):
        return jsonify({"error": "price required"}), 400
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
    
@app2.route('/api/v1/parcels/<int:id>', methods=['GET'])
def get_parcel(id):
    """get specific parcel."""
    parcel2 = parcel.search_parcel(id)
    if not parcel2:
        return jsonify({"message": 'parcel not found'}), 404
    return jsonify({"parcel": parcel2}), 200  

@app2.route('/api/v1/parcels/<int:id>', methods=['PUT'])
def update_status(id):
    get_input = request.get_json()
    if not get_input.get("status"):
        return jsonify({"error" : "status is required"}), 400
    if not get_input.get("sender"):
        return jsonify({"error" : "sender is required"}), 400
    parcel2 = parcel.search_parcel(id)
    if not parcel2:
        return jsonify({"message": 'parcel not found'}), 404
    else:
        if parcel2[0]['sender_id'] != get_input["sender"]:
            return jsonify({"message": 'parcel not yours'}), 400
        if parcel2[0]['status'] == "Delivered":
            return jsonify({"message": 'parcel already delivered'}), 400
        return jsonify({"parcel" : parcel.update_parcel_status(id, get_input["status"])}), 200

@app2.route('/api/v1/parcels/sender/<int:sender_id>', methods=['GET'])
def get_all_parcels_by_user(sender_id):
    sender_parcels = parcel.search_sender_parcels(sender_id)
    return jsonify({'parcels': sender_parcels}), 200