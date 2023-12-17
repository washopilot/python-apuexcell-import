import time

import pandas as pd

tcpu0 = time.time()

excel_file = 'original.xlsx'
_sheet_names = pd.ExcelFile(excel_file).sheet_names
df_dict = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None)


print(_sheet_names)
print(df_dict['1'])

df = df_dict['1']
# Buscar los índices de las filas 'EQUIPOS' y 'MANO DE OBRA'
indices_etiquetas = df[df[1].isin(
    ['EQUIPOS', 'MANO DE OBRA'])].index

# Verificar si se encontraron ambas etiquetas
if len(indices_etiquetas) == 2:
    # Crear un subconjunto del DataFrame desde 'EQUIPOS' hasta 'MANO DE OBRA'
    subconjunto_df = df.loc[indices_etiquetas[0] +
                            1: indices_etiquetas[1]-2].copy()

# Eliminar filas y columnas completamente llenas de NaN
    subconjunto_df = subconjunto_df.dropna(
        axis=0, how='all').dropna(axis=1, how='all')

    # Imprimir el subconjunto resultante
    print()
    print(subconjunto_df)
else:
    print("No se encontraron ambas etiquetas.")

print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
