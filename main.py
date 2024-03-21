import time
import pandas as pd
from tqdm import tqdm
from helpers import (clean_and_sort_dataframe, merge_dataframes,
                     process_sheet_between_tags)


def main():
    tcpu0 = time.time()
    excel_file = 'original.xlsx'

    # Leer el archivo Excel y obtener el nombre de las hojas y los datos de cada hoja en una sola lectura
    with pd.ExcelFile(excel_file) as xls:
        sheet_names = xls.sheet_names
        df_dict_sheets = {}

        # Utilizar tqdm para mostrar el progreso
        for sheet_name in tqdm(sheet_names, desc="Read excel file..."):
            df_dict_sheets[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name, index_col=None, header=None, nrows=65)

    # Inicializar listas para almacenar datos temporales
    equipment_data, labour_data, materials_data = [], [], []

    # Procesar y almacenar datos en listas
    for sheet_name, df_sheet in tqdm(df_dict_sheets.items(), desc="Processing Sheets"):
        if 'EQUIPOS' in df_sheet.values and 'MANO DE OBRA' in df_sheet.values:
            equipment_data.append(process_sheet_between_tags(df_sheet, labels=['EQUIPOS', 'MANO DE OBRA'])[['Descripción', 'Tarifa']])
        if 'MANO DE OBRA' in df_sheet.values and 'MATERIALES' in df_sheet.values:
            labour_data.append(process_sheet_between_tags(df_sheet, labels=['MANO DE OBRA', 'MATERIALES'])[['Descripción', 'Jornal/HR']])
        if 'MATERIALES' in df_sheet.values and 'TRANSPORTE' in df_sheet.values:
            materials_data.append(process_sheet_between_tags(df_sheet, labels=['MATERIALES', 'TRANSPORTE'])[['Descripción', 'Unidad', 'Precio Unit.']])

    # Function to prepare data by concatenating, cleaning, and sorting
    def prepare_data(data_list, start_index):
        df = pd.concat(data_list, axis=0)
        return clean_and_sort_dataframe(df, column_name='Descripción', start_index=start_index)

    # Prepare the equipment data
    df_clean_equipment = prepare_data(equipment_data, 100)
    df_clean_labour = prepare_data(labour_data, 200)
    df_clean_materials = prepare_data(materials_data, 300)

    # Calculate the time elapsed since the start_time and print the result in seconds.
    def print_time_elapsed(start_time):
        print('Completed in:', (time.time() - start_time), 'seconds')

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

    # Crear un escritor de Excel
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    # Exportar los DataFrames a hojas de Excel
    print('Write output.xlsx\n')
    df_clean_equipment.to_excel(writer, sheet_name='Hoja1', index=False)
    df_clean_labour.to_excel(writer, sheet_name='Hoja2', index=False)
    df_clean_materials.to_excel(writer, sheet_name='Hoja3', index=False)

    # Guardar el archivo Excel
    writer._save()

    # Print elapsed time
    print_time_elapsed(tcpu0)


if __name__ == "__main__":
    main()
