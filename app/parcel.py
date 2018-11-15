from datetime import datetime
from flask import request

parcels = []

class Parcel:
    """Class to manipulate parcels."""

    def __init__(self):
        self.parcels = parcels

    def get_all_parcels(self):
        """get list of all parcels."""
        return self.parcels

    def last_parcel_id(self):
        if len(self.parcels) < 1:
            return 1
        return self.parcels[-1]['id'] + 1    

    def add_parcel(self, sender_id, location, name, phone, country, destination, weight, price):
        """add new parcel."""
        parcel = {
            "id": self.last_parcel_id(),
            "sender_id": sender_id,
            "pickup_location": location,
            "recepient_name": name, 
            "recepient_phone": phone, 
            "country":country, 
            "destination": destination,
            "parcel_weight": weight,
            "parcel_price": price,
            "status": "Pending",
            "created": str(datetime.now())
        }
        self.parcels.append(parcel)
        return parcel

    def search_parcel(self, id):
        parcel = [parcel for parcel in self.parcels if parcel['id'] == int(id)]
        return parcel 

    def search_sender_parcels(self, sender_id):
        parcels = [parcel for parcel in self.parcels if parcel['sender_id'] == int(sender_id)]
        return parcels

    def get_parcel(self, id):
        return self.search_parcel(id)

    def update_parcel_status(self, id, status):
        parcel = self.search_parcel(id)
        if parcel:
            parcel[0].update({"status": status})
            return parcel
        return None  

    def search_sender_parcels(self, sender_id):
            parcels = [parcel for parcel in self.parcels if parcel['sender_id'] == int(sender_id)]
            return parcels



