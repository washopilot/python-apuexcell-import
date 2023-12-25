import time

import pandas as pd

from helpers import process_sheet

tcpu0 = time.time()

excel_file = 'original.xlsx'

_sheet_names = pd.ExcelFile(excel_file).sheet_names

df_dict_sheets = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None)


df_materials = pd.DataFrame()

for df_sheet in df_dict_sheets.values():
    _df_temp_process = process_sheet(df_sheet, etiquetas=[
        'EQUIPOS', 'MANO DE OBRA'])
    df_materials = pd.concat(
        [_df_temp_process[['DESCRIPCIÓN', 'TARIFA']], df_materials], axis=0)

df_clean_equipment = df_materials.drop_duplicates().dropna(
    axis=0, how='all').sort_values(by='DESCRIPCIÓN', ascending=True)
new_index = range(200, 200 + len(df_clean_equipment))
df_clean_equipment = df_clean_equipment.set_index(pd.Index(new_index))

print(df_clean_equipment)

print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
