from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('add/', views.add_task, name='AddTask'), 
    path('remove/<int:_id>/', views.remove_task, name='RemoveTask'),
    path('edit/<int:_id>', views.edit_task, name='EditTask'), 
    path('update/<int:task_id>/', views.done_task, name='UpdateTask'),
]