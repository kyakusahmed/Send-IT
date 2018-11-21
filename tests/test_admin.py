import json
from .base_test import BaseTest

class AdminTest(BaseTest):
       
    
    def test_update_status(self):
        token = self.return_admin_token()
        parcel= {
                "sender_name" : "ahmad kyakulumbye",
                "sender_phone" : "256706196611",
                "pickup_location" : "busabala road-zone 1",
                "recepient_name" : "muwonge badru",
                "recepient_phone":"254704196613",
                "recepient_country":"kenya",
                "destination":"nairobi-main street-plot 20",
                "weight": "50kg",
                "status":"pending"
                }
        self.app1.post('/api/v1/parcels', content_type="application/json", headers={"Authorization": "Bearer " + token},  data=json.dumps(parcel))
        response = self.app1.put('/api/v1/parcels/1/status',content_type="application/json", headers={"Authorization": "Bearer " + token},
            json={"status": "delivered"})
        print(response)
        assert response.status_code == 401
        assert json.loads(response.data)['msg'] == "unauthorised access"    

    def test_update_current_location_without_location(self):
        data = {
            "user_id": 1,
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": "50kg",
            "price":"500shs",
            "status":"pending"
        }
        self.app1.post('/api/v1/parcels',content_type="application/json", data=json.dumps(data))
        data = {"current_location":"eldoret"}
        response = self.app1.put('/api/v1/parcels/1',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401  

    def test_get_all_parcels_without_token(self):
        response = self.app1.get('/api/v1/parcels/admin')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401 

    def test_update_status_without_token(self):  
        data = {
            "user_id": 1,
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": "50kg",
            "status":"pending"
        }
        self.app1.post('/api/v1/parcels',content_type="application/json", data=json.dumps(data))
        data = {"status":"cancelled"}
        response = self.app1.put('/api/v1/parcels/1',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401    

    def test_update_user_to_admin_without_token(self):
        data = {
            "user_id": 1,
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": "50kg",
            "price":"500shs",
            "status":"pending"
        }
        self.app1.post('/api/v1/parcels',content_type="application/json", data=json.dumps(data))
        data = {"roles":"admin"}
        response = self.app1.put('/api/v1/parcels/1',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401

    # def test_get_user_not_found(self):
    #     response = self.app1.post('/api/v1/users/roles/1234')
    #     data = json.loads(response.get_data(as_text=True)) 
    #     self.assertEqual(data['msg'], "user not found")

    def test_role_is_required(self):
        data = {
            "user_id": 1,
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": "50kg",
            "price":"500shs",
            "status":"pending"
        }
        self.app1.post('/api/v1/parcels',content_type="application/json", data=json.dumps(data))
        data = {"roles":""}
        response = self.app1.put('/api/v1/users/roles/1',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['msg'], "Role is required"), 400

    # def test_unauthorised_acces(self):
        








