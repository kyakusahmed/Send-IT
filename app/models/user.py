

from app.models.connection import DatabaseConnection
from datetime import datetime


class User(DatabaseConnection):
        def __init__(self):
                super().__init__()


        def update_status(self, status, parcel_id):
            command = "UPDATE parcels SET status = '%s' WHERE parcel_id = '%s'" % (status, parcel_id)
            self.cursor.execute(command)
            return "status updated"    

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


        def register_user(self, first_name, last_name, email, password, role):
            try:
                command = """
                INSERT INTO users (first_name, last_name, email, password, role, created_at) VALUES('{}','{}','{}','{}','{}','{}')
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

        def admin_signin(self, email, password):
            try:
                command = """
                SELECT * FROM users WHERE email= '{}' AND password = '{}'
                """.format(email, password)
                self.cursor.execute(command)
                user1 = self.cursor.fetchone()
                return user1
            except Exception as ex:
                return "failed {}".format(ex)        

        def get_user_by_email(self, email):
            try:
                command = """
                SELECT * FROM users WHERE email='{}'
                """.format(email)
                self.cursor.execute(command)
                email = self.cursor.fetchone()
                return email 
            except Exception as ex:
                return "failed {}".format(ex)

        def add_user(self, user):
            try:
                if self.get_user_by_email(user.email) == 'failed':
                    command = """INSERT INTO Users (first_name, last_name , email, password, role, "")
                                VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING first_name, last_name , email, password, role ;
                                """
                    self.cursor.execute(command)
                    user = self.cursor.fetchone()
                    return user
                else:
                    return 'user exists'    
            except Exception as ex:
                return "failed {}".format(ex)        
              
       def view_parcel_history(self, user_id):
              command = """
              SELECT * from parcels WHERE user_id = {}
              """.format(user_id)
              self.cursor.execute(command)
              return self.cursor.fetchall()




        def parcel(self, user_id):
                try:
                    command = """
                    DELETE from parcels WHERE parcel_id = {}
                    """.format(parcel_id)
                    self.cursor.execute(command)
                    return  "data deleted"
                except Exception as ex:
                    return "failed {}".format(ex)   

        def view_all_parcels(self):
          command = """
          select row_to_json(row) from (SELECT * FROM parcels) row 
          """
          self.cursor.execute(command)
          return self.cursor.fetchall()

        def place_parcel_delivery_order(self, user_id, pickup_location, recepient_name, recepient_phone, recepient_country, 
                                        destination, weight, price, status, created_at):
          command = """INSERT INTO parcels (user_id, pickup_location, recepient_name, recepient_phone, recepient_country, 
          destination, weight, price, status, created_at)  VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}')
          """.format(user_id, pickup_location, recepient_name, recepient_phone, ecepient_country, 
          destination, weight, price, status, str(datetime.now()))
          self.cursor.execute(command)
          return "parcel delivery order is placed"

