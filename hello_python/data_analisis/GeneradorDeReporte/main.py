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


productos = {
  "Pasta Allegri": "ALLEGRI",
  "Pasta Horizonte": "HORIZONTE",
  "Pasticho Allegri": "PASTICHO ALLEGRI",
  "Pasticho Mi Casa": "PASTICHO MI CASA",
  "Harina de Trigo Dulce Mar":  "HARINA DE TRIGO DULCE MAR",
  "Harina de Maiz Juana": "HARINA JUANA",
  "Arroz Monica": "ARROZ MONICA",
  "ChocoCao": "BEBIDA CHOCOCAO",
  "Devoluciones": "ITEM SIN EXISTENCIA"
}

reporte_resumen = []


# ----------- Filtros-----------

def crea_reporte ():
  
    for nombre_producto , texto_buscar in productos.items():
      filtro = df[df['Descripcion'].str.contains(texto_buscar, case=False, na=False)]
      total_cantidad = filtro['Cantidad'].sum()
      total_bruto = filtro['MontoBruto'].sum()

      reporte_resumen.append({
        "Producto/Categoria": nombre_producto,
        "Cantidad Total": total_cantidad,
        "MontoBruto": total_bruto
      })
      
      
    filtro_avena_400 =df[df['Codigo']== '010002']
    reporte_resumen.append({
    'Producto/Categoria': 'Avena Lassie 400Gr',
      'Cantidad Total': filtro_avena_400['Cantidad'].sum(),
      'MontoBruto': filtro_avena_400['MontoBruto'].sum()
      # 'Nro. Ventas': len(filtro_adobo)
      })
    
    filtro_avena_800 =df[df['Codigo']== '010008']
    reporte_resumen.append({
    'Producto/Categoria': 'Avena Lassie 800Gr',
      'Cantidad Total': filtro_avena_800['Cantidad'].sum(),
      'MontoBruto': filtro_avena_800['MontoBruto'].sum()
      # 'Nro. Ventas': len(filtro_adobo)
      })

    filtro_adobo = df[df['Codigo']== '010003']
    reporte_resumen.append({
      'Producto/Categoria': 'Adobo La Comadre 200Gr',
      'Cantidad Total': filtro_adobo['Cantidad'].sum(),
      'MontoBruto': filtro_adobo['MontoBruto'].sum()
      # 'Nro. Ventas': len(filtro_adobo)
    })
    
    filtro_total = df['Cantidad'].sum()
    filtro_monto_global = df['MontoBruto'].sum()
    
    df_reporte = pd.DataFrame(reporte_resumen)
    
    
    
    
    # -------- Vista de la consola --------
    console = Console()

    table = Table(title="📊Reporte De Ventas")
    table.add_column("Producto", style="cyan", no_wrap=True)
    table.add_column("Cant. Total", justify="right", style="magenta")
    table.add_column("Monto Bruto",justify="right", style="yellow")

    for index, row in df_reporte.iterrows():
      table.add_row(
        str(row['Producto/Categoria']),
        f"{row['Cantidad Total']:,.2f}",
        f"{row['MontoBruto']:,.2f}"
        # str(row['Nro. Ventas'])
      )
    table.add_row(
        "TOTAL GLOBAL",           # Primera Columna
        f"{filtro_total:,.2f}",     # Segunda Columna (El número calculado)
        "",                       # Tercera Columna (Vacia)
        style="bold white on blue" # Estilo: Letra blanca fondo azul (o solo "bold")
    )
    table.add_row(
        "MONTO GLOBAL",           # Primera Columna
        f"{filtro_monto_global:,.2f}",     # Segunda Columna (El número calculado)
        "",                       # Tercera Columna (Vacia)
        style="bold yellow on blue" # Estilo: Letra blanca fondo azul (o solo "bold")
    )
    console.print(table)

crea_reporte()
