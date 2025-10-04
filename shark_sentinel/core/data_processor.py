# core/data_processor.py

import rasterio
import numpy as np
import matplotlib.pyplot as plt

def process_ocean_data(file_path):
    # Now that netCDF4 is installed, this more specific command will work.
    with rasterio.open(f'netcdf:{file_path}:chlor_a') as src:
        data = src.read(1)
        
        # We will still use our hardcoded bounds to avoid the georeferencing error.
        image_bounds = [[14.0, 80.0], [10.0, 83.0]]

        # Clean the data
        data[data < 0] = 0
        avg_value = np.mean(data[data > 0])
        
        # --- Image Generation ---
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(data, cmap='viridis')
        ax.axis('off')
        
        output_image_path = 'core/static/core/heatmap.png'
        fig.savefig(output_image_path, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig)

        # Return our hardcoded image_bounds
        return output_image_path, avg_value, image_bounds
