from pathlib import Path
import rasterio
from rasterio.merge import merge

input_dir = Path("data/raw/dem/srtm_rs")

output_path = Path("data/processed/dem/dem_rs_mosaic.tif")
output_path.parent.mkdir(parents=True, exist_ok=True)

rasters = []
for tif in input_dir.glob("*.tif"):
    rasters.append(rasterio.open(tif))

mosaic, transform = merge(rasters)

meta = rasters[0].meta.copy()

meta.update({
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": transform
})

with rasterio.open(output_path, "w", **meta) as dest:
    dest.write(mosaic)

for r in rasters:
    r.close()

print("Mosaico criado com sucesso:", output_path)
