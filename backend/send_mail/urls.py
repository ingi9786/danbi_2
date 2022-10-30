from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.mailchimp_transactional_ping_view, name='ping'),
    path('send/', views.send_mail, name='mailchimp-send'),
    path('test/', views.test),
]   
