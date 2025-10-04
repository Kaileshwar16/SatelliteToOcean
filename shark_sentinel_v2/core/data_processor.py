import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.windows import from_bounds

def process_ocean_data(file_path, bounds):
    """
    Reads a geospatial data file, crops it to the given bounds, 
    calculates a metric, and generates a heatmap.
    """
    with rasterio.open(f'netcdf:{file_path}:chlor_a') as src:
        
        # --- THIS IS THE CORRECTED CODE ---
        # Convert geographic bounds to a pixel window using the correct keywords.
        window = from_bounds(
            left=bounds['west'],
            bottom=bounds['south'],
            right=bounds['east'],
            top=bounds['north'],
            transform=src.transform
        )
        
        # Read only the data from within that window
        data = src.read(1, window=window)

        # The image bounds are now the user's selection
        image_bounds = [[bounds['north'], bounds['west']], [bounds['south'], bounds['east']]]
        
        # Process the cropped data
        data[data < 0] = 0
        if data[data > 0].size == 0:
            avg_value = 0
        else:
            avg_value = np.mean(data[data > 0])
        
        # Generate the image
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(data, cmap='viridis')
        ax.axis('off')
        
        output_image_path = 'core/static/core/heatmap.png'
        fig.savefig(output_image_path, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig)

        return output_image_path, avg_value, image_bounds
