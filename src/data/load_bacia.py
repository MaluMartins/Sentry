import geopandas as gpd

bacias = gpd.read_file("../../data/geoft_bacias_hidrograficas_guaiba.gpkg")

gpd.list_layers("arquivo.gpkg")
bacia_guaiba = bacias[bacias["id"] == "1"]

poligono_bacia = bacia_guaiba.geometry.iloc[0]

