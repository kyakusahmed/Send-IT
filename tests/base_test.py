import unittest
import json
from app.views import app2
from app.models.migrations import Migration
from .import user_register, admin_register, admin_login, user_login


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.migration = Migration()
        self.app1 = app2.test_client()
        
    
    # def create_tables():
    #     self.migration.create_tables([users, parcels])

    def return_admin_token(self):
        """admin token."""
        self.app1.post('/api/v1/users/register', content_type="application/json", json=admin_register)
        response = self.app1.post('/api/v1/users/login', json=admin_login)
        data = json.loads(response.data)
        return json.loads(response.data)['access_token']

    def return_user_token(self):
        """user token."""
        self.app1.post('/api/v1/users/register', json=user_register)
        response = self.app1.post('/api/v1/users/login', json=user_login)
        data = json.loads(response.data)
        return json.loads(response.data)['access_token']
        

    # def tearDown(self):
    #     self.migration.drop_tables([users, parcels])

    # def create_tables():
    #     self.migration.create_tables([users, parcels])

      
