import pandas as pd
import openpyxl
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
  "Pasta Allegri": "PASTA ALLEGRI",
  "Pasta Horizonte": "HORIZONTE",
  "Pasticho Allegri": "PASTICHO ALLEGRI",
  "Pasticho Mi Casa": "PASTICHO MI CASA",
  "Harina de Trigo Dulce Mar":  "HARINA DE TRIGO DULCE MAR",
  "Harina de Maiz Juana": "HARINA JUANA",
  "Harina de Trigo Robin Hood":"ROBIN HOOD",
  "Arroz Monica": "ARROZ MONICA",
  "Chococao": "BEBIDA CHOCOCAO",
}

productos_por_codigo = ['001009', '001011' , '001012']

#  Grupos de producto

allegri = ["Pasta Allegri", "Pasta Horizonte", "Pasticho Allegri","Allegri Especialidades" ,"Pasticho Mi Casa", "Harina de Trigo Dulce Mar" , "Devoluciones"]
monaca = ["Harina de Maiz Juana", "Harina de Trigo Robin Hood", "Arroz Monica", "Chococao", "Avena Lassie 400Gr", "Avena Lassie 800Gr", "Adobo La Comadre 200Gr"]

reporte_resumen = []


# ----------- Filtros-----------

# df[(df['Descripcion'].str.contains("ALLEGRI", case=False)) & (df['Cantidad'] > 0)]
def crea_reporte ():
  
    for nombre_producto , texto_buscar in productos.items():
      filtro = df[(df['Descripcion'].str.contains(texto_buscar, case=False, na=False)) & (df['Cantidad'] > 0) & (df["Cantidad"])]
      total_cantidad = filtro['Cantidad'].sum()
      total_bruto = filtro['MontoBruto'].sum()
      IVA = filtro['IVA'].sum()

      reporte_resumen.append({
        "Producto/Categoria": nombre_producto,
        "Cantidad Total": total_cantidad,
        "MontoBruto": total_bruto,
        "IVA": IVA
      })
      
    #  ---------- Filtros por codigo ----------
    
    filtro_allegri_especialidades = df[df["Codigo"].isin(productos_por_codigo)]
    reporte_resumen.append({
    'Producto/Categoria': 'Allegri Especialidades',
      'Cantidad Total': filtro_allegri_especialidades['Cantidad'].sum(),
      'MontoBruto': filtro_allegri_especialidades['MontoBruto'].sum(),
        "IVA": filtro_allegri_especialidades['IVA'].sum(),
    })
    
    filtro_devoluciones = df[df['Codigo']== '009001']
    reporte_resumen.append({
    'Producto/Categoria': 'Devoluciones',
      'Cantidad Total': filtro_devoluciones['Cantidad'].sum(),
      'MontoBruto': filtro_devoluciones['MontoBruto'].sum(),
        "IVA": filtro_devoluciones['IVA'].sum(),
    })
      
    filtro_avena_400 =df[df['Codigo']== '010002']
    reporte_resumen.append({
    'Producto/Categoria': 'Avena Lassie 400Gr',
      'Cantidad Total': filtro_avena_400['Cantidad'].sum(),
      'MontoBruto': filtro_avena_400['MontoBruto'].sum(),
        "IVA": filtro_avena_400['IVA'].sum(),


      })
    
    filtro_avena_800 =df[df['Codigo']== '010008']
    reporte_resumen.append({
    'Producto/Categoria': 'Avena Lassie 800Gr',
      'Cantidad Total': filtro_avena_800['Cantidad'].sum(),
      'MontoBruto': filtro_avena_800['MontoBruto'].sum(),
        "IVA": filtro_avena_800['IVA'].sum(),
      })

    filtro_adobo = df[df['Codigo']== '010003']
    reporte_resumen.append({
      'Producto/Categoria': 'Adobo La Comadre 200Gr',
      'Cantidad Total': filtro_adobo['Cantidad'].sum(),
      'MontoBruto': filtro_adobo['MontoBruto'].sum(),
        "IVA": filtro_adobo['IVA'].sum(),


    })
    
    filtro_total = df['Cantidad'].sum()
    filtro_monto_global = df['MontoBruto'].sum()
    
    df_reporte = pd.DataFrame(reporte_resumen)
    
    # total_monto_grupo_1 = df_reporte[df_reporte['Producto/Categoria'].isin(lista_grupo_1)]['MontoBruto'].sum()
    filtro_monto_allegri = df_reporte[df_reporte['Producto/Categoria'].isin(allegri)]['MontoBruto'].sum()
    filtro_monto_monaca = df_reporte[df_reporte['Producto/Categoria'].isin(monaca)]['MontoBruto'].sum()
    
    
    
    
    
    # -------- Vista de la consola --------
    console = Console()

    table = Table(title="📊Reporte De Ventas")
    table.add_column("Producto", style="cyan", no_wrap=True)
    table.add_column("Cant. Total", justify="right", style="magenta")
    table.add_column("Monto Bruto",justify="right", style="yellow")
    table.add_column("IVA",justify="right", style="red")
    

    for index, row in df_reporte.iterrows():
      table.add_row(
        str(row['Producto/Categoria']),
        f"{row['Cantidad Total']:,.2f}",
        f"{row['MontoBruto']:,.2f}",
        f"{row['IVA']}"
      )
    table.add_row(
        "TOTAL GLOBAL",           # Primera Columna
        f"{filtro_total:,.2f}",     # Segunda Columna (El número calculado)
        "-",                       # Tercera Columna (Vacia)
        "-",
        style="bold white on blue" # Estilo: Letra blanca fondo azul (o solo "bold")
    )
    table.add_row(
        "MONTO GLOBAL",           # Primera Columna
        f"{filtro_monto_global:,.2f}",     # Segunda Columna (El número calculado)
        "-",                       # Tercera Columna (Vacia)
        "-",
        style="bold yellow on blue" # Estilo: Letra blanca fondo azul (o solo "bold")
    )
    table.add_row(
      "TOTAL MONTO ALLEGRI: ",
      f"{filtro_monto_allegri:,.2f}",
      "-",
      "-",
      style="bold yellow on green"
    )
    table.add_row(
      "TOTAL MONTO MONACA: ",
      f"{filtro_monto_monaca:,.2f}",
      "-",
      "-",
      style="bold yellow on green"
    )

    console.print(table)
    
    #------- Vista Montos Totales -------

crea_reporte()