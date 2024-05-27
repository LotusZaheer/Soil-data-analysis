import pandas as pd

#df_init_soil = pd.read_csv('https://raw.githubusercontent.com/LotusZaheer/Soil-data-analysis/main/Data/Resultados_de_An_lisis_de_Laboratorio_Suelos_en_Colombia.csv')
df_init_soil = pd.read_csv('df_processed.csv')


valores_unicos = df_init_soil.apply(pd.Series.unique)

for row, val in valores_unicos.items():
    print(f"Valores unicos en la columna {row}")
    print(val)
    print('------------------------------------')