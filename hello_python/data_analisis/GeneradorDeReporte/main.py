import pandas as pd
import openpyxl as opyxl
from openpyxl import load_workbook
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
import os

load_dotenv()


filas = {
  "PASTA HORIZONTE": "A1",
  "PASTA ALLEGRI": "A22"
}

# ----------- Headers del dataframe nuevo -----------
nombres_limpios = [
    "Codigo", "Descripcion", "Cantidad", "Pendiente", "MontoBruto", 
    "Descuentos", "IVA", "Costo", "Utilidad", "PorcUtilidad", "Existencia"
]



#  Data frame 



ubicacion_reporte = {
        "JULIO MEDINA": os.getenv("JULIO"),
        "VICTOR FERREIRA": os.getenv("VICTOR_FERREIRA"),
        "LUIS DURAN": os.getenv("LUIS"),
        "ROBERT RODRIGUEZ": os.getenv("ROBERT"),
        "YOSEMITH PONCE": os.getenv("YOSEMITH"),
        "JESUS HERNANDEZ": os.getenv("JESUS"),
        "VICTOR GONZALES": os.getenv("VICTOR_GONZALES")
      }

productos = {
  "Pasta Allegri": "PASTA ALLEGRI",
  "Pasta Horizonte": "HORIZONTE",
  "Pasticho Allegri": "PASTICHO ALLEGRI",
  "Pasticho Mi Casa": "PASTICHO MI CASA",
  "Harina de Trigo Dulce Mar":  "HARINA DE TRIGO DULCE MAR",
  "Harina de Maiz Juana": "HARINA JUANA",
  "Harina de Trigo Robin Hood":"ROBIN HOOD",
  "Harina de Cachapa Juana": "MEZCLA CACHAPA JUANA",
  "Arroz Monica": "ARROZ MONICA",
  "Chococao": "BEBIDA CHOCOCAO",
  "Margarina Juana":"MARGARINA JUANA",
  "Aceite Vegetal": "ACEITE VEGETAL LA COMADRE",
  "Avena Robin Hood":"AVENA ROBIN HOOD HOJ BOLSA"
}




productos_por_codigo = ['001009', '001011' , '001012']

#  Grupos de producto

allegri = ["Pasta Allegri", "Pasta Horizonte", "Pasticho Allegri","Allegri Especialidades" ,"Pasticho Mi Casa", "Harina de Trigo Dulce Mar" , ]
monaca = ["Harina de Maiz Juana","Harina de Cachapa Juana" ,"Harina de Trigo Robin Hood", "Arroz Monica", "Chococao", "Avena Lassie 400Gr", "Avena Lassie 800Gr", "Adobo La Comadre 200Gr", "Margarina Juana", "Aceite Vegetal"]

reporte_resumen = []



# ----------- Filtros-----------

# df[(df['Descripcion'].str.contains("ALLEGRI", case=False)) & (df['Cantidad'] > 0)]

def crea_reporte ():
  
  
  for vendedor , ruta in  ubicacion_reporte.items():
    report_vendedor = []
    print(f"procesando a: {vendedor}")
    if ruta is None:
        raise ValueError(f"La ruta para el vendedor '{vendedor}' no está definida. Verifica las variables de entorno.")
    df = pd.read_csv(
        ruta,
        sep='\t',   
        encoding='latin-1', 
        names=nombres_limpios, #Nombres nuevos para el header
        header=0,
        thousands='.', 
        decimal=',',
        index_col=False,          
        dtype={'Codigo': str}    #Codigo tiene que ser leido como str y no como objeto
    )
    for nombre_producto , texto_buscar in productos.items():
      filtro = df[(df['Descripcion'].str.contains(texto_buscar, case=False, na=False)) & (df['Cantidad'] > 0) & (df["Cantidad"])]
      total_cantidad = filtro['Cantidad'].sum()
      total_bruto = filtro['MontoBruto'].sum()
      IVA = filtro['IVA'].sum()
      

      report_vendedor.append({
        "Vendedor": vendedor,
        "Producto/Categoria": nombre_producto,    
        "Cantidad Total": total_cantidad,
        "MontoBruto": total_bruto,
        "IVA": IVA
      })
      
      
      # print(reporte_resumen[0]["Cantidad Total"])
      
      
      
    #  ---------- Filtros por codigo ----------
    
    filtro_allegri_especialidades = df[df["Codigo"].isin(productos_por_codigo)]
    report_vendedor.append({
    'Producto/Categoria': 'Allegri Especialidades',
      'Cantidad Total': filtro_allegri_especialidades['Cantidad'].sum(),
      'MontoBruto': filtro_allegri_especialidades['MontoBruto'].sum(),
        "IVA": filtro_allegri_especialidades['IVA'].sum(),
    })
    
    filtro_devoluciones = df[df['Codigo']== '009001']
    report_vendedor.append({
    'Producto/Categoria': 'Devoluciones',
      'Cantidad Total': filtro_devoluciones['Cantidad'].sum(),
      'MontoBruto': filtro_devoluciones['MontoBruto'].sum(),
        "IVA": filtro_devoluciones['IVA'].sum(),
    })
      
    filtro_avena_400 =df[df['Codigo']== '010002']
    report_vendedor.append({
    'Producto/Categoria': 'Avena Lassie 400Gr',
      'Cantidad Total': filtro_avena_400['Cantidad'].sum(),
      'MontoBruto': filtro_avena_400['MontoBruto'].sum(),
        "IVA": filtro_avena_400['IVA'].sum(),
      })
    
    filtro_avena_800 =df[df['Codigo']== '010008']
    report_vendedor.append({
    'Producto/Categoria': 'Avena Lassie 800Gr',
      'Cantidad Total': filtro_avena_800['Cantidad'].sum(),
      'MontoBruto': filtro_avena_800['MontoBruto'].sum(),
        "IVA": filtro_avena_800['IVA'].sum(),
      })

    filtro_adobo = df[df['Codigo']== '010003']
    report_vendedor.append({
      'Producto/Categoria': 'Adobo La Comadre 200Gr',
      'Cantidad Total': filtro_adobo['Cantidad'].sum(),
      'MontoBruto': filtro_adobo['MontoBruto'].sum(),
        "IVA": filtro_adobo['IVA'].sum(),


    })
    
    filtro_total = df['Cantidad'].sum()
    filtro_monto_global = df['MontoBruto'].sum()
    
    # df_reporte = pd.DataFrame(report_vendedor)
    df_reporte_individual = pd.DataFrame(report_vendedor)
    
    filtro_monto_allegri = df_reporte_individual[df_reporte_individual['Producto/Categoria'].isin(allegri)]['MontoBruto'].sum()
    filtro_monto_monaca = df_reporte_individual[df_reporte_individual['Producto/Categoria'].isin(monaca)]['MontoBruto'].sum()

    # try:
    #   wb = load_workbook(filename=os.getenv("REPORTE"))
    #   ws = wb.active

    #   value = ws['A5'].value
    #   # sheet_ranges = wb['A5']
    #   print(f"Valor: {value}")
    # except ValueError,NameError,RuntimeError:
    #   print("Error al abrir el archivo de excel")


    

    
    
    # -------- Vista de la consola --------
    console = Console()

    table = Table(title="📊Reporte De Ventas")
    table.add_column("Producto", style="cyan", no_wrap=True)
    table.add_column("Cant. Total", justify="right", style="magenta")
    table.add_column("Monto Bruto",justify="right", style="yellow")
    table.add_column("IVA",justify="right", style="red")
    

    for index, row in df_reporte_individual.iterrows():
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

crea_reporte()