from django.test import TestCase
from django.contrib.auth import get_user_model



class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(email='test@a.com', password='test1234!', last_name='kim', first_name='ingi')

    def test_get_short_name_method(self):
        self.assertEqual(self.user.get_short_name(), 'ingi')

    def test_get_full_name_method(self):
        self.assertEqual(self.user.get_full_name(), 'ingi kim')


class UserManagerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
    
    def test_create_user(self):
        # Fail case
        with self.assertRaises(ValueError):
            self.User.objects.create_user('', 'test1234!')
        with self.assertRaises(ValueError):
            self.User.objects.create_user('test.com', 'test1234!')
        # Success Case
        user = self.User.objects.create_user('test1@a.com', 'test1234!')
        self.assertEqual(str(user), 'test@a.com')
        
    def test_create_superuser(self):
        # Fail case
        with self.assertRaises(ValueError):
            su_user = self.User.objects.create_superuser('test@a.com', 'test1234!', is_superuser=False)
        # Success Case
        su_user = self.User.objects.create_superuser('test@a.com', 'test1234!')
        self.assertEqual(str(su_user), 'test@a.com')