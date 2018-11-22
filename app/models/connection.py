import psycopg2
import os

class DatabaseConnection:
 
    def __init__(self):
        if os.getenv('APP_SETTINGS') == 'testing':
            self.db = 'test_db'
        else:
            self.db = 'sendit'

        try:
            self.conn = psycopg2.connect(
            database="d7mcn5rj3q8pnl", user="", password="29a416b2acdb956b73715f37028a7b5637f7e7c8f2d9b50908eddf1dd7458ef0", port="5432", host="ec2-107-21-93-132.compute-1.amazonaws.com"
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print("connected")
            print(self.db)

            # self.conn = psycopg2.connect(
            # database=self.db, user="postgres", password="1988", port="5432", host="127.0.0.1"
            # )
            # self.conn.autocommit = True
            # self.cursor = self.conn.cursor()
            # print("connected")
        except Exception as ex:
            print("connection failed {}".format(ex))