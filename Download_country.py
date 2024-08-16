

import geopandas as gpd
import pycountry
import osmnx as ox
from warnings import warn
import pandas as pd
import time


import geopandas as gpd
import folium
from folium.plugins import MarkerCluster


def get_country_states(country):
    print('Country')
    print(country)
    try:
        country_code = pycountry.countries.search_fuzzy(country)[0].alpha_2
        states = pycountry.subdivisions.get(country_code=country_code)
        states_info = [(state.code, state.name, state.type) for state in states]
        return states_info
    except LookupError:
        return None


def graph_from_place(query, which_result=None, buffer_dist=None):
    if buffer_dist is not None:
        warn(
            "The buffer_dist argument has been deprecated and will be removed "
            "in the v2.0.0 release. Buffer your query area directly, if desired. "
            "See the OSMnx v2 migration guide: https://github.com/gboeing/osmnx/issues/1123",
            FutureWarning,
            stacklevel=2,
        )

    if isinstance(query, (str, dict)):
        gdf_place = ox.geocode_to_gdf(
            query, which_result=which_result, buffer_dist=buffer_dist
        )
    elif isinstance(query, list):
        gdf_place = ox.geocode_to_gdf(query, buffer_dist=buffer_dist)
    else:
        msg = "query must be dict, string, or list of strings"
        raise TypeError(msg)

    polygon = gdf_place["geometry"].unary_union
    return polygon


def plot_geometries_from_dataset(pais, df):

    m = folium.Map()

    for idx, row in df.iterrows():
        folium.GeoJson(
            row['geometry'], 
            name=row['state'], 
            style_function=lambda x: {'fillColor': 'blue'},
            popup=folium.Popup(row['state'], parse_html=True)
        ).add_to(m)

    m.save(f'./{pais}_estados.html')


def main(pais):

    estados_info = get_country_states(pais)

    if estados_info:
        geometrias_estados = []

        """"""
        for estado in estados_info:
            estado_actual = estado[0]
            geometria_estado = graph_from_place(f"{estado_actual}")
            geometrias_estados.append(geometria_estado)

            print(f"Procesando {estado_actual}")
        """"""

        """
        from tqdm import tqdm
        pbar = tqdm(estados_info, desc="Procesando estados")
        for estado in pbar:
            estado_actual = estado[0]
            geometria_estado = graph_from_place(f"{estado_actual}")
            geometrias_estados.append(geometria_estado)
            pbar.set_description(f"Procesando {estado_actual}")
        """

        nombres_estados = [estado[1] for estado in estados_info]
        df = pd.DataFrame({
            "state": nombres_estados,
            "geometry": geometrias_estados
        })

        gdf = gpd.GeoDataFrame(df, geometry='geometry')

        plot_geometries_from_dataset(pais, gdf)

        gdf.to_csv(f"{pais}_estados.csv", index=False)
        print(gdf)

        print("Dataset generado exitosamente.")
    else:
        print(f"No se encontraron estados para el país {pais}")


if __name__ == "__main__":
    main('Colombia')
