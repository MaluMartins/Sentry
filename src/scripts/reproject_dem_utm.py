# reprojetar dem para utm 22s (coordenadas em metros, melhor para trabalhar no mesa)

from pathlib import Path
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

input_path = Path("data/processed/dem/dem_guaiba_clip.tif")
output_path = Path("data/processed/dem/dem_guaiba_utm22s.tif")

output_path.parent.mkdir(parents=True, exist_ok=True)

dst_crs = "EPSG:32722"  # UTM Zona 22 Sul

with rasterio.open(input_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs,
        dst_crs,
        src.width,
        src.height,
        *src.bounds
    )

    meta = src.meta.copy()
    meta.update({
        "crs": dst_crs,
        "transform": transform,
        "width": width,
        "height": height
    })

    with rasterio.open(output_path, "w", **meta) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )

print("DEM reprojetado para UTM 22S:", output_path)
