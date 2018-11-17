from app.models.connect import DatabaseConnection

class Migration(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def drop_tables(self):
        commands = (
        """ 
        DROP TABLE  CASCADE
        """,
        """ 
        DROP TABLE CASCADE
        """,
        """ 
        DROP TABLE  CASCADE
        """)
        for command in commands:
            self.cursor.execute(command)
    

    def create_tables(self):
    
        """ create tables in the PostgreSQL database"""
        commands = (
        """ CREATE TABLE IF NOT EXISTS USERS (
            USER_ID SERIAL PRIMARY KEY,
            FIRST_NAME VARCHAR(50) NOT NULL,
            LAST_NAME VARCHAR(50) NOT NULL,
            EMAIL VARCHAR(50),
            PASSWORD VARCHAR(50),
            ROLE VARCHAR(25) NOT NULL,
            CREATED_AT timestamp(6) without time zone
            )
        """,
        """ CREATE TABLE IF NOT EXISTS MENU (
                MENU_ID SERIAL PRIMARY KEY,
                FOOD_TITLE VARCHAR(50),
                DESCRIPTION VARCHAR(500) NOT NULL,
                PRICE VARCHAR(50) NOT NULL,
                STATUS VARCHAR(50) ,
                USER_ID INTEGER REFERENCES USERS(USER_ID)
        )
        """,
        """ CREATE TABLE IF NOT EXISTS  ORDERS (
                ORDERS_ID SERIAL PRIMARY KEY,
                USER_ID INTEGER REFERENCES USERS(USER_ID),
                QUANTITY VARCHAR(50),
                LOCATION VARCHAR(50),
                STATUS VARCHAR(50),
                CREATED_AT timestamp(6) without time zone
        )
        """)

        for command in commands:
            self.cursor.execute(command)