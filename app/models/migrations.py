from app.models.connection import DatabaseConnection

class Migration(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def drop_tables(self):
        commands = (
        """ 
        DROP TABLE users CASCADE
        """,
        """
        DROP TABLE parcels CASCADE
        """
        )
        for command in commands:
            self.cursor.execute(command)
    

    def create_tables(self):
    
        """ create tables in the PostgreSQL database"""
        commands = (
        """ CREATE TABLE IF NOT EXISTS USERS (
            USER_ID SERIAL PRIMARY KEY,
            FIRST_NAME VARCHAR(50) NOT NULL,
            LAST_NAME VARCHAR(50) NOT NULL,
            EMAIL VARCHAR(50) UNIQUE,
            PASSWORD VARCHAR(50),
            ROLE VARCHAR(25) NOT NULL,
            CREATED_AT timestamp(6) without time zone
            )
        """,
        """ CREATE TABLE IF NOT EXISTS PARCELS (
            PARCEL_ID  SERIAL PRIMARY KEY UNIQUE,
            user_id INTEGER REFERENCES USERS(USER_ID),
            SENDER_NAME VARCHAR(50) NOT NULL,
            SENDER_PHONE VARCHAR(50) NOT NULL,
            PICKUP_LOCATION VARCHAR(50) NOT NULL,
            RECEPIENT_NAME VARCHAR(50) NOT NULL,
            RECEPIENT_PHONE VARCHAR(50) NOT NULL,
            RECEPIENT_COUNTRY VARCHAR(50) NOT NULL,
            DESTINATION VARCHAR(50) NOT NULL,
            WEIGHT VARCHAR(50),
            PRICE VARCHAR(50),
            STATUS VARCHAR(25) NOT NULL,
            CURRENT_LOCATION VARCHAR(50),
            CREATED_AT timestamp(6) without time zone
            )
        """
        )

        for command in commands:
            self.cursor.execute(command)