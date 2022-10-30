from django.shortcuts import HttpResponse
from .tasks import test_func, ping_task, send_email_to_subscriber
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
def test(request):
    test_func.delay()
    return JsonResponse({'hi':'hi'})

def mailchimp_transactional_ping_view(request):
    ping_task.delay()
    return JsonResponse({"state":"hi"})
        
def send_mail(request):
    send_email_to_subscriber.delay()
    return JsonResponse({"status":'hi'})
        
# mandrill에 인증된 도메인으로만 메일을 보낼수 있다. ingi9786.com > ingi9786.com은 reject_reason: null로 뜨네
# {"detail": "sending email success", "response": [{"email": "test@ingi9786.com", "status": "sent", "_id": "022f4e693d8c4f49a2a62499db794cf9", "reject_reason": null}]}