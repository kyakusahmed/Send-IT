from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .connection import DatabaseConnection



class Admin(DatabaseConnection):
    """ user database interaction."""

    def register_admin(self, first_name, last_name, email, password, role):
        try:
            command = """
            INSERT INTO USERS (first_name, last_name, email, password, role, created_at) VALUES('{}','{}','{}','{}','{}','{}')
            """.format( first_name, last_name, email, password, role, datetime.now())
            self.cursor.execute(command)
            return "user registered successfully"
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
               


