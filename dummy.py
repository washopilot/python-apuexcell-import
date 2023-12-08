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


# Ejemplo de uso
dictionary = {1: ('a', 'b'), 2: ('c', 'd'), 3: ('e', 'f')}
tuple_list = [('a', 'b', 'm'), ('c', 'd', 'n'), ('e', 'o', 'f', 'p')]

result = transform_tuples(dictionary, tuple_list)
print(result)
