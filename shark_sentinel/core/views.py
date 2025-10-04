# core/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .data_processor import process_ocean_data
from django.http import JsonResponse
from django.conf import settings
import os

# This view will serve our main HTML page
def index(request):
    return render(request, 'core/index.html')

from django.conf import settings
import os

# This is our API endpoint
class OceanDataView(APIView):
    def get(self, request, *args, **kwargs):
        # --- IMPORTANT ---
        # Replace this with the exact name of the file you downloaded!
        #AQUA_MODIS.20250831.L3m.DAY.CHL.chlor_a.4km.nc

        filename = 'AQUA_MODIS.20250831.L3m.DAY.CHL.chlor_a.4km.nc'
        file_path = os.path.join(settings.BASE_DIR, 'core', 'data', filename)

        try:
            # Call our processor function to do all the work
            image_path, avg_value, bounds = process_ocean_data(file_path)

            # --- Simple Rule-Based "AI" ---
            # This is where you define what different data values mean.
            # You can adjust the threshold (0.5) to what makes sense for your data.
            if avg_value > 0.5:
                probability = "High"
                message = f"High chlorophyll levels (avg: {avg_value:.2f} mg/m³) suggest a rich food web, which can attract sharks."
            else:
                probability = "Low"
                message = f"Lower chlorophyll levels (avg: {avg_value:.2f} mg/m³) suggest less phytoplankton activity."

            # Structure the data for the frontend
            response_data = {
                'heatmap_url': '/static/core/heatmap.png',
                'image_bounds': bounds,
                'shark_probability': probability,
                'analysis': message,
            }
            return Response(response_data)
        
        except FileNotFoundError:
            return Response({'error': f'Data file not found at {file_path}. Did you place it in the core/data folder and update the filename in views.py?'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

def test_view(request):
    return JsonResponse({'status': 'ok'})
