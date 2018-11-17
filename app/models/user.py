from app.models.connection import DatabaseConnection
from datetime import datetime


class User(DatabaseConnection):
        def __init__(self):
                super().__init__()

        def update_status(self, status, parcel_id):
            command = "UPDATE parcels SET status = '%s' WHERE parcel_id = '%s'" % (status, parcel_id)
            self.cursor.execute(command)
            return "status updated"    