from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .data_processor import process_ocean_data
from django.conf import settings

def index(request):
    return render(request, 'core/index.html')

# in core/views.py

class OceanDataView(APIView):
    def get(self, request, *args, **kwargs):
        print("\n--- NEW REQUEST RECEIVED ---")
        try:
            # Step 1: Get the raw string parameters from the URL
            north_str = request.GET.get('north')
            south_str = request.GET.get('south')
            east_str = request.GET.get('east')
            west_str = request.GET.get('west')
            print(f"1. Received params: N={north_str}, S={south_str}, E={east_str}, W={west_str}")

            # Step 2: Convert to float
            north = float(north_str)
            south = float(south_str)
            east = float(east_str)
            west = float(west_str)
            print("2. Successfully converted all params to float.")

            # Step 3: Prepare to call the data processor
            bounds = {'north': north, 'south': south, 'east': east, 'west': west}
            filename = 'AQUA_MODIS.20250831.L3m.DAY.CHL.chlor_a.4km.nc' # Make sure your file is named data.nc
            file_path = settings.BASE_DIR / 'core' / 'data' / filename
            print(f"3. Calling data processor for file: {file_path}")

            # Step 4: Call the data processor
            image_path, avg_value, image_bounds = process_ocean_data(file_path, bounds)
            print("4. Data processor finished successfully.")

            # ... the rest of the code is the same ...
            if avg_value > 0.5:
                probability = "High"
                message = f"High chlorophyll levels (avg: {avg_value:.2f} mg/m³) suggest a rich food web."
            else:
                probability = "Low"
                message = f"Lower chlorophyll levels (avg: {avg_value:.2f} mg/m³) suggest less activity."

            response_data = {
                'heatmap_url': '/static/core/heatmap.png',
                'image_bounds': image_bounds,
                'shark_probability': probability,
                'analysis': message,
            }
            return Response(response_data)
            
        except TypeError as e:
            print(f"!!! A TypeError occurred: {e}")
            return Response({'error': 'A TypeError occurred. Check terminal for details.'}, status=400)
        except Exception as e:
            print(f"!!! An unexpected error occurred: {e}")
            return Response({'error': str(e)}, status=500)
