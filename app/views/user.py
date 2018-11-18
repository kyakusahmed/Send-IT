def update_current_location(self, current_location, parcel_id):
    command = "UPDATE parcels SET current_location = '%s' WHERE parcel_id = '%s'" % (status, parcel_id)
    self.cursor.execute(command)
    return "status updated"    