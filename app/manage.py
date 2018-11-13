from datetime import datetime
from flask import request

parcels = []

class Parcel:
    """Class to manipulate parcels."""

    def __init__(self):
        self.parcels = parcels

    def search_parcel(self, id):
        parcel = [parcel for parcel in self.parcels if parcel['id'] == int(id)]
        return parcel 