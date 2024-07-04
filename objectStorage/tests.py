from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
import json
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class SignUpViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_signup_success(self):
        with patch('django.core.mail.send_mail') as mock_send_mail:
            data = {
                'username': 'hosein',
                'email': 'hoseinbm138084@gmail.com',
                'password': '123'
            }
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(), {'message': 'User created successfully'})
            self.assertTrue(User.objects.filter(email='hoseinbm138084@gmail.com').exists())
            mock_send_mail.assert_called_once()

    def test_signup_missing_email_password(self):
        data = {
            'username': 'hosein',
            'email': '',
            'password': ''
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Email and password are required'})

    def test_signup_existing_email(self):
        User.objects.create_user(username='hosein', email='hoseinbm138084@gmail.com', password='123')
        data = {
            'username': 'hosein12',
            'email': 'hoseinbm138084@gmail.com',
            'password': 'password123'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'User with that email already exists'})

    def test_signup_existing_username(self):
        User.objects.create_user(username='ali', email='hoseinbm138084@gmail.com', password='123')
        data = {
            'username': 'ali',
            'email': 'hosein.borimnejad1380@gmail.com',
            'password': '123'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'User with that username already exists'})

    def test_signup_invalid_json(self):
        response = self.client.post(self.url, 'invalid json', content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid JSON format in request body'})

    def test_signup_method_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Method not allowed'})





class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')  # Make sure you have a URL pattern named 'login'
        self.user = User.objects.create_user(username='hosein', email='hoseinbm138084@gmail.com', password='112')

    def test_login_success_with_email(self):
        data = {
            'text': 'hoseinbm138084@gmail.com',
            'password': '112'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logged in successfully"})

    def test_login_success_with_username(self):
        data = {
            'text': 'hosein',
            'password': '112'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logged in successfully")

    def test_login_missing_email_or_password(self):
        data = {
            'text': 'hoseinbm138084@gmail.com',
            'password': ''
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Email or password is empty'})

    def test_login_invalid_email_or_password(self):
        data = {
            'text': 'hoseinb22m138084@gmail.com',
            'password': '1314'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid email or password'})

    def test_login_missing_username_or_password(self):
        data = {
            'text': 'hosein',
            'password': ''
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'username or password is empty'})

    def test_login_nonexistent_username(self):
        data = {
            'text': 'ali',
            'password': '112'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'User with that username does not exists'})

    def test_login_invalid_json(self):
        response = self.client.post(self.url, 'invalid json', content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid JSON format in request body'})

    def test_login_method_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Method not allowed'})
