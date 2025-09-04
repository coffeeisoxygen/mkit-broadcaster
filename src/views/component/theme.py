import flet as ft


def build_theme_switch(is_dark: bool, on_change):
    theme_switch = ft.Switch(value=is_dark, scale=0.7, on_change=on_change)
    theme_toggle_row = ft.Row(
        [
            ft.Icon(ft.Icons.LIGHT_MODE, size=16),
            theme_switch,
            ft.Icon(ft.Icons.DARK_MODE, size=16),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    return theme_switch, theme_toggle_row
