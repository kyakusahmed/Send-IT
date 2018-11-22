from app.models.connection import DatabaseConnection
from datetime import datetime

class User(DatabaseConnection):
        def __init__(self):
                super().__init__()
        
        def update_status(self,parcel_id,status):
            command = "UPDATE parcels SET status = '%s' WHERE parcel_id = '%s'" % (status, parcel_id)
            self.cursor.execute(command)
            return "status updated"    

        def find_parcel(self, parcel_id):
            command = """
            SELECT * from parcels WHERE parcel_id ={}
            """.format(parcel_id)
            self.cursor.execute(command)
            data = self.cursor.fetchone()
            return data

        def update_parcel_destination(self, destination, parcel_id):
            command = "UPDATE parcels SET destination = '%s' WHERE parcel_id = '%s'" % (parcel_id, destination)
            self.cursor.execute(command)
            return "destination updated"        


        def register_user(self, first_name, last_name, email, password, role):
            try:
                command = """
                INSERT INTO USERS (first_name, last_name, email, password, role, created_at) VALUES('{}','{}','{}','{}','{}','{}')
                """.format( first_name, last_name, email, password, role, datetime.now())
                self.cursor.execute(command)
                return "user registered successfully"
            except Exception as ex:
                return "failed {}".format(ex)

        def user_signin(self, email, password):
            try:
                command = """
                SELECT * FROM users WHERE email= '{}' AND password = '{}'
                """.format(email, password)
                self.cursor.execute(command)
                user1 = self.cursor.fetchone()
                return user1
            except Exception as ex:
                return "failed {}".format(ex)  

        def get_user_by_ID(self, user_id):
            try:
                command = """
                SELECT * FROM users WHERE user_id='{}'
                """.format(user_id)
                self.cursor.execute(command)
                user = self.cursor.fetchone()
                return user 
            except Exception as ex:
                return "failed {}".format(ex)

        def get_user_by_email(self, email):
            command = """
            SELECT * FROM users WHERE email='{}'
            """.format(email)
            self.cursor.execute(command)
            user = self.cursor.fetchone()
            return user

        def add_user(self, user):
            try:
                command = """INSERT INTO Users (first_name, last_name , email, password, created_at)
                            VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING first_name, last_name , email, password, datetime.now();
                            """

                self.cursor.execute(command)
                user = self.cursor.fetchone()
                return user
            except Exception as ex:
                return "failed {}".format(ex)        
              
        def view_parcel_history(self, user_id):
            command = """
            SELECT * from parcels WHERE user_id = {}
            """.format(user_id)
            self.cursor.execute(command)
            parcels = self.cursor.fetchall()
            return parcels  

        def view_all_parcels(self):
            command = """
            SELECT * FROM parcels 
            """
            self.cursor.execute(command)
            results= self.cursor.fetchall()
            return results

        def place_parcel_delivery_order(self, user_id, sender_name, sender_phone, pickup_location, recepient_name, recepient_phone, recepient_country, 
                                        destination, weight, price, status):
            command = """INSERT INTO parcels (user_id, sender_name, sender_phone, pickup_location, recepient_name, recepient_phone, recepient_country, 
            destination, weight, status, created_at)  VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}')
            """.format(user_id, sender_name, sender_phone, pickup_location, recepient_name, recepient_phone, recepient_country, 
            destination, weight, price, status, datetime.now())
            self.cursor.execute(command)
            return "successful"
        
        def update_current_location(self, current_location, parcel_id):
            command = "UPDATE parcels SET current_location = '%s' WHERE parcel_id = '%s'" % (parcel_id, current_location)
            self.cursor.execute(command)
            return "current_location updated" 

        def update_user_to_admin(self, user_id, role):
            command = "UPDATE users SET role = '%s' WHERE user_id = '%s'" % (role, user_id)
            self.cursor.execute(command)
            return "Role updated" 

            



