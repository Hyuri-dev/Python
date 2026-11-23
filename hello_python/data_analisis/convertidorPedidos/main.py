import asyncio
import flet as ft
from convertidor import procesar_pedidos


async def main(page: ft.Page):
    page.align_items = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    archivo_seleccionado = {"path": None}

    CLAVE_MAPEO = "convertidor_app.rutas"
    CLAVE_SALIDA = "convertidor_app.ruta_salida"
    CLAVE_MODELO = "convertidor_app.ruta_modelo"
    CLAVE_ZONA = "convertidor_app.ruta_zonas"
    prefs = ft.SharedPreferences()

    ruta_mapeo_inicial = await prefs.get(CLAVE_MAPEO)
    ruta_salida_inicial = await prefs.get(CLAVE_SALIDA)
    ruta_modelo_inicial = await prefs.get(CLAVE_MODELO)
    ruta_zona_modelo_inicial = await prefs.get(CLAVE_ZONA)

    txt_ruta = ft.Text(
        value=f"Ruta de mapeo de productos: {ruta_mapeo_inicial or 'No configurada'}",
        selectable=True,
        color=ft.Colors.BLUE_700,
    )
    txt_ruta_salida = ft.Text(
        value=f"Ruta de salida de archivos: {ruta_salida_inicial or 'No configurada'}",
        selectable=True,
        color=ft.Colors.BLUE_700,
    )
    txt_ruta_modelo = ft.Text(
        value=f"Ruta del modelo: {ruta_modelo_inicial or 'No configurada'}",
        selectable=True,
        color=ft.Colors.BLUE_700,
    )
    
    txt_ruta_zonas =ft.Text(
      value=f"Ruta para las zonas: {ruta_zona_modelo_inicial}" or "No configurada una ruta para leer las zonas",
      selectable=True,
      color=ft.Colors.BLUE_700,  
    )

    warning_text = ft.Text(value="Ningún Archivo Seleccionado", size=20)

    async def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            archivo_seleccionado["path"] = e.files[0].path
            warning_text.value = f"Archivo seleccionado: {archivo_seleccionado['path']}"
            boton_convertir.disabled = False
        else:
            warning_text.value = "Selección cancelada"
            archivo_seleccionado["path"] = None
            boton_convertir.disabled = True
        page.update()

    async def on_mapeo_selected(e: ft.ControlEvent):
        archivo = await ft.FilePicker().pick_files(
            allow_multiple=False,
            dialog_title="Seleccione el archivo de mapeo",
            allowed_extensions=["xlsx", "xls"],
        )
        if archivo:
            ruta = archivo[0].path
            await prefs.set(CLAVE_MAPEO, ruta)
            txt_ruta.value = f"Ruta de mapeo de productos: {ruta}"
            page.update()
    
    async def on_rutas_zonas_selected(e: ft.ControlEvent):
      archivo = await ft.FilePicker().pick_files(
        allow_multiple=False,
        allowed_extensions=['xlsx' , 'xls'],
        dialog_title="Seleccione el archivo de zonas"
      )
      
      if archivo:
        ruta =archivo[0].path
        await prefs.set(CLAVE_ZONA, ruta)
        txt_ruta_zonas.value = f"Ruta de zonas: {ruta}"
        page.update()

    async def on_ruta_salida_selected(e: ft.ControlEvent):
        carpeta = await ft.FilePicker().get_directory_path(
            dialog_title="Seleccione la carpeta para guardar el archivo"
        )
        if carpeta:
            await prefs.set(CLAVE_SALIDA, carpeta)
            txt_ruta_salida.value = f"Ruta de salida de archivos: {carpeta}"
            page.update()

    async def on_ruta_modelo_selected(e: ft.ControlEvent):
        archivo = await ft.FilePicker().pick_files(
            allow_multiple=False,
            dialog_title="Seleccione el archivo del modelo",
            allowed_extensions=["xlsx", "xls"],
        )
        if archivo:
            ruta = archivo[0].path
            await prefs.set(CLAVE_MODELO, ruta)
            txt_ruta_modelo.value = f"Ruta del modelo: {ruta}"
            page.update()

    async def convertir_archivo(e):
        # 1. Leer siempre los valores actualizados desde SharedPreferences
        ruta_pedidos = archivo_seleccionado["path"]
        ruta_mapeo = await prefs.get(CLAVE_MAPEO)
        ruta_salida = await prefs.get(CLAVE_SALIDA)
        ruta_modelo = await prefs.get(CLAVE_MODELO)
        ruta_zonas = await prefs.get(CLAVE_ZONA)

        # 2. Validar que las 4 rutas existan antes de llamar a procesar_pedidos
        if not all([ruta_pedidos, ruta_mapeo, ruta_salida, ruta_modelo, ruta_zonas]):
            warning_text.value = "⚠️ Faltan rutas por configurar en el menú superior."
            warning_text.color = ft.Colors.AMBER_700
            page.update()
            return

        warning_text.value = "Procesando el archivo, espere..."
        warning_text.color = ft.Colors.BLUE_700
        boton_convertir.disabled = True
        page.update()

        try:
            # 3. Ejecutar en hilo separado sin bloquear la UI
            salida = await asyncio.to_thread(
                procesar_pedidos,
                ruta_pedidos,
                ruta_mapeo,
                ruta_salida,
                ruta_modelo,
                ruta_zonas,
            )
            warning_text.value = "✅ Archivo guardado como: pedidos_convertidos_diacenca.xlsx"
            warning_text.color = ft.Colors.GREEN_700
            if salida["no_mapeados"]:
                lista_faltantes = "\n".join(f"• {p}" for p in salida["no_mapeados"])
                dlg = ft.AlertDialog(
                    title="⚠️ Productos omitidos (sin mapeo)",
                    content=ft.Text(
                        f"El archivo se genero, pero estos productos no estan en tu lista de mapeo:\n\n{lista_faltantes}",
                        selectable=True,
                    ),
                    actions=[
                        ft.TextButton("Entendido", on_click=lambda _: page.close(dlg))
                    ],
                )
                page.open(dlg)
        except Exception as ex:
            warning_text.value = f"❌ Error durante la conversión: {ex}"
            warning_text.color = ft.Colors.RED_700
        finally:
            boton_convertir.disabled = False
            page.update()

    page.appbar = ft.AppBar(
        bgcolor=ft.Colors.GREY_900,
        leading=ft.Icon(ft.Icons.MENU),
        leading_width=20,
        title=ft.Text(
            "Convertidor de Pedidos",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        elevation=0,
        actions=[
            ft.PopupMenuButton(
                key="popup",
                items=[
                    ft.PopupMenuItem(
                        content="Configurar ruta de plantilla",
                        on_click=on_mapeo_selected,
                    ),
                    ft.PopupMenuItem(
                        content="Configurar ruta de salida",
                        on_click=on_ruta_salida_selected,
                    ),
                    ft.PopupMenuItem(
                        content="Configurar ruta del modelo",
                        on_click=on_ruta_modelo_selected,
                    ),
                    ft.PopupMenuItem(
                        content="Configurar ruta para lectura de zonas",
                        on_click=on_rutas_zonas_selected,
                    ),
                ],
            )
        ],
    )

    title = ft.Text(
        value="Ingrese el archivo de pedidos a convertir",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    file_picker = ft.FilePicker(on_result=on_files_selected)
    page.services.append(file_picker)

    boton_abrir = ft.Button(
        "Buscar Archivo",
        icon=ft.Icons.UPLOAD_FILE,
        action=ft.PickFiles(
            file_picker,
            allow_multiple=False,
            dialog_title="Seleccione un archivo",
            allowed_extensions=["xlsx", "xls"],
        ),
    )

    boton_convertir = ft.Button(
        "Convertir Archivo",
        icon=ft.Icons.PLAY_ARROW,
        disabled=True,
        on_click=convertir_archivo,
    )

    page.add(
        title,
        warning_text,
        boton_abrir,
        ft.Divider(height=20, color=ft.Colors.BLUE_50),
        boton_convertir,
        txt_ruta,
        txt_ruta_salida,
        txt_ruta_modelo,
        txt_ruta_zonas
    )


ft.run(main)
