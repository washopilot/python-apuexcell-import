import time

import pandas as pd

from helpers import (clean_and_sort_dataframe, merge_dataframes,
                     process_sheet_between_tags)

tcpu0 = time.time()

excel_file = 'original.xlsx'

_sheet_names = pd.ExcelFile(excel_file).sheet_names

df_dict_sheets = pd.read_excel(excel_file, sheet_name=[
    sheet for sheet in _sheet_names if sheet != 'Rubros'], index_col=None, header=None, nrows=65, usecols='B:J')

# Initialize lists to store temporary data
equipment_data, labour_data, materials_data = [], [], []

for df_sheet in df_dict_sheets.values():
    # Process and store data in lists instead of repeatedly concatenating DataFrames
    equipment_data.append(process_sheet_between_tags(df_sheet, labels=['EQUIPOS', 'MANO DE OBRA'])
                          [['DESCRIPCIÓN', 'TARIFA']])

    labour_data.append(process_sheet_between_tags(df_sheet, labels=['MANO DE OBRA', 'MATERIALES'])
                       [['DESCRIPCIÓN', 'JORNAL / HORA']])

    materials_data.append(process_sheet_between_tags(df_sheet, labels=['MATERIALES', 'TRANSPORTE'])
                          [['DESCRIPCIÓN', 'UNIDAD', 'P. UNITARIO']])


# Function to prepare data by concatenating, cleaning, and sorting
def prepare_data(data_list, start_index):
    df = pd.concat(data_list, axis=0)
    return clean_and_sort_dataframe(df, start_index=start_index)


# Prepare the equipment data
df_clean_equipment = prepare_data(equipment_data, 100)
df_clean_labour = prepare_data(labour_data, 200)
df_clean_materials = prepare_data(materials_data, 300)


# Calculate the time elapsed since the start_time and print the result in seconds.
def print_time_elapsed(start_time):
    print('Completed in:', (time.time() - start_time), 'seconds')


# Print DataFrames
print("df_clean_equipment:\n", df_clean_equipment, "\n")
print("df_clean_labour:\n", df_clean_labour, "\n")
print("df_clean_materials:\n", df_clean_materials, "\n")

# Specific sheet processing
df_sheet_test = process_sheet_between_tags(
    df_dict_sheets['1'], labels=['EQUIPOS', 'MANO DE OBRA'])

# Merge DataFrames
dfC = merge_dataframes(df_sheet_test, df_clean_equipment, [
                       'Z', 'DESCRIPCIÓN', 'CANTIDAD'], result_column_name='Z')

# Print results of processing and merging
print("df_sheet_test:\n", df_sheet_test, "\n")
print("dfC:\n", dfC, "\n")

# Print elapsed time
print_time_elapsed(tcpu0)
