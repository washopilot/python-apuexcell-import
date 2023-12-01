import time

from openpyxl import load_workbook
from tabulate import tabulate

from helpers import clean_list_tuples, get_tuples_between_tags, listingSheet

tcpu0 = time.time()

wb = load_workbook(filename='original.xlsx', read_only=True, data_only=True)

listingData = []


# # Bucle principal
# for sheet in wb.sheetnames:
#     detailedSheet = listingSheet(wb[sheet])
#     inputs = get_tuples_between_tags(
#         detailedSheet, 'EQUIPOS', 'MANO DE OBRA', True)

#     print(inputs)

detailedSheet = listingSheet(wb['1'])
supplies_list = get_tuples_between_tags(
    detailedSheet, 'EQUIPOS', 'MANO DE OBRA', True)
clean_supplies_list = clean_list_tuples(supplies_list, (0, 5))
print(clean_supplies_list)


# # Imprime la lista listingData
# print()
# print(len(listingData))
# print(listingData)

# # Filtra la lista listingData de repetidos
# print()
# listingDataFilter = list(set(listingData))
# print(len(listingDataFilter))
# print(listingDataFilter)
# print(tabulate(listingDataFilter))


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
