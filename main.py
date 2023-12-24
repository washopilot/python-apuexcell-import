import time

import pandas as pd

tcpu0 = time.time()


def procesar_sheet(sheet_data, etiquetas=['EQUIPOS', 'MANO DE OBRA']):
    # Buscar los índices de las filas utilizando las etiquetas proporcionadas
    indices_etiquetas = sheet_data[sheet_data[1].isin(etiquetas)].index

    # Verificar si se encontraron ambas etiquetas
    if len(indices_etiquetas) == 2:
        # Crear un subconjunto del DataFrame desde la primera etiqueta hasta la segunda etiqueta
        sheet_data = sheet_data.loc[indices_etiquetas[0] +
                                    1: indices_etiquetas[1] - 2]

        # Eliminar filas y columnas completamente llenas de NaN
        sheet_data = sheet_data.dropna(
            axis=0, how='all').dropna(axis=1, how='all')

        # Tomar la primera fila como encabezados
        nuevos_encabezados = sheet_data.iloc[0]

        # Eliminar la primera fila del DataFrame original
        sheet_data = sheet_data[1:]

        # Asignar los nuevos encabezados al DataFrame original
        sheet_data.columns = nuevos_encabezados

        # Imprimir el subconjunto resultante
        # print("\nSubconjunto resultante:")
        # print(sheet_data)
    else:
        # print(f"No se encontraron ambas etiquetas: {etiquetas}.")
        # sheet_data = pd.DataFrame()
        return None

    sheet_data.columns.name = None
    return sheet_data


excel_file = 'original.xlsx'
_sheet_names = pd.ExcelFile(excel_file).sheet_names
df_dict_sheets = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None)


# print(df_dict_sheets['1'])

_df = df_dict_sheets['1']

_df_procesado = procesar_sheet(_df, etiquetas=['MATERIALES', 'TRANSPORTE'])
print(_df_procesado)

print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
