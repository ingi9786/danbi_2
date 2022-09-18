from django.urls import path
from . import views

urlpatterns = [
    path('', views.Routine_list_create_view, name='routine_list_create'),
    path('<int:pk>', views.Routine_detail_view, name='routine_detail'),
    path('deleted', views.Deleted_routine_list_view, name='deleted_routine_list'),
    path('date/', views.Dated_Routine_list_view, name='dated_routine_list'),
]