# %% [markdown]
# # Proyecto de Análisis de Datos

# %% [markdown]
# ## Importaciones

# %%
import numpy as np
import pandas as pd
from unidecode import unidecode
import matplotlib.pyplot as plt

# %% [markdown]
# ## Lectura

# %%
#Lectura de datos
df_init_soil = pd.read_csv('https://raw.githubusercontent.com/LotusZaheer/Soil-data-analysis/main/Data/Resultados_de_An_lisis_de_Laboratorio_Suelos_en_Colombia.csv', low_memory=False)

# %% [markdown]
# ### Funciones de limpieza

# %%
def unique_values_count(df):
    # Obtener los valores únicos para cada columna
    unique_values = df.apply(pd.Series.unique)

    # Crear una lista para almacenar los resultados
    results = []

    # Iterar sobre las columnas y contar los valores únicos
    for columna, valores in unique_values.items():
        num_unique_values = len(valores)
        results.append({'Column Name': columna, 'Unique Values Count': num_unique_values})

    # Crear un DataFrame a partir de la lista de resultados
    results_df = pd.DataFrame(results)

    return results_df

# Función para convertir cadenas de texto a minúsculas sin acentos
def convert_to_lowercase_without_accents(valor):
    if isinstance(valor, str):  # Verificar si el valor es una cadena de texto
        # Convertir a minúsculas y quitar acentos
        return unidecode(valor).lower()
    return valor  # Mantener otros tipos de datos sin cambios

# Función para limitar los números a 6 cifras significativas
def limit_to_six_digits(valor):
    if isinstance(valor, (int, float)):  # Verificar si el valor es numérico
        return round(valor, 6)           # Redondear a 6 cifras significativas
    return valor                         # Mantener otros tipos de datos sin cambios

def limpieza_y_conversion(columna):
    """Función que facilita la limpieza y manejo de 
    columnas numéricas que contienen (, en vez de punto en algunos valores)
    y el signo < haciendo referencia a valores menores a cero"""
    
    columna = columna.str.replace(',', '.')
    columna = columna.apply(lambda x: -float(x.replace('<', '').strip()) if '<' in x else float(x))
    return pd.to_numeric(columna, errors='coerce')



# %%
 #Revisión general de los datos
df_init_soil

# %%
print('Columnas:')
print(df_init_soil.columns)

# %%
count1 = unique_values_count(df_init_soil)
count1

# %%
print(df_init_soil.shape)

# %%
# Eliminamos las columnas sin información
df_without_nan = df_init_soil.dropna(axis=1, how='all')
print(df_without_nan.shape)

# %%
# Mostrar los tipos de datos de cada columna
print("Tipos de datos de cada columna:")
print(df_without_nan.dtypes)

# %%
# Aplicar las funciones a cada elemento del DataFrame
df_in_lower = df_without_nan.applymap(convert_to_lowercase_without_accents)
df_processed = df_in_lower.applymap(limit_to_six_digits)
count2 = unique_values_count(df_processed)
count2

# %%
merged_df = pd.merge(count1, count2, on='Column Name', suffixes=('_count1', '_count2'))

# Realiza la resta entre las columnas 'Unique Values Count' de count1 y count2
merged_df['Difference'] = merged_df['Unique Values Count_count1'] - merged_df['Unique Values Count_count2']

# Selecciona solo las columnas necesarias en el DataFrame resultante
df_review = merged_df[['Column Name', 'Difference']]
df_review


# %%
valores_unicos = df_processed.apply(pd.Series.unique)
for row, val in valores_unicos.items():
    print(f"Valores unicos en la columna {row}")
    print(val)
    print('------------------------------------')
# df_processed.to_csv('df_processed.csv', index=False)

# %%
data_processed = df_processed.copy()
print(data_processed.info())

# %%
# Visualización de columnas numéricas
valores = data_processed.iloc[:, 9:]
valores

# %% [markdown]
# ### Limpieza de columnas numéricas
# 

