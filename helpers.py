from openpyxl.worksheet.worksheet import Worksheet


def listing_sheet(ws: Worksheet, min_col=2, max_col=10):
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
        # _conditions_to_exclude = [
        #     'Herramienta menor (5% M.O.)', 'Seguridad industrial e Higiene Laboral (2% M.O)']
        # if any(condition in _tpl for condition in _conditions_to_exclude):
        #     _resulting_tuple = (_tpl[cols[0]],)
        # else:
        _resulting_tuple = tuple(_tpl[i] for i in cols)

        if any(element not in (None, '') for element in _resulting_tuple):
            result.append(_resulting_tuple)

    return result


def transform_tuples(dictionary, tuple_list):
    """
    Transforma una lista de tuplas reemplazando todos los elementos con la clave del diccionario
    si la tupla del diccionario está incluida en la tupla de la lista.

    Args:
    - dictionary: Diccionario de tuplas.
    - tuple_list: Lista de tuplas con más de dos elementos.

    Returns:
    - Lista de tuplas transformada.
    """
    result = []

    # Iterar sobre la lista de tuplas
    for tuple_list_item in tuple_list:
        # Buscar la tupla en el diccionario
        for key, tuple_dictionary in dictionary.items():
            # Verificar si la tupla del diccionario está incluida en la tupla de la lista
            if all(element in tuple_list_item for element in tuple_dictionary):
                # Construir la nueva tupla secuencialmente
                new_tuple = (key,)
                for element in tuple_list_item:
                    if element not in tuple_dictionary:
                        new_tuple += (element,)
                result.append(new_tuple)
                break  # Salir del bucle interno si se encuentra la correspondencia

    return result
