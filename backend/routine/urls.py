from django.urls import path
from . import views

urlpatterns = [
    path('', views.Routine_list_create_view, name='routine_list_create'),
    path('<int:pk>', views.Routine_detail_view, name='routine_detail'),
    path('deleted', views.Deleted_routine_mixin_view, name='deleted_routine_list_create'),
    path('deleted/<int:pk>', views.Deleted_routine_mixin_view, name='deleted_routine_detail'),
]