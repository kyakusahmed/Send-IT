from flask import Flask, jsonify, request
from app.manage import Parcel

app2 = Flask(__name__)
parcel = Parcel()


@app2.route('/api/v1/parcels/<int:id>', methods=['GET'])
def get_parcel(id):
    """get specific order."""
    parcel2 = parcel.search_parcel(id)
    if not parcel2:
        return jsonify({"message": 'parcel not found'}), 404
    return jsonify({"parcel": parcel2}), 200  