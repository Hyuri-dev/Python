import pandas as pd
import openpyxl

route ="C:\\Users\\Personal\\Downloads\\pedidos.xlsx"

encabezados = ["Nombre Cliente" , "Nombre Producto" ,"Cantidad Pedida","Monto pedido" ]

df = pd.read_excel(route, header=9, usecols=encabezados)


# filtro_cliente = {
#   cliente: datos for cliente, datos in df.groupby("Nombre Cliente")
# }

df_filtrado = (
  df.groupby("Nombre Cliente", as_index=False).agg(
    {
      "Nombre Producto": lambda x: ",".join(x.astype(str)),
      "Cantidad Pedida":"sum",
      "Monto pedido":"sum",
    }
  )
)
listado = list(df.columns)

df_filtrado.to_excel("resumen_pedido_prueba.xlsx", index=False)

# print(df)
# print(listado)
# print(filtro_cliente)
print(df_filtrado)

