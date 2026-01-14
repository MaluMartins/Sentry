# ajustar resolução do DEM de 30m para 150m (melhor para trabalhar com células no modelo)

from pathlib import Path
import rasterio
from rasterio.enums import Resampling

input_path = Path("data/processed/dem/dem_guaiba_utm22s.tif")
output_path = Path("data/processed/dem/dem_guaiba_150m.tif")

scale_factor = 5.4  # ~27m -> 150m

with rasterio.open(input_path) as src:
    new_width = src.width // scale_factor
    new_height = src.height // scale_factor

    data = src.read(
        out_shape=(
            src.count,
            int(new_height),
            int(new_width)
        ),
        resampling=Resampling.average
    )

    transform = src.transform * src.transform.scale(
        src.width / new_width,
        src.height / new_height
    )

    meta = src.meta.copy()
    meta.update({
        "height": new_height,
        "width": new_width,
        "transform": transform
    })

with rasterio.open(output_path, "w", **meta) as dst:
    dst.write(data)

print("DEM reamostrado para 150m:", output_path)
