import flet as ft

from views.main_layout import build_main_layout


def main_app(page: ft.Page):
    """Entry point utama aplikasi Flet MKIT Broadcaster.

    Mengatur layout utama dari builder modular.
    """
    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT
    layout = build_main_layout(page)
    page.add(layout)
