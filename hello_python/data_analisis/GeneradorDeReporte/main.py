import pandas as pd

# ----------- Headers del dataframe nuevo -----------
nombres_limpios = [
    "Codigo", "Descripcion", "Cantidad", "Pendiente", "MontoBruto", 
    "Descuentos", "IVA", "Costo", "Utilidad", "PorcUtilidad", "Existencia"
]

#  Data frame 
df = pd.read_csv(
    r"\\SERVIDOR\a2Apps\a2Admin\Empre001\REPORTS\Productosvendidos.TXT",
    sep='\t', 
    encoding='latin-1', 
    names=nombres_limpios, #Nombres nuevos para el header
    header=0,
    thousands='.', 
    decimal=',',
    index_col=False,         
    dtype={'Codigo': str}    #Codigo tiene que ser leido como str y no como objeto
)

# ----------- Filtros-----------
# filtro = df[df['Cantidad'] < 50]
filtro_pasta_allegri = df[df['Descripcion'].str.contains("PASTA ALLEGRI", case=False, na=False )]
total= filtro_pasta_allegri.sum()

filtro_pasta_horizonte = df[df['Descripcion'].str.contains("PASTA HORIZONTE", case=False, na=False )]
total = filtro_pasta_horizonte.sum()

filtro_pasticho_allegri = df[df['Descripcion'].str.contains("PASTICHO ALLEGRI", case=False, na=False )]
total = filtro_pasticho_allegri.sum()

filtro_pasticho_micasa =df[df['Descripcion'].str.contains("PASTICHO MI CASA", case=False, na=False )]
total = filtro_pasticho_micasa.sum()


filtro_harina_dulce_mar =df[df['Descripcion'].str.contains("HARINA DE TRIGO DULCE MAR", case=False, na=False )]
total = filtro_harina_dulce_mar.sum()


filtro_devoluciones =df[df['Descripcion'].str.contains("ITEM SIN EXISTENCIA", case=False, na=False )]
total = filtro_devoluciones.sum()


#--- PRODUCTOS MONACA ---
filtro_avena = df[df['Descripcion'].str.contains("AVENA LASSIE", case=False, na=False )]
filtro_harina_maiz = df[df['Descripcion'].str.contains("HARINA JUANA", case=False, na=False )]
filtro_adobo = df[df['Codigo']=='010003']
filtro_arroz_monica = df[df['Descripcion'].str.contains("ARROZ MONICA", case=False, na=False )]
filtro_harina_robin_hood = df[df['Descripcion'].str.contains("ROBIN HOOD", case=False, na=False )]
filtro_chococao = df[df['Descripcion'].str.contains("BEBIDA CHOCOCAO", case=False, na=False )]













# Total = filtro['Cantidad'].sum()

# ----------- Salida de datos -----------
print("----------------- Productos Allegri -----------------")
print(filtro_pasta_allegri[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_pasta_horizonte[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_pasticho_allegri[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_harina_dulce_mar[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_pasticho_micasa[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_devoluciones[['Codigo', 'Descripcion', 'Cantidad']])

print("----------------- Productos Monaca -----------------")
print(filtro_harina_maiz[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_arroz_monica[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_harina_robin_hood[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_avena[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_adobo[['Codigo', 'Descripcion', 'Cantidad']])
print(filtro_chococao[['Codigo', 'Descripcion', 'Cantidad']])

