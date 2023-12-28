import time

import pandas as pd

from helpers import (clean_and_sort_dataframe, merge_dataframes,
                     process_sheet_between_tags)

tcpu0 = time.time()

excel_file = 'original.xlsx'

_sheet_names = pd.ExcelFile(excel_file).sheet_names

df_dict_sheets = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None, nrows=65, usecols='B:J')

df_equipment = df_labour = df_materials = pd.DataFrame()

for df_name, df_sheet in df_dict_sheets.items():

    _df_temp = process_sheet_between_tags(df_sheet, labels=[
        'EQUIPOS', 'MANO DE OBRA'])
    df_equipment = pd.concat(
        [_df_temp[['DESCRIPCIÓN', 'TARIFA']], df_equipment], axis=0)

    _df_temp = process_sheet_between_tags(df_sheet, labels=[
        'MANO DE OBRA', 'MATERIALES'])
    df_labour = pd.concat(
        [_df_temp[['DESCRIPCIÓN', 'JORNAL / HORA']], df_labour], axis=0)

    _df_temp = process_sheet_between_tags(df_sheet, labels=[
        'MATERIALES', 'TRANSPORTE'])
    df_materials = pd.concat(
        [_df_temp[['DESCRIPCIÓN', 'UNIDAD', 'P. UNITARIO']], df_materials], axis=0)

df_clean_equipment = clean_and_sort_dataframe(df_equipment, start_index=1)
df_clean_labour = clean_and_sort_dataframe(df_labour, start_index=1)
df_clean_materials = clean_and_sort_dataframe(df_materials, start_index=1)

print(df_clean_equipment)
print(df_clean_labour)
print(df_clean_materials)


df_sheet_test = process_sheet_between_tags(df_dict_sheets['10'], labels=[
    'MATERIALES', 'TRANSPORTE'])

dfC = merge_dataframes(df_sheet_test, df_clean_equipment, [
                       'Z', 'CANTIDAD'], result_column_name='Z')

print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
