

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
