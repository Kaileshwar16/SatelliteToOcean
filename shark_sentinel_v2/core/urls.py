from django.urls import path
from .views import index, OceanDataView

urlpatterns = [
    path('', index, name='index'),
    path('api/ocean-data/', OceanDataView.as_view(), name='ocean-data'),
]
