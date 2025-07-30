
from django.urls import path
from . import views

urlpatterns = [
    # Task results
    path('results/', views.TaskResultListView.as_view(), name='task-results'),
    path('results/<str:task_id>/', views.TaskResultDetailView.as_view(), name='task-result-detail'),
    
    # Email tasks
    path('emails/', views.EmailTaskListCreateView.as_view(), name='email-tasks'),
    
    # Task operations
    path('start-long-task/', views.start_long_task, name='start-long-task'),
    path('add/', views.add_task, name='add-task'),
    path('multiply/', views.multiply_task, name='multiply-task'),
    path('send-email/', views.send_email, name='send-email'),
    path('process-data/', views.process_data, name='process-data'),
    
    # Task management
    path('status/<str:task_id>/', views.task_status, name='task-status'),
    path('cancel/<str:task_id>/', views.cancel_task, name='cancel-task'),
    path('celery-status/', views.celery_status, name='celery-status'),
]