from celery import shared_task
import mailchimp_transactional
from mailchimp_transactional.api_client import ApiClientError
from django.conf import settings
from django.http import JsonResponse

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Celery Done"


@shared_task(bind=True)
def ping_task(self):
    mailchimp = mailchimp_transactional.Client(
        api_key=settings.MAILCHIMP_TRANSACTIONAL_API_KEY,
    )
    try:
        mailchimp.users.ping()
        return JsonResponse({
            'detail': 'Everything is working fine',
        })
    except ApiClientError as error:
        return 'error occur'

@shared_task(bind=True)
def send_email_to_subscriber(self):
    mailchimp = mailchimp_transactional.Client(
        api_key=settings.MAILCHIMP_TRANSACTIONAL_API_KEY,
    )
    message = {
        'from_email': 'test@ingi9786.com',
        'subject': 'Testing sending email',
        'text': 'Hi, this is my first email via Mailchimp Transcational API',
        'to': [
            {
                'email': 'admin@ingi9786.com',
                'type': 'to'
            },
        ]
    }
    # try:
    response = mailchimp.messages.send({
        'message': message
    })
    return 'HI'
        # return JsonResponse({
        #     'detail': 'sending email success',
        #     'response': response,
        # })
    # except ApiClientError as error:
    #     return JsonResponse({
    #         'detail': 'sending eamil fail',
    #         'error': error.text,
    #     })
