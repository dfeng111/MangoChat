import unittest
from login import login

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.login = login.test_client()
        # Propagate exceptions to the test client
        self.login.testing = True

    def tearDown(self):
        pass

    def test_login_correct_credentials(self):
        # Simulate a POST request with correct username and password
        response = self.login.post('/login', data=dict(username='john', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, john!', response.data)

    def test_login_incorrect_username(self):
        # Simulate a POST request with incorrect username
        response = self.login.post('/login', data=dict(username='wronguser', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password. Please try again.', response.data)

    def test_login_incorrect_password(self):
        # Simulate a POST request with incorrect password
        response = self.login.post('/login', data=dict(username='john', password='wrongpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password. Please try again.', response.data)

if __name__ == '__main__':
    unittest.main()