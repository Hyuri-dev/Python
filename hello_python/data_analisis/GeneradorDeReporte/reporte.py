import pandas as pd
from rich.console import Console
from rich.table import Table


headers_novo = [
    "Codigo", "Descripcion", "Cantidad", "MontoBruto", 
    "Descuentos", "IVA", "Costo", "Utilidad", "PorcUtilidad"
]

df = pd.read_csv(
    r"C:\Users\Jefferson\desarrollo python\hello_python\Python\hello_python\data_analisis\GeneradorDeReporte\assets\files\Productosvendidos.TXT",
    sep='\t', 
    encoding='latin-1', 
    names=headers_novo, #Nombres nuevos para el header
    header=0,
    thousands='.', 
    decimal=',',
    index_col=False,         
    dtype={'Codigo': str}    #Codigo tiene que ser leido como str y no como objeto
)


productos_novo = {
  "Pasta Veneciana":"PASTA LA VENECIANA",
  "Pasticho Sirena":"PASTICHO LA SIRENA DIRECTO AL HORNO",
  "Aceite de Soya Portumesa":"ACEITE DE SOYA PORTUMESA 12 X 850 ML",
  "Aceite de Soya Portumesa":"ACEITE SOYA PORTUMESA 12 X 485ML",
}

especialiodades_novo = ['0050011', '005014']

reporte_resumen = []

def crear_reporte_novo():
  for nombre_producto , texto_buscar in productos_novo.items():
    filtro = df[(df['Descripcion'].str.contains(texto_buscar, case=False, na=False)) & (df['Cantidad']> 0)]
    total_cantidad = filtro['Cantidad'].sum()
    total_bruto = filtro['MontoBruto'].sum()
    IVA = filtro['IVA'].sum()

    reporte_resumen.append({
      "Producto":nombre_producto,
      "Cantidad Total": total_cantidad,
      "Monto Bruto": total_bruto,
      "IVA": IVA
    })

    df_reporte = pd.DataFrame(reporte_resumen)

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
    
  console.print(table)

crear_reporte_novo()