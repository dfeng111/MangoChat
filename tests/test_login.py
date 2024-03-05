import unittest
from flask import app

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_login_correct_credentials(self):
        # Simulate a POST request with correct credentials
        response = self.app.post('/login', data=dict(username='chris', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, john!', response.data)

    def test_login_incorrect_username(self):
        # Simulate a POST request with incorrect username
        response = self.app.post('/login', data=dict(username='wronguser', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password. Please try again.', response.data)

    def test_login_incorrect_password(self):
        # Simulate a POST request with incorrect password
        response = self.app.post('/login', data=dict(username='chris', password='wrongpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password. Please try again.', response.data)

if __name__ == '__main__':
    unittest.main()
