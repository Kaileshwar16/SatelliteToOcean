from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .data_processor import process_ocean_data
from django.conf import settings

def index(request):
    return render(request, 'core/index.html')

class OceanDataView(APIView):
    def get(self, request, *args, **kwargs):
        filename = 'AQUA_MODIS.20250831.L3m.DAY.CHL.chlor_a.4km.nc'
        file_path = settings.BASE_DIR / 'core' / 'data' / filename
        try:
            image_path, avg_value, bounds = process_ocean_data(file_path)
            if avg_value > 0.5:
                probability = "High"
                message = f"High chlorophyll levels (avg: {avg_value:.2f} mg/m³) suggest a rich food web."
            else:
                probability = "Low"
                message = f"Lower chlorophyll levels (avg: {avg_value:.2f} mg/m³) suggest less activity."
            response_data = {
                'heatmap_url': '/static/core/heatmap.png',
                'image_bounds': bounds,
                'shark_probability': probability,
                'analysis': message,
            }
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
