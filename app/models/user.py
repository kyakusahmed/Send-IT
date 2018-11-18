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