import json
from .base_test import BaseTest

class UserTest(BaseTest):
       
    def test_register_user(self):
        data = {
           "first_name":"james",
	       "last_name":"dinho",
	       "email":"yoobmed@outlook.com",
	       "password":"123456"
        }
        response = self.app1.post('/api/v1/users/register', content_type="application/json", json=data)
        self.assertEqual(response.status_code, 201)
        

    def test_user_login(self):
        data = {
           "first_name":"ahmed",
	       "last_name":"kyakus",
	       "email":"kyakus@outlook.com",
	       "password":"123456",
	       "role": "admin"
           }
        self.app1.post('/api/v1/users/register', content_type = "application/json", json=data)
     
        data1 = {
            "email": "kyakus@outlook.com",
            "password": "123456"
        }
        resp = self.app1.post('/api/v1/users/login', content_type = "application/json", json=data1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)["status"], "Login successful")

    def test_update_destination(self):
        token = self.return_user_token()
        
        parcel= {

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
        self.app1.post('/api/v1/parcels', headers={"Authorization": "Bearer " + token}, json=parcel)
        response = self.app1.put('/api/v1/parcels/1',headers={"Authorization": "Bearer " + token},
            json={"destination": "lubaga","parecl_id":1})
        assert response.status_code == 200
        assert json.loads(response.data)['parcel'] == "destination updated"      

    def test_update_destination_without_token(self):
        response =self.app1.put('/api/v1/parcels/1', json={"destination": "lubaga","parecl_id":1})
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 401
        self.assertEqual(data['msg'], "Missing Authorization Header")  

    def test_user_place_parcel_without_token(self):
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

        response = self.app1.post('/api/v1/parcels',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401     

    def test_some_fields_are_missing(self):
        data = {
            
            "last_name":"",
            "email":"ahmed@outlook.com",
            "password":"123456",
            "role":"user"
            }
        response = self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['error'], "some fields are missing") 
        assert response.status_code == 200  
        	
    def test_invalid_email(self):
        data = {	
            "first_name":"ahmad",
            "last_name":"john",
            "email":"@outlook.com",
            "password":"123456",
            "role":"user"
        }
        response = self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['msg'], "invalid email") 
        assert response.status_code == 406  
