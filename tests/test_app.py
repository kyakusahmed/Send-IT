import unittest
import json
from app.views import app2

class OrderTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app2.test_client()
        self.app.testing = True
        self.test_parcel = { 
            "country": "uganda",
            "destination": "kampala",
            "parcel_price": "500k",
            "parcel_weight": "1kg",
            "pickup_location": "nairobi",
            "recepient_name": "Ahmad",
            "recepient_phone": "256706196611",
            "sender_id": 1,
            "status":"pending"
            }

    def test_get_all_parcels(self):
        response = self.app.get("/api/v1/parcels")
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        self.assertIsInstance(data['parcels'], list)

    def test_get_parcel(self):
        self.app.post('/api/v1/parcels', json=self.test_parcel)
        response = self.app.get('/api/v1/parcels/1')
        assert response.status_code == 404

    def test_update_status(self):
        self.app.post('/api/v1/parcels', json=self.test_parcel)
        response =self.app.put('/api/v1/parcels/1', json={"status": "pending", "sender": 1})
        assert response.status_code == 404

    def test_update_status_not_found(self):
        self.app.post('/api/v1/parcels', json=self.test_parcel)
        response =self.app.get('/api/v1/parcels/12345')
        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "parcel not found"
        assert response.status_code == 404
   
    def test_parcel_not_found(self):
        response =self.app.get('/api/v1/parcels/12345')
        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "parcel not found"
        assert response.status_code == 404

    def test_field_is_required(self):
        required = { 
            "country": "uganda",
            "destination": "kampala",
            "parcel_price": "500k",
            "parcel_weight": "1kg",
            "pickup_location": "",
            "recepient_name": "kampala",
            "recepient_phone": "25706196611",
            "sender_id": 1}
        response = self.app.post('/api/v1/parcels', json=required)
        assert response.status_code == 406

    def test_get_all_parcels_by_user(self):
        response = self.app.get('/api/v1/parcels/sender/1')
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        self.assertIsInstance(data['parcels'], list)
   
    def test_add_parcel(self):
        self.app.post('/api/v1/parcels', json=self.test_parcel)
        response = self.app.get('/api/v1/parcels')
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        self.assertIsInstance(data, dict)

    def test_status_is_required(self):
        self.app.post('/api/v1/parcels', json=self.test_parcel)
        response =self.app.put('/api/v1/parcels/1', json={"status": "", "sender": 1})
        data = json.loads(response.get_data(as_text=True))
        assert data["error"] == "status is required"
        assert response.status_code == 406

    def test_sender_is_required(self):
        self.app.post('/api/v1/parcels', json=self.test_parcel)
        response =self.app.put('/api/v1/parcels/1', json={"status": "cancelled", "sender": ""})
        data = json.loads(response.get_data(as_text=True))
        assert data["error"] == "sender is required"
        assert response.status_code == 406   

    def test_weight_required(self):
        required = { 
            "country": "uganda",
            "destination": "kampala",
            "parcel_price": "500k",
            "parcel_weight": "",
            "pickup_location": "",
            "recepient_name": "kampala",
            "recepient_phone": "25706196611",
            "sender_id": 1}
        self.app.post('/api/v1/parcels', json=required)
        response =self.app.get('/api/v1/parcels')
        assert response.status_code == 200 

    def test_price_required(self):
        required = { 
            "country": "uganda",
            "destination": "kampala",
            "parcel_price": "",
            "parcel_weight": "5kg",
            "pickup_location": "nairobi",
            "recepient_name": "kampala",
            "recepient_phone": "25706196611",
            "sender_id": 1}
        self.app.post('/api/v1/parcels', json=required)
        response =self.app.get('/api/v1/parcels')
        assert response.status_code == 200        
        
    def test_recipient_name_is_required(self):
        required = { 
            "country": "uganda",
            "destination": "kampala",
            "parcel_price": "",
            "parcel_weight": "5kg",
            "pickup_location": "nairobi",
            "recepient_name": "",
            "recepient_phone": "25706196611",
            "sender_id": 1}
        self.app.post('/api/v1/parcels', json=required)
        response =self.app.get('/api/v1/parcels')
        assert response.status_code == 200        