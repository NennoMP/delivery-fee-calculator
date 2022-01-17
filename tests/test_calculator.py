import unittest
from monolith.app import app


class TestDelivery(unittest.TestCase):

    def __init__(self, *args, **kw):
        super(TestDelivery, self).__init__(*args, **kw)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    # Generic tests for the endpoint
    def test_endpoint(self):
        test_app = app.test_client()

        # Try un-allowed method
        response = test_app.get('/delivery_calculator')
        self.assertEqual(response.status_code, 405)

    # Test develiveries with invalid <cart_value>
    def test_cart_exceptions(self):
        test_app = app.test_client()

        # <cart_value> invalid (negative)
        payload = {
                'cart_value': -5,
                'delivery_distance': 2000,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

        # <cart_value> invalid (equal to 0)
        payload = {
                'cart_value': 0,
                'delivery_distance': 2000,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

    # Test develiveries with valid <cart_value>
    def test_cart(self):
        test_app = app.test_client()

        # Base case
        payload = {
                'cart_value': 790,
                'delivery_distance': 2235,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 710)

        # <cart_value> equal to 10€
        payload = {
                'cart_value': 1000,
                'delivery_distance': 2235,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 500)

        # <cart_value> greater than 10€
        payload = {
                'cart_value': 1500,
                'delivery_distance': 2235,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 500)

        # <cart_value> equal to 100€
        payload = {
                'cart_value': 10000,
                'delivery_distance': 2235,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 0)

        # <cart_value> greater than 100€
        payload = {
                'cart_value': 10000,
                'delivery_distance': 2235,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 0)

        # post delivery fee with total fee greater than 15€
        payload = {
                'cart_value': 100,
                'delivery_distance': 6000,
                'number_of_items': 20,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 1500)

    # Test develiveries with invalid <delivery_distance>
    def test_distance_exceptions(self):
        test_app = app.test_client()

        # <delivery_distance> invalid (negative)
        payload = {
                'cart_value': 500,
                'delivery_distance': -5,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

        # <delivery_distance> invalid (equal to 0)
        payload = {
                'cart_value': 500,
                'delivery_distance': 0,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

    # Test develiveries with valid <delivery_distance>
    def test_distance(self):
        test_app = app.test_client()

        # <delivery_distance> smaller than 500 meters
        payload = {
                'cart_value': 500,
                'delivery_distance': 300,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 600)

        # <delivery_distance> not exact value
        payload = {
                'cart_value': 500,
                'delivery_distance': 1499,
                'number_of_items': 4,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 800)

    # Test develiveries with invalid <number_of_items>
    def test_items_exceptions(self):
        test_app = app.test_client()

        # <number_of_items> invalid (negative)
        payload = {
                'cart_value': 500,
                'delivery_distance': 1000,
                'number_of_items': -5,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

        # <number_of_items> invalid (equal to 0)
        payload = {
                'cart_value': 500,
                'delivery_distance': 1000,
                'number_of_items': 0,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

    # Test develiveries with valid <number_of_items>
    def test_items(self):
        test_app = app.test_client()

        # <number_of_items> greater than 4
        payload = {
                'cart_value': 500,
                'delivery_distance': 1000,
                'number_of_items': 10,
                'time': '2023-10-12T13:00:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 1000)

    # Test develiveries with invalid <time>
    def test_time_exceptions(self):
        test_app = app.test_client()

        # <time> is not a datetime
        payload = {
                'cart_value': 500,
                'delivery_distance': 2000,
                'number_of_items': 4,
                'time': 'wrong'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')
        
        # <time> is not ISO format
        payload = {
                'cart_value': 500,
                'delivery_distance': 2000,
                'number_of_items': 4,
                'time': '2023-10-12'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

        # <time> in the past
        payload = {
                'cart_value': 500,
                'delivery_distance': 2000,
                'number_of_items': 4,
                'time': '2000-09-23T16:30:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_response['status'], 'Failed')

    # Test develiveries with valid <time>
    def test_time(self):
        test_app = app.test_client()

        # <time> during Friday rush
        payload = {
                'cart_value': 500,
                'delivery_distance': 1000,
                'number_of_items': 6,
                'time': '2022-09-23T16:30:00Z'
        }
        response = test_app.post('/delivery_calculator', json=payload)
        json_response = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(json_response['delivery_fee'], 880)