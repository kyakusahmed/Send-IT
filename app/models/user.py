from app.models.connection import DatabaseConnection
from datetime import datetime


class User(DatabaseConnection):
        def __init__(self):
                super().__init__()

        def find_parcel(self, parcel_id):
                command = """
                SELECT * from parcels WHERE parcel_id ={}
                """.format(parcel_id)
                self.cursor.execute(command)
                data = self.cursor.fetchone()
                return dataat

        def update_parcel_destination(self, destination, parcel_id):
                command = "UPDATE parcels SET destination = '%s' WHERE parcel_id = '%s'" % (destination, parcel_id)
                self.cursor.execute(command)
                return "status updated"        


