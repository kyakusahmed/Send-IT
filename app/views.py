from flask import Flask, jsonify, request
from app.manage import Parcel

app2 = Flask(__name__)
parcel = Parcel()

@app2.route('/api/v1/parcels/sender/<int:sender_id>', methods=['GET'])
def get_all_parcels_by_user(sender_id):
    sender_parcels = parcel.search_sender_parcels(sender_id)
    return jsonify({'parcels': sender_parcels})