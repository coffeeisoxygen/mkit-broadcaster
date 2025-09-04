import flet as ft


def main_app(page: ft.Page):
    """Entry point utama aplikasi Flet MKIT Broadcaster.

    Mengatur layout utama dari builder modular.
    """
    import asyncio

    import flet as ft

    from views.main_layout import build_main_layout

    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT
    layout = asyncio.run(build_main_layout(page))
    page.add(layout)
