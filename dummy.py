import pandas as pd

# DataFrame 1
data1 = {'Nombre': ['Alice', 'Bob'],
         'Edad': [25, 30]}
df1 = pd.DataFrame(data1)

# DataFrame 2
data2 = {'Nombre': ['Bob', 'Charlie', 'David'],
         'Edad': [31, 35, 40]}
df2 = pd.DataFrame(data2)

# Concatenar a lo largo de las filas (axis=0)
df_concat = pd.concat([df1, df2], axis=0)

# Eliminar filas duplicadas basadas en todas las columnas
df_concat_sin_duplicados = df_concat.drop_duplicates()

# Imprimir el DataFrame resultante sin filas duplicadas
print("DataFrame Concatenado sin Filas Duplicadas:")
print(df_concat_sin_duplicados.reset_index(drop=True))
