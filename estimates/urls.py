from django.urls import path
from .views import EstimateListView, EstimateCreateView, accept_estimate_view


urlpatterns = [
    path('', EstimateListView.as_view(), name='estimate-list'),
    path('create/', EstimateCreateView.as_view(), name='estimate-create'),
    path('<int:pk>/accept/', accept_estimate_view, name='estimate-accept'),
]
