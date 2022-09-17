from django.urls import path
from . import views

urlpatterns = [
    path('', views.Routine_list_create_view, name='routine_list_create'),
    path('<int:pk>', views.Routine_update_view, name='routine_update'),
]