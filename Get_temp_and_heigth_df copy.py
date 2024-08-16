import osmnx as ox
import requests
import pandas as pd
from tqdm import tqdm

# Función para obtener altitud usando Open Elevation API
def get_altitude(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['results']
        return results[0]['elevation']
    else:
        return None

# Función para obtener datos meteorológicos usando Open-Meteo API
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=America/Bogota"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        daily = results['daily']
        return {
            'temperature_max': daily['temperature_2m_max'][0],
            'temperature_min': daily['temperature_2m_min'][0]
        }
    else:
        return None


def get_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        return results['current_weather']['temperature']
    else:
        return None

# Función para obtener altitudes y temperaturas para los municipios
def get_data_for_municipalities(municipios):
    data = []

    for municipio in tqdm(municipios, desc="Procesando municipios", unit="municipio"):

        try:
            # Obtener coordenadas desde OSM
            gdf = ox.geocode_to_gdf(municipio + ", Colombia")
            lat, lon = gdf.geometry[0].centroid.y, gdf.geometry[0].centroid.x

            # Obtener altitud desde Open Elevation API
            altitud = get_altitude(lat, lon)

            # Obtener datos meteorológicos desde Open-Meteo API
            weather = get_weather(lat, lon)
            if weather:
                temperatura_max = weather['temperature_max']
                temperatura_min = weather['temperature_min']
            else:
                temperatura_max = None
                temperatura_min = None

            temperatura = get_temperature(lat, lon)

            data.append({
                'Municipio': municipio,
                'Altitud': altitud,
                'Temp_Max': temperatura_max,
                'Temp_Min': temperatura_min,
                'Temp_Mean': temperatura,
            })

            print(f"{municipio}: Altitud {altitud} metros, Temp Max {temperatura_max} °C, Temp Min {temperatura_min} °C")
        except Exception as e:
            print(f"Error al obtener datos para {municipio}: {e}")

    return pd.DataFrame(data)

# Lista de municipios de Cundinamarca
municipios = ['funza', 'bituima', 'villapinzon', 'bogota,  d.c.', 'tuta', 'la vega', 'villeta', 'garagoa', 'chia', 'chita', 'socota', 'maripi', 'nocaima', 'duitama', 'cachipay', 'guaduas', 'carmen de carupa', 'une', 'lenguazaque', 'san cayetano', 'cogua', 'choconta', 'la calera', 'villa de san diego de ubate', 'tenjo', 'tausa', 'bojaca', 'viota', 'gacheta', 'el espino', 'viani', 'samaca', 'la uvita', 'cienega', 'ramiriqui', 'el colegio', 'medina', 'tibana', 'cota', 
              'caqueza', 'ventaquemada', 'tabio', 'choachi', 'sasaima', 'guayabetal', 'ubala', 'tibirita', 'la palma', 'mosquera', 'tibacuy', 'manta', 'san juan de rioseco', 'sotaquira', 'chaguani', 'fusagasuga', 'pasca', 'chipaque', 'facatativa', 'la pena', 'tibasosa', 'toca', 'turmeque', 'paime', 'tocaima', 'sogamoso', 'pachavita', 'aquitania', 'anapoima', 'santa rosa', 'guacheta', 'nobsa', 'puerto salgar', 'puerto boyaca', 'quipile', 'raquira', 'gachala', 'subachoque',
                'guatavita', 'venecia', 'quebradanegra', 'sibate', 'fuquene', 'pandi', 'apulo', 'chiquinquira', 'umbita', 'arcabuco', 'caparrapi', 'anolaima', 'macanal', 'la mesa', 'san francisco', 'quipama', 'sesquile', 'guayabal de siquima', 'mongui', 'macheta', 'gama', 'motavita', 'ricaurte', 'san miguel de sema', 'pacho', 'chitaraque', 'soata', 'suesca', 'granada', 'beltran', 'nemocon', 'alban', 'san bernardo', 'junin', 'san pablo de borbur', 'saboya', 'fomeque', 
                'supata', 'jerusalen', 'villagomez', 'arbelaez', 'guasca', 'san luis de gaceno', 'san antonio del tequendama', 'simijaca', 'sutamarchan', 'zipaquira', 'gameza', 'cubara', 'moniquira', 'el rosal', 'silvania', 'belen', 'santa rosa de viterbo', 'pauna', 'puli', 'tocancipa', 'paratebueno', 'zetaquira', 'cucunuba', 'guateque', 'yacopi', 'gutierrez', 'oicata', 'combita', 'la esperanza', 'cabrera', 'gachancipa', 'miraflores', 'paipa', 'cajica', 'san jose de pare', 
                'topaipi', 'firavitoba', 'soraca', 'el cocuy', 'sutatenza', 'soacha', 'narino', 'agua de dios', 'tipacoque', 'tota', 'boyaca', 'muzo', 'nilo', 'ubaque', 'utica', 'susa', 'tunja', 'sopo', 'madrid', 'el penon', 'tena', 'zipacon', 'vergara', 'santa sofia', 'santana', 'coper', 'paez', 'boavita', 'jerico', 'otanche', 'pesca', 'nimaima', 'sativanorte', 'siachoque', 'buenavista', 'carmen de apicala', 'almeida', 'corrales', 'paya', 'guataqui', 'jenesano', 
                'tenza', 'tinjaca', 'la capilla', 'guayata', 'paz de rio', 'caldas', 'san antonio', 'san miguel', 'pajarito', 'gachantiva', 'san eduardo', 'togui', 'berbeo', 'chinavita', 'beteitiva', 'san fernando', 'nuevo colon', 'cerinza', 'san juan nepomuceno', 'quetame', 'girardot', 'susacon', 'sachica', 'campohermoso', 'briceno', 'borrar', 'tunungua', 'cuitiva', 'espinal', 'tuquerres', 'fosca', 'san mateo', 'sora', 'el retorno', 'sutatausa', 'tutaza', 
                'la victoria', 'pisba', 'iza', 'floresta', 'chiquiza', 'villa de leyva', 'santa ana', 'andalucia', 'la sierra', 'covarachia']

# Obtener datos para los municipios de Cundinamarca
df_data = get_data_for_municipalities(municipios)

# Guardar el DataFrame de datos en un nuevo archivo CSV
df_data.to_csv('temp_and_heigth_df.csv', index=False)

print(df_data.head())
