

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