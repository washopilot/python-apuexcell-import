import time

from openpyxl import Workbook, load_workbook
from tabulate import tabulate

from helpers import clean_list_tuples, get_tuples_between_tags, listingSheet, transform_tuples

tcpu0 = time.time()

wb = load_workbook(filename='original.xlsx', read_only=True, data_only=True)

# Inicialización de data
listing_data = []  # Aquí se almacena todos los apus
equipment_list = labour_list = materials_list = []

# Bucle busqueda y limpieza de insumos
for sheet in wb.sheetnames:
    if sheet == 'Rubros':
        continue

    detailedSheet = listingSheet(wb[sheet])

    equipment_list = equipment_list + clean_list_tuples(get_tuples_between_tags(
        detailedSheet, 'EQUIPOS', 'MANO DE OBRA', True), (0, 5))
    labour_list = labour_list + clean_list_tuples(get_tuples_between_tags(
        detailedSheet, 'MANO DE OBRA', 'MATERIALES', True), (0, 5))
    materials_list = materials_list + clean_list_tuples(get_tuples_between_tags(
        detailedSheet, 'MATERIALES', 'TRANSPORTE', True), (0, 5, 7))

# Limpieza de repetidos y ordenamiento
clean_equipment_dict = {index: value for index,
                        value in enumerate(sorted(set(equipment_list)), 1)}
clean_labour_dict = {index: value for index,
                        value in enumerate(sorted(set(labour_list)), 1)}
clean_materials_dict = {index: value for index,
                        value in enumerate(sorted(set(materials_list)), 1)}

print(tabulate(clean_equipment_dict.items()))
print()
print(tabulate(clean_labour_dict.items()))
print()
print(tabulate(clean_materials_dict.items()))
print()

# Segunda vuelta de rubros
for sheet in wb.sheetnames:
    if sheet == 'Rubros':
        continue

    detailedSheet = listingSheet(wb[sheet])

    equipment_list = clean_list_tuples(get_tuples_between_tags(
        detailedSheet, 'EQUIPOS', 'MANO DE OBRA', True), (0, 4, 5))
    new_equipment_list = transform_tuples(clean_equipment_dict, equipment_list)

    labour_list = clean_list_tuples(get_tuples_between_tags(
        detailedSheet, 'MANO DE OBRA', 'MATERIALES', True), (0, 4, 5))
    new_labour_list = transform_tuples(clean_labour_dict, labour_list)

    materials_list = clean_list_tuples(get_tuples_between_tags(
        detailedSheet, 'MATERIALES', 'TRANSPORTE', True), (0, 5, 6, 7))
    new_materials_list = transform_tuples(clean_materials_dict, materials_list)

    listing_data.append({'SHEET': sheet,
                        'EQUIPO': new_equipment_list,
                        'MANO DE OBRA': new_labour_list, 'MATERIALES': new_materials_list})

print(listing_data)
# Close the workbook after reading
wb.close()


# # Crear un nuevo libro de Excel y EXPORTA los resultados
# excel_book = Workbook()
# excel_book.remove(excel_book['Sheet'])
# _active_sheet = excel_book.create_sheet(title='EQUIPOS')
# for row_data in clean_equipment_list:
#     _active_sheet.append((row_data[0], *row_data[1]))

# _active_sheet = excel_book.create_sheet(title='MANO DE OBRA')
# for row_data in clean_labour_list:
#     _active_sheet.append((row_data[0], *row_data[1]))

# _active_sheet = excel_book.create_sheet(title='MATERIALES')
# for row_data in clean_materials_list:
#     _active_sheet.append((row_data[0], *row_data[1]))

# # Guardar el libro de Excel
# excel_book.save("output.xlsx")

# print("Se ha creado el archivo Excel: output.xlsx")


print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
