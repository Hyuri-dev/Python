from src.modules.productos import add_product , get_products


if __name__ == "__main__":
    # add_product("Zapato kike", 12.4)

    lista = get_products()
    for p in lista:
        print(f"- ID: {p['id']} | {p['nombre']}, | Precio: Bs{p['precio_base']}")

