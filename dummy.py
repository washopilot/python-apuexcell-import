def obt_tpl_ent_etq(lst, etq_ini, etq_fin):
    res = []
    entre_etiq = False

    for tpl in lst:
        if tpl == (etq_ini,):
            entre_etiq = True
            temp_res = []
        elif tpl == (etq_fin,):
            entre_etiq = False
            if temp_res:
                res.extend(temp_res)

    # Eliminar el primer y último elemento de la lista resultante
    if len(res) >= 2:
        res.pop(0)
        res.pop(-1)

    return tuple(res)


# Ejemplo de uso
lst_tpls = [('etiqueta1',), ('a', 'b'), ('a', 'b'), ('a', 'b'),
            ('etiqueta2',), ('a', 'b'), ('a', 'b'), ('etiqueta3',)]
res = obt_tpl_ent_etq(lst_tpls, 'etiqueta1', 'etiqueta2')

print(res)
