from flask import Flask, jsonify, request
from app.manage import Parcel

app2 = Flask(__name__)
parcel = Parcel()

@app2.route('/api/v1/parcels', methods=['GET'])
def get_all_orders():
    return jsonify({'parcels': parcel.get_all_parcels()}), 200