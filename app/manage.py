from datetime import datetime
from flask import request

parcels = []

class Parcel:
    """Class to manipulate parcels."""

    def __init__(self):
        self.parcels = parcels

    def search_sender_parcels(self, sender_id):
        parcels = [parcel for parcel in self.parcels if parcel['sender_id'] == int(sender_id)]
        return parcels

    def update_parcel_status(self, id, status):
            parcel = self.search_parcel(id)
        if parcel:
            parcel[0].update({"status": status})
            return parcel
        return None  

    def search_sender_parcels(self, sender_id):
            parcels = [parcel for parcel in self.parcels if parcel['sender_id'] == int(sender_id)]
            return parcels


