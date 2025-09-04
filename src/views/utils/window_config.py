import flet as ft


def configure_window(page: ft.Page):
    page.window.width = 900
    page.window.height = 600
    page.window.min_width = 700
    page.window.min_height = 500
    page.window.resizable = True
    page.window.alignment = ft.alignment.center