# %%
# Corregir las columnas con valores extraños para poder convertir a float
columns_to_numeric = valores.columns.tolist()


# %% [markdown]
# ### Se convierten las columnas a los tipos de datos pertinentes
# 
# - Se pierden algunas filas en la conversión debido a valores con símbolos como < o valores nulos en todas las columnas.
# - Se agrega el ID.

# %%
data_processed = data_processed.astype(str).assign(**{col: pd.to_numeric(data_processed[col], errors='coerce') for col in columns_to_numeric})
data_processed

# %% [markdown]
# # Exploración de datos y análisis
# 

# %% [markdown]
# ## Análisis por Ubicación Geográfica y Tipo de Cultivo

# %% [markdown]
# ### Se filtran los datos por departamento y municipio
# 
# * Se calcula el top 30 por cultivos en Cundinamarca, Boyacá y Bogotá.
# * De igual modo, el top 10 por cultivos en cada uno de los departamentos seleccionados: Cundinamarca, Boyacá y Bogotá.
# 

# %%
departamentos = ['cundinamarca', 'boyaca', 'bogota, d.c.']
datos_filtrados = data_processed[data_processed['Departamento'].isin(departamentos)]


cultivo_ubicaicon = datos_filtrados.groupby(['Departamento', 'Municipio','Cultivo'])['Cultivo'].count().reset_index(name='Count')
cultivo_ubicaicon.sort_values(by=['Count', 'Departamento'], ascending=[False, False], inplace=True)
top_30_cultivos = cultivo_ubicaicon.head(30)
top_30_cultivos

# %% [markdown]
# ### Cultivos más comunes

# %%
cultivos_mas_comunes = datos_filtrados.groupby('Cultivo')['Cultivo'].count().reset_index(name='Count')
cultivos_mas_comunes = cultivos_mas_comunes.sort_values(by='Count', ascending=False).head(10)
cultivos_mas_comunes 

# %% [markdown]
# ### Cultivos más comunes en Cundinamarca

# %%
conteo_departamento = datos_filtrados.groupby('Departamento')['Cultivo'].count().reset_index(name='Count')
conteo_departamento

# %%
cultivos_mas_comunes_cundinamarca1 = datos_filtrados[datos_filtrados['Departamento'].isin(['cundinamarca']) & ~datos_filtrados['Municipio'].isin(['bogota, d.c.'])]

cultivos_mas_comunes_cundinamarca = cultivos_mas_comunes_cundinamarca1.groupby(['Cultivo'])['Cultivo'].count().reset_index(name='Count')
cultivos_mas_comunes_cundinamarca = cultivos_mas_comunes_cundinamarca.sort_values(by='Count', ascending=False).head(10)
print(f'Cultivos mas comunes en cundinamarca \n*','--'*20,'\n',cultivos_mas_comunes_cundinamarca)

# %% [markdown]
# ### Cultivos más comunes en Bogotá

# %%
prueba = cultivos_mas_comunes_cundinamarca1.groupby(['Cultivo'])['Cultivo'].count().reset_index(name='Count')
prueba = prueba.sort_values(by='Count', ascending=False).head(10)
prueba

# %%
cultivos_mas_comunes_bogota = datos_filtrados[datos_filtrados['Departamento'].isin(['bogota, d.c.']) | datos_filtrados['Municipio'].isin(['bogota,  d.c.'])]
cultivos_mas_comunes_bogota = cultivos_mas_comunes_bogota.groupby(['Cultivo'])['Cultivo'].count().reset_index(name='Count')
cultivos_mas_comunes_bogota = cultivos_mas_comunes_bogota.sort_values(by='Count', ascending=False).head(10)
print(f'Cultivos mas comunes en Bogota \n*','--'*20,'\n',cultivos_mas_comunes_bogota)

# %%
cultivos_mas_comunes_boyaca = datos_filtrados[datos_filtrados['Departamento'].isin(['boyaca'])]
cultivos_mas_comunes_boyaca = cultivos_mas_comunes_boyaca.groupby(['Cultivo'])['Cultivo'].count().reset_index(name='Count')
cultivos_mas_comunes_boyaca = cultivos_mas_comunes_boyaca.sort_values(by='Count', ascending=False).head(10)
print(f'Cultivos mas comunes en Boyaca \n*','--'*20,'\n',cultivos_mas_comunes_boyaca)


