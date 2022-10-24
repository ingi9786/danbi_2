from celery import shared_task
from django.contrib.auth import get_user_model

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Celery Done"

@shared_task(bind=True)
def send_email_to_subscriber(self):
    user = get_user_model().objects.get(__exact="ingi9786@naver.com")
    