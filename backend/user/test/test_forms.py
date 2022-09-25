from django.test import TestCase
from ..forms import CustomUserCreationForm



class CustomUserCreationFormTests(TestCase):
    def test_password_validation(self):
        # check password identical
        form = CustomUserCreationForm(data={'email':'test1@a.com', 'password1':'test1234!', 'password2':'test1235!'})
        self.assertFalse(form.is_valid())
        
        # check minimum length of password
        form = CustomUserCreationForm(data={'email':'test1@a.com', 'password1':'test12!', 'password2':'test12!'})
        self.assertFalse(form.is_valid())

        # check must contain special_char
        form = CustomUserCreationForm(data={'email':'test1@a.com', 'password1':'test1234', 'password2':'test1234'})
        self.assertFalse(form.is_valid())
        
        # check must contain normal char
        form = CustomUserCreationForm(data={'email':'test1@a.com', 'password1':'!@##1234', 'password2':'!@##1234'})
        self.assertFalse(form.is_valid())
        
        # check must contain number
        form = CustomUserCreationForm(data={'email':'test1@a.com', 'password1':'!@##test', 'password2':'!@##test'})
        self.assertFalse(form.is_valid())
        
        # check valid form
        form = CustomUserCreationForm(data={'email':'test1@a.com', 'password1':'dlsrl1234!', 'password2':'dlsrl1234!'})
        self.assertTrue(form.is_valid())
    