
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





