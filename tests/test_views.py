import json
from .base_test import BaseTest

class UserTest(BaseTest):

    def test_update_current_location_without_token(self):
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
        response = self.app1.get('/api/v1/parcels')
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
        print(data)
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401    

    def test_update_user_to_admin_without_token(self):
        data1 = {"role":"admin"}
        response = self.app1.put('/api/v1/parcels/1',content_type="application/json", data=json.dumps(data1))
        data = json.loads(response.get_data(as_text=True))
        print(data)
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401


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
        self.assertEqual(json.loads(resp.data)["message"], "Login successful")
        

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

    def test_first_name_parameter_is_missing(self):
        data = {
            "first_name":"",
            "last_name":"waqas",
            "email":"ahmed@outlook.com",
            "password":"123456"
            }
        response = self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['message'], "Missing first_name parameter") 
        assert response.status_code == 406

    def test_last_name_missing(self):
        data = {
            "first_name":"mega",
            "last_name":"",
            "email":"ahmed@outlook.com",
            "password":"123456"
            }
        response = self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['message'], "Missing last_name parameter") 
        assert response.status_code == 406    

    def test_password_missing(self):
        data = {
            "first_name":"mega",
            "last_name":"waqas",
            "email":"ahmed@outlook.com",
            "password":""
            }
        response = self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['message'], "Missing password parameter") 
        assert response.status_code == 406        

    def test_email_is_missing(self):
        data = {
            "first_name":"mega",
            "last_name":"waqas",
            "email":"",
            "password":""
            }
        response = self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True)) 
        self.assertEqual(data['message'], "Missing email parameter") 
        assert response.status_code == 406            
        	
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
        self.assertEqual(data['message'], "invalid email") 
        assert response.status_code == 406

    def test_get_parcel_without_token(self):
        response = self.app1.get('/api/v1/parcels/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], "Missing Authorization Header")
        assert response.status_code == 401 

    def test_user_update_status_without_tokens(self):
        response =self.app1.put('/api/v1/parcel/1/user', json={"status": "cancelled","parcel_id":1})
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 401
        self.assertEqual(data['msg'], "Missing Authorization Header")  


    def test_user_register(self):
        data = {
           "first_name":"ahmed",
	       "last_name":"kyakus",
	       "email":"kyakus@outlook.com",
	       "password":"123456",
	       "role": "admin"
           }

 
        response = self.app1.post('/api/v1/users/register', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_all_parcels(self):
        token = self.return_user_token()
        response = self.app1.get("/api/v1/parcels", headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 401

    def test_user_register_email_exist(self):
        admin_register = {
            "first_name": "amina",
            "last_name": "joe",
            "email": "amina@admin.com",
            "password": "aminajoe",
            "role": "admin"
        }

        token = self.return_user_token()
        self.app1.post('/api/v1/users/register', json=admin_register)
        response = self.app1.post('/api/v1/users/register', json=admin_register)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['message'] == "user registered already"


    def test_successful_user_login(self):
        admin_register = {
            "first_name": "amina",
            "last_name": "joe",
            "email":"ahmed@outlook.com",
            "password":"123456",
            "role": "admin"
        }

        token = self.return_user_token()
        self.app1.post('/api/v1/users/register',content_type="application/json", data=json.dumps(admin_register))
        user_login = {
            "email":"ahmed@outlook.com",
            "password":"123456"
        }
        response = self.app1.post('/api/v1/users/login', headers={"Authorization": "Bearer " + token}, json=user_login)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == 'Login successful'

    def test_get_parcels_with_token(self):
        token = self.return_admin_token()
        token2 = self.return_user_token()
        data = {
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": 50
        }
        self.app1.post('/api/v1/parcels',content_type="application/json",
         headers={"Authorization": "Bearer " + token2},  data=json.dumps(data))
        response = self.app1.get('/api/v1/parcels', headers={"Authorization": "Bearer " + token})
        assert response.status_code == 200

    def test_update_users_to_admin(self):
        token= self.return_admin_token()
        data = {
           "first_name":"ahmed",
	       "last_name":"kyakus",
	       "email":"kyakus@outlook.com",
	       "password":"123456"
        }
        self.app1.post('/api/v1/users/register', json=data)
        data1 = {"role":"admin"}
        response = self.app1.put('/api/v1/users/1',content_type="application/json",
        headers={"Authorization": "Bearer " + token}, data=json.dumps(data1))
        data = json.loads(response.get_data(as_text=True))
        assert json.loads(response.data)['message'] == 'User role updated successfuly'
        assert response.status_code == 200

    def test_get_parcel_with_token(self):
        token= self.return_admin_token()
        response = self.app1.get('/api/v1/parcels/1', content_type="application/json", headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data['parcel'], dict)
        assert response.status_code == 200

    def test_view_user_parcels_history(self):
        token= self.return_user_token()
        response = self.app1.get('/api/v1/parcels/users/1', content_type="application/json", headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data['parcels'], list)
        assert response.status_code == 200

    def test_update_current_location(self):
        token = self.return_admin_token()
        token2 = self.return_user_token()
        data = {
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
        self.app1.post('/api/v1/parcels',content_type="application/json", headers={"Authorization": "Bearer " + token2}, data=json.dumps(data))
        data = {"current_location":"nakapiripiriti-town"}
        response = self.app1.put('/api/v1/parcels/1/location',content_type="application/json", headers={"Authorization": "Bearer " + token}, data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['parcel'], "current_location updated")
        assert response.status_code == 200 

    def test_admin_update_status_delivered(self):
        token = self.return_admin_token()
        token2 = self.return_user_token()
        data1 = {
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": "50kg",
            "status":"delivered"
        }
        self.app1.post('/api/v1/parcels',content_type="application/json", headers={"Authorization": "Bearer " + token2}, data=json.dumps(data1))
        data = {"status":"cancelled"}
        response = self.app1.put('/api/v1/parcels/1',content_type="application/json", headers={"Authorization": "Bearer " + token}, data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["message"], "parcel already delivered")
        assert response.status_code == 200 

    def test_update_destination(self):
        token2 = self.return_user_token()
        data1 = {
            "sender_name" : "ahmad kyakulumbye",
            "sender_phone" : "256706196611",
            "pickup_location" : "busabala road-zone 1",
            "recepient_name" : "muwonge badru",
            "recepient_phone":"254704196613",
            "recepient_country":"kenya",
            "destination":"nairobi-main street-plot 20",
            "weight": "50kg",
            "status":"delivered"
        }
        self.app1.post('/api/v1/parcels',content_type="application/json", headers={"Authorization": "Bearer " + token2}, data=json.dumps(data1))
        data = {"destination":"moldovia"}
        response = self.app1.put('/api/v1/parcels/1/destination',content_type="application/json", headers={"Authorization": "Bearer " + token2}, data=json.dumps(data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["parcel"], "destination updated")
        assert response.status_code == 200 

   



