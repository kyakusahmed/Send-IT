


@app2.route('/api/v1/parcels/users/<int:user_id>', methods=['GET'])
def view_user_parcels_history(user_id):
    user_parcels = user.view_parcel_history(user_id)
    return jsonify({'parcels': user_parcels})