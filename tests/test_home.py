import unittest
from monolith.app import app


class TestHome(unittest.TestCase):

    def __init__(self, *args, **kw):
        super(TestHome, self).__init__(*args, **kw)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    # Test GET / (home)
    def test_home(self):
        test_app = app.test_client()

        response = test_app.get('/')
        self.assertEqual(response.status_code, 200)