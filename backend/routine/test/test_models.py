from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Routine, RoutineDay, RoutineResult



class RoutineModelTest(TestCase):
    def setUp(self): 
        self.user = get_user_model().objects.create_user('test@a.com', 'test1234')
        self.rou_obj = Routine.objects.create(account=self.user, title='test routine')
        self.day_obj = RoutineDay.objects.create(day='mon', routine=self.rou_obj)
        self.rst_obj = RoutineResult.objects.create(routine=self.rou_obj)

    def test_days_property(self):
        self.assertEqual(self.rou_obj.days[0], self.day_obj)
    
    def test_result_property(self):
        self.assertEqual(self.rou_obj.result[0], self.rst_obj)