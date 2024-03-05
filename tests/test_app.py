import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page(self):
        # Test home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello World!")

    def test_index_page(self):
        # Test index page
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Yo Country', response.data)

    def test_login_page(self):
        # Test login page GET request
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Page', response.data)

        # Test login with valid credentials
        response = self.app.post('/login', data=dict(username='john', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, john!', response.data)

        # Test login with invalid credentials
        response = self.app.post('/login', data=dict(username='john', password='wrongpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_success_page(self):
        # Test success page
        response = self.app.get('/success/john')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, john!', response.data)

if __name__ == '__main__':
    unittest.main()
