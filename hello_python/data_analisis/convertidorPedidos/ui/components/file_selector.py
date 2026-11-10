from pathlib import Path
from typing import Callable, List, Optional
import flet as ft

Icons = getattr(ft, "Icons", getattr(ft, "icons", None))
Colors = getattr(ft, "Colors", getattr(ft, "colors", None))


def show_snackbar(page: ft.Page, message: str, bgcolor: Optional[str] = None) -> None:
    """Muestra un ft.SnackBar de forma compatible con distintas versiones de Flet."""
    snack = ft.SnackBar(
        content=ft.Text(message, color=Colors.WHITE if bgcolor else None),
        bgcolor=bgcolor,
        open=True,
    )
    if hasattr(page, "open"):
        try:
            page.open(snack)
            return
        except Exception:
            pass
    page.snack_bar = snack
    page.update()


class FileSelector(ft.Column):
    """
    Componente reutilizable que combina un campo de texto interactivo
    con botones de exploración de archivos y/o carpetas mediante ft.FilePicker.
    """

    def __init__(
        self,
        page: ft.Page,
        label: str,
        value: str = "",
        hint_text: str = "",
        mode: str = "file",  # "file", "directory", o "both"
        allowed_extensions: Optional[List[str]] = None,
        on_change: Optional[Callable[[str], None]] = None,
        helper_text: Optional[str] = None,
    ) -> None:
        super().__init__(spacing=4)
        self.host_page = page
        self.mode = mode
        self.allowed_extensions = allowed_extensions or ["xlsx", "xlsm", "xls"]
        self.on_change_callback = on_change

        self.file_picker = ft.FilePicker(on_result=self._on_picker_result)
        if self.file_picker not in self.host_page.overlay:
            self.host_page.overlay.append(self.file_picker)

        self.text_field = ft.TextField(
            label=label,
            value=value,
            hint_text=hint_text,
            expand=True,
            dense=True,
            border_radius=8,
            on_change=self._handle_text_change,
        )

        buttons: List[ft.Control] = []
        if mode in ("file", "both"):
            buttons.append(
                ft.ElevatedButton(
                    text="Archivo",
                    icon=Icons.UPLOAD_FILE,
                    tooltip="Seleccionar archivo",
                    on_click=self._pick_file,
                )
            )
        if mode in ("directory", "both"):
            buttons.append(
                ft.OutlinedButton(
                    text="Carpeta",
                    icon=Icons.FOLDER_OPEN,
                    tooltip="Seleccionar carpeta",
                    on_click=self._pick_directory,
                )
            )

        self.controls = [
            ft.Row(
                controls=[self.text_field, *buttons],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]

    @property
    def value(self) -> str:
        return (self.text_field.value or "").strip()

    @value.setter
    def value(self, new_val: str) -> None:
        self.text_field.value = new_val
        self.text_field.error_text = None

    def set_error(self, error_message: Optional[str]) -> None:
        self.text_field.error_text = error_message

    def _get_initial_directory(self) -> Optional[str]:
        current = self.value
        if not current:
            return None
        path = Path(current)
        if path.is_dir():
            return str(path)
        if path.parent.is_dir():
            return str(path.parent)
        return None

    def _pick_file(self, _: ft.ControlEvent) -> None:
        initial_dir = self._get_initial_directory()
        self.file_picker.pick_files(
            dialog_title="Seleccionar archivo Excel",
            allow_multiple=False,
            allowed_extensions=self.allowed_extensions,
            initial_directory=initial_dir,
        )

    def _pick_directory(self, _: ft.ControlEvent) -> None:
        initial_dir = self._get_initial_directory()
        self.file_picker.get_directory_path(
            dialog_title="Seleccionar carpeta",
            initial_directory=initial_dir,
        )

    def _on_picker_result(self, e: ft.FilePickerResultEvent) -> None:
        selected_path: Optional[str] = None
        if getattr(e, "files", None) and len(e.files) > 0:
            selected_path = e.files[0].path
        elif getattr(e, "path", None):
            selected_path = e.path

        if selected_path:
            self.text_field.value = selected_path
            self.text_field.error_text = None
            if self.on_change_callback:
                self.on_change_callback(selected_path)
            self.host_page.update()

    def _handle_text_change(self, e: ft.ControlEvent) -> None:
        self.text_field.error_text = None
        if self.on_change_callback:
            self.on_change_callback(self.value)
        self.host_page.update()
