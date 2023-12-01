from openpyxl.worksheet.worksheet import Worksheet


def listingSheet(ws: Worksheet, min_col=2, max_col=10):
    """Rutina para listar filas de una hoja del libro de excel

    Args:
        ws (Worksheet): libro de excell

    Returns:
        list: Lista sin depurar de las filas de una hoja 
    """
    _wsData = []

    for row in ws.iter_rows(min_col=min_col, max_col=max_col):
        _row = tuple(
            cell.value for cell in row)

        if _row:
            _wsData.append(_row)

    return _wsData


def get_tuples_between_tags(lst: list, start_tag: str, end_tag: str, delete_first_last=True):
    """Rutina para listar filas entre etiquetas

    Args:
        lst (list): lista de entrada
        start_tag (str): Etiqueta de entrada
        end_tag (str): Etiqueta de salida
        delete_first_last (bool): borrar primera y último elemento de la lista resultante. Por defecto, es True

    Returns:
        list: Retorna de lista resultante
    """

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
    if len(result) >= 2 and delete_first_last:
        result.pop(0)
        result.pop(-1)

    return result


def clean_list_tuples(lst: list, cols: tuple):
    """Rutina para limpiar una lista de tuplas y devolver por las columnas indicadas

    Args:
        lst (list): Lista de entrada con tuplas a depurar
        cols (tuple): Tupla con un listado de columnas a devolver partiendo de cero (0,..n)

    Returns:
        list: Retorna la lista depurada
    """

    result = []

    for _tpl in lst:
        _conditions_to_exclude = [
            'Herramienta menor (5% M.O.)', 'Seguridad industrial e Higiene Laboral (2% M.O)']
        if any(condition in _tpl for condition in _conditions_to_exclude):
            _resulting_tuple = (_tpl[cols[0]],)
        else:
            _resulting_tuple = tuple(_tpl[i] for i in cols)

        if any(element not in (None, '') for element in _resulting_tuple):
            result.append(_resulting_tuple)

    return result
