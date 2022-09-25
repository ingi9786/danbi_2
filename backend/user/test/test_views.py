from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..forms import *



class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.URL = reverse('register')
        self.User = get_user_model()
        
    def test_GET_register_form(self):
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'register.html')
        
    def test_POST_register_form(self):
        res = self.client.post(self.URL, {
            'email': 'test1@a.com',
            'password1': 'test1234!',
            'password2': 'test1234!'
        })
        self.assertEqual(res.status_code, 302)
        user = self.User.objects.first()
        self.assertEqual(user.email, 'test1@a.com')

    def test_POST_register_form_no_data(self):
        res = self.client.post(self.URL)
        self.assertEqual(res.status_code, 200)
        user = self.User.objects.first()
        self.assertEqual(user, None)


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.URL = reverse('login')
        self.credentials = {
            'email': 'test1@a.com',
            'password': 'test1234!'
        }
        self.User = get_user_model()
        self.user = self.User.objects.create_user(**self.credentials)
    
    def test_GET_login_view(self):
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'login.html')

    def test_POST_login_view(self):
        res = self.client.post(self.URL, {'username': 'test1@a.com',
                                          'password': 'test1234!'})
        self.assertEqual(res.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), 1)