# %% [markdown]
# 

# %%
fig, axs = plt.subplots(4, 1, figsize=(12, 18))

# Gráfico de barras para Cundinamarca
axs[0].barh(cultivos_mas_comunes_cundinamarca['Cultivo'], cultivos_mas_comunes_cundinamarca['Count'], color='skyblue')
axs[0].set_xlabel('Count')
axs[0].set_ylabel('Cultivo')
axs[0].set_title('Cantidad de cada cultivo en Cundinamarca')
axs[0].invert_yaxis()  # Invertir el eje y para que el cultivo con mayor count esté arriba
axs[0].grid(True)

# Gráfico de barras para Bogotá
axs[1].barh(cultivos_mas_comunes_bogota['Cultivo'], cultivos_mas_comunes_bogota['Count'], color='lightgreen')
axs[1].set_xlabel('Count')
axs[1].set_ylabel('Cultivo')
axs[1].set_title('Cantidad de cada cultivo en Bogotá')
axs[1].invert_yaxis()
axs[1].grid(True)

# Gráfico de barras para Boyacá
axs[2].barh(cultivos_mas_comunes_boyaca['Cultivo'], cultivos_mas_comunes_boyaca['Count'], color='salmon')
axs[2].set_xlabel('Count')
axs[2].set_ylabel('Cultivo')
axs[2].set_title('Cantidad de cada cultivo en Boyacá')
axs[2].invert_yaxis()
axs[2].grid(True)

# Gráfico de pastel para el conteo de departamentos
axs[3].pie(conteo_departamento['Count'], labels=conteo_departamento['Departamento'], autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'salmon'])
axs[3].set_title('Distribución de cultivos por departamento')

# Ajustar el layout para evitar superposición
plt.tight_layout()

# Mostrar la figura con los cuatro gráficos
plt.show()

# %% [markdown]
# # Análisis de salud del suelo por top 10 cultivos teniendo en cuenta la relación entre:
# 

# %% [markdown]
# 
# * pH agua:suelo 2,5:1,0 
# * Materia orgánica (MO) %
# * Capacidad de intercambio catiónico (CICE) suma de bases cmol(+)/kg

# %%
valores = ['Municipio','Cultivo','pH agua:suelo 2,5:1,0', 'Materia orgánica (MO) %', 'capacidad de intercambio cationico (CICE) suma de bases cmol(+)/kg']
salud_del_suelo_cun = datos_filtrados[datos_filtrados['Departamento'].isin(['cundinamarca'])]
salud_del_suelo_cun = salud_del_suelo_cun.loc[:, valores]
salud_del_suelo_cun = salud_del_suelo_cun.groupby(['Cultivo'])[valores[2:]].mean()
salud_del_suelo_cun['count'] = cultivos_mas_comunes_cundinamarca1.groupby(['Cultivo']).size()
# salud_del_suelo_cun = salud_del_suelo_cun.sort_values(by=valores[2:], ascending=True)
salud_del_suelo_cun = salud_del_suelo_cun.sort_values(by='count', ascending=False).reset_index()
salud_del_suelo_cun_10 = salud_del_suelo_cun.head(10)
salud_del_suelo_cun

# %%
correlacion =  salud_del_suelo_cun_10.drop(columns=['Cultivo', 'count'])
correlacion = correlacion.corr()

plt.figure(figsize=(10, 14))
plt.imshow(correlacion, cmap='coolwarm', interpolation='nearest')
plt.colorbar()
plt.title('Matriz de Correlación')
plt.xticks(range(len(correlacion.columns)), correlacion.columns, rotation=65)
plt.yticks(range(len(correlacion)), correlacion.columns)
plt.show()

# %%
salud_del_suelo_cun.describe()

# %%



