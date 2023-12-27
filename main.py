import time

import pandas as pd

from helpers import (clean_and_sort_dataframe, merge_dataframes,
                     process_sheet_between_tags)

tcpu0 = time.time()

excel_file = 'original.xlsx'

_sheet_names = pd.ExcelFile(excel_file).sheet_names

df_dict_sheets = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None, nrows=65, usecols='B:J')


df_materials = pd.DataFrame()

for df_name, df_sheet in df_dict_sheets.items():
    _df_temp_process = process_sheet_between_tags(df_sheet, labels=[
        'MATERIALES', 'TRANSPORTE'])
    # print(_df_temp_process.columns)
    df_materials = pd.concat(
        [_df_temp_process[['DESCRIPCIÓN', 'UNIDAD', 'P. UNITARIO']], df_materials], axis=0)

df_clean_equipment = clean_and_sort_dataframe(df_materials, start_index=100)


df_sheet_test = process_sheet_between_tags(df_dict_sheets['10'], labels=[
    'MATERIALES', 'TRANSPORTE'])

print(df_clean_equipment)
print()
print(df_sheet_test)
print()

dfC = merge_dataframes(df_sheet_test, df_clean_equipment, [
                       'Z', 'CANTIDAD'], result_column_name='Z')

print(dfC)
print()
print(df_clean_equipment.loc[200])


print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
