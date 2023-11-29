import time

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet import worksheet
from tabulate import tabulate

tcpu0 = time.time()

wb = load_workbook(filename='original.xlsx', read_only=True, data_only=True)

listingData = []

# Rutina para listar filas de una hoja del libro excel


def listingSheet(ws: worksheet.Worksheet):
    _wsData = []

    for row in ws.iter_rows(min_col=2, max_col=10):
        _row = tuple(
            cell.value for cell in row)

        if _row:
            _wsData.append(_row)

    return _wsData

# Rutina para listar filas entre etiquetas


def get_tuples_between_tags(lst, start_tag, end_tag):
    result = []
    inside_tag = False

    for tpl in lst:
        if start_tag in tpl:
            inside_tag = True
            temp_result = []
        elif end_tag in tpl:
            inside_tag = False
            if temp_result:
                result.extend(temp_result)
        elif inside_tag:
            temp_result.append(tpl)

    # Eliminar el primer y último elemento de la lista resultante
    if len(result) >= 2:
        result.pop(0)
        result.pop(-1)

    return result


# Bucle principal
for sheet in wb.sheetnames:
    detailedSheet = listingSheet(wb[sheet])
    inputs = get_tuples_between_tags(detailedSheet, 'EQUIPOS', 'MANO DE OBRA')

    # Limpia las tuplas y añade a listingData
    for tpl in inputs:
        conditions_to_exclude = [
            'Herramienta menor (5% M.O.)', 'Seguridad industrial e Higiene Laboral (2% M.O)']

        if any(condition in tpl for condition in conditions_to_exclude):
            resulting_tuple = (tpl[0],)
        else:
            resulting_tuple = (tpl[0], tpl[5])

        if any(element not in (None, '') for element in resulting_tuple):
            listingData.append(resulting_tuple)

# Imprime la lista listingData
print()
print(len(listingData))
print(listingData)

# Filtra la lista listingData de repetidos
print()
listingDataFilter = list(set(listingData))
print(len(listingDataFilter))
print(listingDataFilter)
print(tabulate(listingDataFilter))


# Close the workbook after reading
wb.close()


# Crear un nuevo libro de Excel y obtener la hoja activa
excel_book = Workbook()
active_sheet = excel_book.active

# Escribir datos en la hoja
for row_data in listingDataFilter:
    active_sheet.append(row_data)

# Guardar el libro de Excel
excel_book.save("output.xlsx")

print("Se ha creado el archivo Excel: output.xlsx")


print('Finalizado en: ', (time.time()-tcpu0), 'segundos')
