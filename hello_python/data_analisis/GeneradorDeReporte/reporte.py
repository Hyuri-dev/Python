import pandas as pd
from rich.console import Console
from rich.table import Table


headers_novo = [
    "Codigo", "Descripcion", "Cantidad", "Pendiente" ,"MontoBruto", 
    "Descuentos", "IVA", "Costo", "Utilidad", "PorcUtilidad", "Existencia"
]

df = pd.read_csv(
    r"\\SERVIDOR\a2Apps\a2NovoEuropa\a2Admin\Empre001\REPORTS\Productosvendidos.TXT",
    sep='\t', 
    encoding='latin-1', #formato del texto, como hay letras con tildes, usamos el formato latin-1 para que estas sean reconocidas 
    names=headers_novo, #Nombres nuevos para el header
    header=0,
    thousands='.', 
    decimal=',',
    index_col=False,         
    dtype={'Codigo': str}    #Codigo tiene que ser leido como str y no como objeto
) 

# Variables Para la busqueda de los productos (Contienen Maps para poder iterar entre cada producto)
productos_novo = {
  "Pasta Veneciana":"PASTA LA VENECIANA",
  "Pasticho Sirena":"PASTICHO LA SIRENA DIRECTO AL HORNO",
  "Aceite de Soya Portumesa Grande":"ACEITE SOYA PORTUMESA 12 X 850 ML",
  "Aceite de Soya Portumesa Pequeño":"ACEITE SOYA PORTUMESA 12 X 485ML",
}

especialidades_novo = {"Pasta Linguini":'0050011',
                      "Fideos la Sirena":"005014"}

productos_giralda = {
  "Pure de Tomate Tomatodo 490Gr":"012001",
  "Salsa Napolitana 490Gr":"012002",
  "Mayonesa 175Gr":"012003",
  "Vinagre 500Ml":"012004",
  "Vinagre 3.78L":"012005",
  "Salsa de Ajo 150 CC":"012006",
  "Salsa Inglesa 150 CC":"012007",
  "Salsa de Soya 150 CC":"012008",
  "Tripack de Salsas 150 CC":"012009",
  "Alcaparras 500Gr":"012010",
  "Aceitunas Enteras 500Gr":"012011",
  "Salsa de Ajo 3.78L":"012012",
  "Salsa Inglesa 3.78L":"012013",
  "Salsa de Soya 3.78L":"012014",
  "Salsa de Tomate Ketchup 397Gr":"012015",
  "Salsa de Tomate Ketchup Hot 397Gr":"012016",
  "Salsa para Carne 79 380Gr":"012017",
  "Pure de Tomate Tomatodo 190Gr":"012018",
  "Salsa Napolitana 190Gr":"012019",
  "Vinagre 1000Ml":"012020",
  "Alcaparras 200Gr":"012021",
  "Aceitunas Rellenas 200Gr":"012022",
  "Aceitunas Rellenas 490Gr":"012023",
  "Mayonesa 445Gr":"012024",
  "Mostaza Premium 185Gr":"012026",
  "Salsa Bolognesa 190Gr":"012027",
  "Salsa Bolognesa 490Gr":"012028",
  "Salsa a Base de Tomates Hacienda 380Gr":"012030",
}

reporte_resumen = []

def crear_reporte_novo():
  for nombre_producto , texto_buscar in productos_novo.items():
    filtro = df[(df['Descripcion'].str.contains(texto_buscar, case=False, na=False)) & (df['Cantidad']> 0)]
    total_cantidad = filtro['Cantidad'].sum()
    if total_cantidad > 0:
      total_bruto = filtro['MontoBruto'].sum()
      IVA = filtro['IVA'].sum()
      
      reporte_resumen.append({
        "Producto":nombre_producto,
        "Cantidad Total": total_cantidad,
        "Monto Bruto": total_bruto,
        "IVA": IVA
      })
    
    
      #---- Especialidades Veneciana ----
      
  for nombre_especialidad, codigo_buscar in especialidades_novo.items():
    filtro_especialidades = df[(df['Codigo'].str.contains(codigo_buscar, case=False, na=False)) & (df['Cantidad']>0)]
    total_cantidad_Especialidad = filtro_especialidades['Cantidad'].sum()
    
    if total_cantidad_Especialidad > 0:
      total_bruto_Especialidad = filtro_especialidades['MontoBruto'].sum()

      reporte_resumen.append({
        "Producto":nombre_especialidad,
        "Cantidad Total": total_cantidad_Especialidad,
        "Monto Bruto": total_bruto_Especialidad,
      })
      
      #---- Especialidades Giralda ----
  for nombre_giralda , codigo_buscar_giralda in productos_giralda.items():
    filtro_monaca = df[(df['Codigo'].str.contains(codigo_buscar_giralda, case=False , na=False) & (df['Cantidad']>0))]
    total_cantidad_giralda = filtro_monaca['Cantidad'].sum()
    
    if total_cantidad_giralda >0:
      total_bruto_giralda = filtro_monaca['MontoBruto'].sum()
      IVA_GIRALDA = filtro_monaca['IVA'].sum()

      
      reporte_resumen.append({
        "Producto": nombre_giralda,
        "Cantidad Total": total_cantidad_giralda,
        "Monto Bruto": total_bruto_giralda,
        "IVA":IVA_GIRALDA ,
      })
  
  devoluciones = df[df['Codigo']== '009001']
  reporte_resumen.append({
    'Producto': 'Devoluciones',
      'Cantidad Total': devoluciones['Cantidad'].sum(),
      'Monto Bruto': devoluciones['MontoBruto'].sum(),
        "IVA": devoluciones['IVA'].sum(),
    })

  df_reporte = pd.DataFrame(reporte_resumen)
  
  monto_global = df_reporte['Monto Bruto'].sum()
  total_productos_global =df_reporte['Cantidad Total'].sum()
  
  # print(f"Monto global: {monto_global} y un total de productos: {total_productos_global}")

  if not df_reporte.empty:
    console = Console()

    table = Table(title="📊Reporte De Ventas")
    table.add_column("Producto", style="cyan", no_wrap=True)
    table.add_column("Cant. Total", justify="right", style="magenta")
    table.add_column("Monto Bruto",justify="right", style="yellow")
    table.add_column("IVA",justify="right", style="red")

    for index, row in df_reporte.iterrows():
        table.add_row(
          str(row['Producto']),
          f"{row['Cantidad Total']:,.2f}",
          f"{row['Monto Bruto']:,.2f}",
          f"{row['IVA']}"
        )
    table.add_row(
          "TOTAL MONTO: ",
          f"{monto_global:,.2f}",
          "-",
          "-",
          style="bold yellow on green"
        )
    table.add_row(
          "TOTAL PRODUCTOS: ",
          f"{total_productos_global:,.2f}",
          "-",
          "-",
          style="bold yellow on green"
        )

    console.print(table)

crear_reporte_novo()