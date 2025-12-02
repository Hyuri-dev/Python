import pandas as pd
from rich.console import Console
from rich.table import Table

# ----------- Headers del dataframe nuevo -----------
nombres_limpios = [
    "Codigo", "Descripcion", "Cantidad", "Pendiente", "MontoBruto", 
    "Descuentos", "IVA", "Costo", "Utilidad", "PorcUtilidad", "Existencia"
]

#  Data frame 
df = pd.read_csv(
    r"C:\Users\Jefferson\desarrollo python\hello_python\Python\hello_python\data_analisis\GeneradorDeReporte\Productosvendidos_PRUEBA.TXT",
    sep='\t', 
    encoding='latin-1', 
    names=nombres_limpios, #Nombres nuevos para el header
    header=0,
    thousands='.', 
    decimal=',',
    index_col=False,         
    dtype={'Codigo': str}    #Codigo tiene que ser leido como str y no como objeto
)


productos = {
  "Pasta Allegri": "ALLEGRI",
  "Pasta Horizonte": "HORIZONTE",
  "Pasticho Allegri": "PASTICHO ALLEGRI",
  "Pasticho Mi Casa": "PASTICHO MI CASA",
  "Harina de Trigo":  "HARINA DE TRIGO MAR",
  "Devoluciones": "ITEM SIN EXISTENCIA"
}

reporte_resumen = []

for nombre_producto , texto_buscar in productos.items():
  filtro = df[df['Descripcion'].str.contains(texto_buscar, case=False, na=False)]
  total_cantidad = filtro['Cantidad'].sum()

  reporte_resumen.append({
    "Producto/Categoria": nombre_producto,
    "Cantidad Total": total_cantidad
  })

filtro_adobo = df[df['Codigo']== '010003']
reporte_resumen.append({
  'Producto / Categoria': 'Adobo La Comadre 200Gr',
  'Cantidad Total': filtro_adobo['Cantidad'].sum(),
  'Nro. Ventas': len(filtro_adobo)
})

df_reporte = pd.DataFrame(reporte_resumen)

pd.options.display.float_format = '{:,.2f}'.format
print("\n REPORTE DEL MES: ")
print(df_reporte)
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

console = Console()

table = Table(title="📊Reporte De Ventas")
table.add_column("Producto", style="cyan", no_wrap=True)
table.add_column("Cant. Total", justify="right", style="magenta")
table.add_column("Ventas",justify="right", style="yellow")

for index, row in df_reporte.iterrows():
  table.add_row(
    str(row['Producto/Categoria']),
    f"{row['Cantidad Total']:,.2f}",
    str(row['Nro. Ventas'])
  )

  console.print(table)