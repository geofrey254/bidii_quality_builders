from django.urls import path
from .views import revenue_chart

urlpatterns = [
    path('', revenue_chart, name='dashboard'),
]
