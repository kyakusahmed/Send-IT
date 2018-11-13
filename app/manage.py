from datetime import datetime
from flask import request

parcels = []

class Parcel:
    """Class to manipulate parcels."""

    def __init__(self):
        self.parcels = parcels
        

    def add_parcel(self, sender_id, location, name, phone, country, destination, weight, price):
        """add new parcel."""
        parcel = {
            "id": len(self.parcels)+1,
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