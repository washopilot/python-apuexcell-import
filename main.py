import time

import pandas as pd
from tqdm import tqdm

from helpers import (clean_and_sort_dataframe, merge_dataframes,
                     process_sheet_between_tags)


def main():
    tcpu0 = time.time()
    excel_file = 'original.xlsx'

    # Read the Excel file and get the sheet names and data for each sheet in a single read
    with pd.ExcelFile(excel_file) as xls:
        sheet_names = xls.sheet_names
        df_dict_sheets = {}

        # Use tqdm to show progress
        for sheet_name in tqdm(sheet_names, desc="Read excel file..."):
            df_dict_sheets[sheet_name] = pd.read_excel(
                xls, sheet_name=sheet_name, index_col=None, header=None, nrows=65)

    # Process and store data in lists
    equipment_data, labour_data, materials_data = [], [], []
    for sheet_name, df_sheet in tqdm(df_dict_sheets.items(), desc="Processing Sheets"):
        tags = df_sheet.values.flatten()
        if 'EQUIPOS' in tags and 'MANO DE OBRA' in tags:
            equipment_data.append(process_sheet_between_tags(
                df_sheet, labels=['EQUIPOS', 'MANO DE OBRA'])[['Descripción', 'Tarifa']])
        if 'MANO DE OBRA' in tags and 'MATERIALES' in tags:
            labour_data.append(process_sheet_between_tags(df_sheet, labels=[
                               'MANO DE OBRA', 'MATERIALES'])[['Descripción', 'Jornal/HR']])
        if 'MATERIALES' in tags and 'TRANSPORTE' in tags:
            materials_data.append(process_sheet_between_tags(df_sheet, labels=[
                                  'MATERIALES', 'TRANSPORTE'])[['Descripción', 'Unidad', 'Precio Unit.']])

    # Function to prepare data by concatenating, cleaning, and sorting
    def prepare_data(data_list, start_index):
        df = pd.concat(data_list, axis=0)
        return clean_and_sort_dataframe(df, column_name='Descripción', start_index=start_index)

    # Prepare the equipment data
    df_clean_equipment = prepare_data(equipment_data, 100)
    df_clean_labour = prepare_data(labour_data, 200)
    df_clean_materials = prepare_data(materials_data, 300)

    # Print DataFrames
    print("\nPrint results:\n")
    print("df_clean_equipment:\n", df_clean_equipment, "\n")
    print("df_clean_labour:\n", df_clean_labour, "\n")
    print("df_clean_materials:\n", df_clean_materials, "\n")

    # Specific sheet processing
    df_sheet_test = process_sheet_between_tags(
        df_dict_sheets['Sheet357'], labels=['EQUIPOS', 'MANO DE OBRA'])

    # Merge DataFrames
    dfC = merge_dataframes(df_sheet_test, df_clean_equipment, [
                           'Z', 'Descripción', 'Cantidad'], result_column_name='Z')

    # Print results of processing and merging
    print("df_sheet_test:\n", df_sheet_test, "\n")
    print("dfC:\n", dfC, "\n")

    # Create an Excel writer
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    # Export DataFrames to Excel sheets
    print('Write output.xlsx\n')
    df_clean_equipment.to_excel(writer, sheet_name='Hoja1', index=False)
    df_clean_labour.to_excel(writer, sheet_name='Hoja2', index=False)
    df_clean_materials.to_excel(writer, sheet_name='Hoja3', index=False)

    # Save the Excel file
    writer._save()

    # Print elapsed time
    print('Completed in:', (time.time() - tcpu0), 'seconds')


if __name__ == "__main__":
    main()
