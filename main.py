import time

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet import worksheet
from tabulate import tabulate

tcpu0 = time.time()

wb = load_workbook(filename='original.xlsx', read_only=True, data_only=True)

listingData = ()
# ws = wb['1']


# for idx, row in enumerate(ws.rows, 1):
#     _row = [idx]

#     for cell in row:
#         if cell.value:
#             _row.append(cell.value)

#     if _row != [idx]:
#         data.append(_row)
#         print(_row)

def listingSheet(ws: worksheet.Worksheet):
    _wsData = []

    for row in ws.iter_rows(min_col=2,max_col=10):
        _row = tuple(
            cell.value for cell in row)
        # print(_row, len(_row))

        if _row:
            _wsData.append(_row)

    return _wsData


def obt_tpl_ent_etq(lst, etq_ini, etq_fin):
    res = []
    entre_etiq = False

    for tpl in lst:
        if etq_ini in tpl:
            entre_etiq = True
            temp_res = []
        elif etq_fin in tpl:
            entre_etiq = False
            if temp_res:
                res.extend(temp_res)
        elif entre_etiq:
            temp_res.append(tpl)

    # Eliminar el primer y último elemento de la lista resultante
    if len(res) >= 2:
        res.pop(0)
        res.pop(-1)

    return res


for sheet in wb.sheetnames:
    detailedSheet = listingSheet(wb[sheet])
    # print(detailedSheet)
    insumos = obt_tpl_ent_etq(detailedSheet, 'EQUIPOS', 'MANO DE OBRA')
    # print(insumos)
    for tupla in insumos:
        # print(tupla)
        if not ('Herramienta menor (5% M.O.)' in tupla or 'Seguridad industrial e Higiene Laboral (2% M.O)' in tupla):
            tupla_resultante = (tupla[0], tupla[5],)
        else:
            tupla_resultante = (tupla[0],)
        if all(elemento == None for elemento in tupla_resultante) or all(elemento == '' for elemento in tupla_resultante) or tuple(set(tupla_resultante)) == ('', None):
            continue
        else:
            # print(tupla_resultante)
            listingData += (tupla_resultante,)


print()
print(len(listingData))
print(listingData)

print()
listingDataFilter = tuple(set(listingData))
print(len(listingDataFilter))
print(listingDataFilter)
print(tabulate(listingDataFilter))


# Close the workbook after reading
wb.close()


# Crear un nuevo libro de Excel y obtener la hoja activa
libro_excel = Workbook()
hoja_activa = libro_excel.active

# Escribir datos en la hoja
for fila_datos in listingDataFilter:
    hoja_activa.append(fila_datos)

# Guardar el libro de Excel
libro_excel.save("output.xlsx")

print("Se ha creado el archivo Excel: output.xlsx")


print('Terminado en: ', (time.time()-tcpu0), 'segundos')
