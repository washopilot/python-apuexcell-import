import time

import pandas as pd

from helpers import clean_and_sort_dataframe, process_sheet

tcpu0 = time.time()

excel_file = 'original.xlsx'

_sheet_names = pd.ExcelFile(excel_file).sheet_names

df_dict_sheets = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None)


df_materials = pd.DataFrame()

for df_name, df_sheet in df_dict_sheets.items():
    _df_temp_process = process_sheet(df_sheet, labels=[
        'MATERIALES', 'TRANSPORTE'])
    # print(_df_temp_process.columns)
    df_materials = pd.concat(
        [_df_temp_process[['DESCRIPCIÓN', 'UNIDAD', 'P. UNITARIO']], df_materials], axis=0)

df_clean_equipment = clean_and_sort_dataframe(df_materials, start_index=1)


df_Sheet_1 = process_sheet(df_dict_sheets['1'], labels=[
                           'MATERIALES', 'TRANSPORTE'])

print(df_clean_equipment)
print()
print(df_Sheet_1)
print()

column_names_C = ['CODIGO', 'CANTIDAD']
dfC = pd.DataFrame(columns=column_names_C)

# Iterar sobre las filas de dfA
for index_A, row_A in df_Sheet_1.iterrows():
    # Verificar si la fila de dfA está incluida en alguna fila de dfB
    matching_rows = df_clean_equipment[df_clean_equipment.apply(lambda row_B: row_B.isin(row_A).all(), axis=1)]
    
    if not matching_rows.empty:
        # Tomar el índice de la primera coincidencia
        index_B = matching_rows.index[0]
    else:
        # Si no hay coincidencias, asignar None
        index_B = None

    # Obtener los valores de las columnas especificadas en column_names_C en dfA
    values_C = [row_A[column] for column in column_names_C[1:]]

    # Concatenar el resultado a dfC
    dfC = pd.concat([dfC, pd.DataFrame([[index_B] + values_C], columns=column_names_C)], ignore_index=True)

print(dfC)
print()
print(df_clean_equipment.loc[109])


print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
