import time

from openpyxl import load_workbook
from tabulate import tabulate

from helpers import clean_list_tuples, get_tuples_between_tags, listingSheet

tcpu0 = time.time()

wb = load_workbook(filename='original.xlsx', read_only=True, data_only=True)

# Inicialización de data
listing_data = []
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
clean_equipment_list = list(enumerate(sorted(set(equipment_list)), 1))
clean_labour_list = list(enumerate(sorted(set(labour_list)), 1))
clean_materials_list = list(enumerate(sorted(set(materials_list)), 1))

print(tabulate(clean_equipment_list))
print(tabulate(clean_labour_list))
print(tabulate(clean_materials_list))

# Close the workbook after reading
wb.close()


# # Crear un nuevo libro de Excel y obtener la hoja activa
# excel_book = Workbook()
# active_sheet = excel_book.active

# # Escribir datos en la hoja
# for row_data in listingDataFilter:
#     active_sheet.append(row_data)

# # Guardar el libro de Excel
# excel_book.save("output.xlsx")

# print("Se ha creado el archivo Excel: output.xlsx")


print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
