# recortar região específica da bacia do Guaíba a partir do DEM mosaico do RS

from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.mask import mask

dem_path = Path("data/processed/dem/dem_rs_mosaic.tif")
bacia_path = Path("data/raw/geoft_bacias_hidrograficas_guaiba.gpkg")
output_path = Path("data/processed/dem/dem_guaiba_clip.tif")

output_path.parent.mkdir(parents=True, exist_ok=True)

bacia = gpd.read_file(bacia_path)

with rasterio.open(dem_path) as src:

    # Garantir CRS igual
    if bacia.crs != src.crs:
        bacia = bacia.to_crs(src.crs)

    # Converter geometria para formato aceito pelo rasterio
    geometries = [geom for geom in bacia.geometry]

    clipped, transform = mask(
        src,
        geometries,
        crop=True,
        nodata=src.nodata
    )

    meta = src.meta.copy()
    meta.update({
        "height": clipped.shape[1],
        "width": clipped.shape[2],
        "transform": transform
    })

with rasterio.open(output_path, "w", **meta) as dest:
    dest.write(clipped)

print("DEM recortado com sucesso:", output_path)
