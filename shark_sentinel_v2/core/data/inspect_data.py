# inspect_data.py
import netCDF4
import os

# Get the full path to the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join('AQUA_MODIS.20250831.L3m.DAY.CHL.chlor_a.4km.nc')

try:
    print(f"--- Inspecting file at: {file_path} ---")
    dataset = netCDF4.Dataset(file_path, 'r')
    
    print("\nFound the following variables inside the file:")
    for var_name in dataset.variables.keys():
        print(f"- {var_name}")
        
    dataset.close()
    print("\n--- Inspection complete ---")

except FileNotFoundError:
    print(f"\nERROR: Could not find the file at {file_path}. Make sure it exists.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
