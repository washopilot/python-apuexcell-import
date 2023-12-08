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

    _detailedSheet = listingSheet(wb[sheet])

    equipment_list = equipment_list + clean_list_tuples(get_tuples_between_tags(
        _detailedSheet, 'EQUIPOS', 'MANO DE OBRA', True), (0, 5))
    labour_list = labour_list + clean_list_tuples(get_tuples_between_tags(
        _detailedSheet, 'MANO DE OBRA', 'MATERIALES', True), (0, 5))
    materials_list = materials_list + clean_list_tuples(get_tuples_between_tags(
        _detailedSheet, 'MATERIALES', 'TRANSPORTE', True), (0, 5, 7))

# Limpieza de repetidos y ordenamiento
clean_equipment_dict = {index: value for index,
                        value in enumerate(sorted(set(equipment_list)), 77)}
clean_labour_dict = {index: value for index,
                     value in enumerate(sorted(set(labour_list)), 532)}
clean_materials_dict = {index: value for index,
                        value in enumerate(sorted(set(materials_list)), 326)}

# print(tabulate(clean_equipment_dict.items()))
# print()
# print(tabulate(clean_labour_dict.items()))
# print()
# print(tabulate(clean_materials_dict.items()))
# print()

# Segunda vuelta de rubros
for sheet in wb.sheetnames:
    if sheet == 'Rubros':
        continue

    _detailedSheet = listingSheet(wb[sheet])
    # print(_detailedSheet)

    _equipment_list = clean_list_tuples(get_tuples_between_tags(
        _detailedSheet, 'EQUIPOS', 'MANO DE OBRA', True), (0, 4, 5))
    _new_equipment_list = transform_tuples(
        clean_equipment_dict, _equipment_list)

    _labour_list = clean_list_tuples(get_tuples_between_tags(
        _detailedSheet, 'MANO DE OBRA', 'MATERIALES', True), (0, 4, 5))
    _new_labour_list = transform_tuples(clean_labour_dict, _labour_list)

    _materials_list = clean_list_tuples(get_tuples_between_tags(
        _detailedSheet, 'MATERIALES', 'TRANSPORTE', True), (0, 5, 6, 7))
    _new_materials_list = transform_tuples(
        clean_materials_dict, _materials_list)

    _new_pa = {'SHEET': sheet, 'ITEM': _detailedSheet[7][0], 'RUBRO': _detailedSheet[9][0], 'UNIDAD': _detailedSheet[9][8],   'EQUIPO': _new_equipment_list,
               'MANO DE OBRA': _new_labour_list, 'MATERIALES': _new_materials_list}
    # print(_new_pa)
    listing_data.append(_new_pa)

# print(listing_data)

# Creación del diccionario general de Rubros
dict_data = {index: value for index,
             value in enumerate(listing_data, 3237)}

print(dict_data[3239])

# Close the workbook after reading
wb.close()


# # Crear un nuevo libro de Excel y EXPORTA los resultados
# excel_book = Workbook()
# excel_book.remove(excel_book['Sheet'])
# _active_sheet = excel_book.create_sheet(title='EQUIPOS')
# for row_data in clean_equipment_dict.items():
#     _active_sheet.append((row_data[0], *row_data[1]))

# _active_sheet = excel_book.create_sheet(title='MANO DE OBRA')
# for row_data in clean_labour_dict.items():
#     _active_sheet.append((row_data[0], *row_data[1]))

# _active_sheet = excel_book.create_sheet(title='MATERIALES')
# for row_data in clean_materials_dict.items():
#     _active_sheet.append((row_data[0], *row_data[1]))

# # Guardar el libro de Excel
# excel_book.save("output.xlsx")

# print("Se ha creado el archivo Excel: output.xlsx")


print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
