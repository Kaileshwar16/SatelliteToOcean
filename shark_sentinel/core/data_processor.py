# core/data_processor.py

import rasterio
import numpy as np
import matplotlib.pyplot as plt

def process_ocean_data(file_path):
    """
    Reads a geospatial data file (like .nc or .tif), calculates a simple
    metric, and generates a transparent heatmap PNG for map overlay.
    """
    
    with rasterio.open(f'netcdf:{file_path}') as src:

        # Read the data from the first band of the file
        # The data variable is now a 2D array of chlorophyll values
        data = src.read(1)

        # Get the geographic boundaries (latitude/longitude) of the data
        bounds = src.bounds

        # Clean the data: NASA uses large negative numbers for "no data" (e.g., land, clouds)
        # We replace them with 0 so they don't skew our calculations.
        data[data < 0] = 0
        
        # Calculate a simple metric: the average chlorophyll value for the area
        # We only average the pixels that actually have data (> 0).
        avg_value = np.mean(data[data > 0])
        
        # --- Image Generation ---
        fig, ax = plt.subplots(figsize=(10, 10))
        # Use a colormap to draw the data. 'viridis' is great for scientific data.
        ax.imshow(data, cmap='viridis', extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])
        # Hide the white border and axes for a clean overlay on the map
        ax.axis('off')
        
        # Define where to save the image. We overwrite it each time for simplicity.
        output_image_path = 'core/static/core/heatmap.png'
        # Save the figure with a transparent background
        fig.savefig(output_image_path, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig) # Close the figure to save memory

        # Define the corner coordinates for the Leaflet map overlay
        image_bounds = [[bounds.top, bounds.left], [bounds.bottom, bounds.right]]
        
        # Return everything the API view will need
        return output_image_path, avg_value, image_bounds
