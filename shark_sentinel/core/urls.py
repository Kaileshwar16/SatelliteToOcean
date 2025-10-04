# core/urls.py

from django.urls import path
from .views import index, OceanDataView, test_view # <-- ADD test_view HERE

urlpatterns = [
    path('', index, name='index'),
    path('api/ocean-data/', OceanDataView.as_view(), name='ocean-data'),
    
    # vvv ADD THIS NEW URL PATTERN AT THE END vvv
    path('test/', test_view, name='test-view'),
]
