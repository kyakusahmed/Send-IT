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
