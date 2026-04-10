from django.urls import path
from .views import JobListView, update_job_status


urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('<int:pk>/status/', update_job_status, name='job-status-update'),
]
