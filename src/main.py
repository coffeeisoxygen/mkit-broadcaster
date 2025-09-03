import flet as ft
from loguru import logger

from views.broadcast import broadcast_page
from views.dashboard import dashboard_page
from views.settings import settings_page


async def main(page: ft.Page):
    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Atur ukuran window agar proporsional di desktop
    page.window.width = 900
    page.window.height = 600
    page.window.min_width = 700
    page.window.min_height = 500
    page.window.resizable = True
    page.window.alignment = ft.alignment.center

    nav_rail = ft.Ref[ft.NavigationRail]()
    selected_index = ft.Ref[int]()
    selected_index.current = 0

    pages = [
        ("Dashboard", dashboard_page),
        ("Broadcast", broadcast_page),
        ("Settings", settings_page),
    ]
    # Konten utama dengan lebar maksimal dan padding
    content = ft.Container(
        content=pages[0][1](page),
        expand=True,
        width=700,
        padding=20,
        alignment=ft.alignment.center,
    )

    def on_nav_change(e):
        idx = e.control.selected_index
        selected_index.current = idx
        content.content = pages[idx][1](page)
        # Bind logger with active page info
        logger.bind(active_page=pages[idx][0]).info(f"Active page: {pages[idx][0]}")
        page.update()

    def toggle_sidebar(e):
        nav_rail.current.extended = not nav_rail.current.extended
        page.update()

    nav = ft.NavigationRail(
        ref=nav_rail,
        selected_index=selected_index.current,
        on_change=on_nav_change,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=False,
        min_width=60,
        min_extended_width=150,
        group_alignment=-0.9,
        leading=ft.IconButton(
            icon=ft.Icons.MENU, tooltip="Toggle Navigation", on_click=toggle_sidebar
        ),
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.SEND, label="Broadcast"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Settings"),
        ],
    )

    page.add(
        ft.Row(
            [
                nav,
                ft.VerticalDivider(width=1),
                ft.Container(content, expand=True, alignment=ft.alignment.center),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    # Initial logger bind for default page
    logger.bind(active_page=pages[0][0]).info(f"Active page: {pages[0][0]}")


if __name__ == "__main__":
    logger.info("Starting Flet app...")
    ft.app(target=main, view=ft.AppView.FLET_APP)
