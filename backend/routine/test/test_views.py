from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..serializers import *



class RoutineListCreateAPIViewCREATETest(TestCase):
    def setUp(self):
        self.URL = reverse('routine_list_create')
        self.credentials = {'email': 'test@a.com', 'password':'test1234!'}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    def test_routine_create(self):
        res = self.client.post(self.URL, 
            {
            "title": "created_routine",
            "category": "miracle",
            "goal": "To test create",
            "is_alarm": "True",
            "days": [{"day":"mon"}, {"day":"tue"}]
            },
            content_type='application/json')

        rou = Routine.objects.first()
        self.assertEqual(rou.title, 'created_routine')
        self.assertEqual(RoutineDay.objects.filter(routine=rou)[0].day, 'mon')
        self.assertEqual(RoutineResult.objects.filter(routine=rou)[0].result, 'not')
        self.assertEqual(res.data['status'], 201)


class RoutineListCreateAPIViewLISTTest(TestCase):
    def setUp(self):
        self.URL = reverse('routine_list_create')
        self.credentials = {'email': 'test@a.com', 'password':'test1234!'}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)
        for i in range(2):
            day = "mon" if i==0 else "tue" 
            self.client.post(self.URL,
                {
                "title": f"created_routine_{day}",
                "category": "miracle",
                "goal": "To test create",
                "is_alarm": "True",
                "days": [{"day": f"{day}"}]
                },
                content_type='application/json')
        Routine.objects.create(title='deleted_routine', is_deleted=True, account=self.user)

    def test_deleted_routine_list(self):
        url = self.URL + '?is-del=1'
        res = self.client.get(url)
        self.assertEqual(res.data['data'][0]['title'], 'deleted_routine')
        self.assertEqual(len(res.data['data']), 1)

    def test_alive_and_dated_routine_list(self):
        url = self.URL + '?date=20220927'
        res = self.client.get(url)
        self.assertEqual(res.data['data'][0]['title'], 'created_routine_tue')
        self.assertEqual(len(res.data['data']), 1)

    def test_alive_and_all_routine_list(self):
        res = self.client.get(self.URL)
        self.assertEqual(len(res.data['data']), 2)


class RoutineDetailAPIViewTest(TestCase):
    def setUp(self):
        self.credentials = {'email': 'test@a.com', 'password':'test1234!'}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)
        self.rou_obj = Routine.objects.create(account=self.user, title='routine')
        self.URL = reverse(viewname='routine_detail', kwargs={'pk':self.rou_obj.id})

    def test_routine_retrieve(self):
        res = self.client.get(self.URL)
        self.assertEqual(res.data['message'], 'You have successfully lookup the routine.')
        self.assertEqual(res.data['status'], 200)

    def test_routine_update(self):
        res = self.client.put(self.URL, {
            "title": "updated-routine",
            "category": "miracle",
            "goal": "updated",
            "is_alarm": 'False',
            "days": [
                {
                    "day": "thu"
                },
                {
                    "day": "fri"
                }
            ],
            "result": [
                {
                    "result": "not"
                }
            ]
            }, content_type='application/json')
        r = Routine.objects.get(id=self.rou_obj.id)
        self.assertEqual(res.data['message'], 'You have successfully updated the routine.')
        self.assertEqual(res.data['status'], 200)
    
    def test_routine_delete(self):
        rst_obj = RoutineResult.objects.create(routine=self.rou_obj)
        res = self.client.delete(self.URL, content_type='application/x-www-form-urlencoded')    
        # self.assertEqual(self.rou_obj.is_deleted, True)
        # self.assertEqual(rst_obj.is_deleted, True)
        self.assertEqual(res.data['status'], 200)
        self.assertEqual(res.data['message'], 'You have successfully deleted the routine.')

