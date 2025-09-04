import asyncio
from datetime import datetime

import flet as ft
from loguru import logger

from views.component.header import build_header
from views.component.sidebar import build_sidebar
from views.pages.broadcast import broadcast_page
from views.pages.dashboard import dashboard_page
from views.pages.profile import profile_page
from views.pages.settings import settings_page


async def main(page: ft.Page):
    clock_text = ft.Text(value="", size=15, weight=ft.FontWeight.W_600)

    async def update_clock():
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            clock_text.value = now
            page.update()
            await asyncio.sleep(1)

    page.run_task(update_clock)
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
        ("Profile", profile_page),
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
        # update icon
        if nav_rail.current.extended:
            sidebar_toggle_btn.icon = ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED
        else:
            sidebar_toggle_btn.icon = ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED
        page.update()

    # State for theme mode, switch kecil dan di pojok kiri bawah
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    theme_switch = ft.Switch(value=is_dark, scale=0.7)

    def on_theme_toggle(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        )
        logger.info(f"Theme changed to: {page.theme_mode}")
        page.update()

    theme_switch.on_change = on_theme_toggle

    theme_toggle_row = ft.Row(
        [
            ft.Icon(ft.Icons.LIGHT_MODE, size=16),
            theme_switch,
            ft.Icon(ft.Icons.DARK_MODE, size=16),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Buat IconButton sebagai variabel agar bisa diubah iconnya
    sidebar_toggle_btn = ft.IconButton(
        icon=ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED,
        tooltip="Toggle Navigation",
        on_click=toggle_sidebar,
    )

    nav = build_sidebar(
        nav_rail,
        selected_index,
        on_nav_change,
        toggle_sidebar,
        sidebar_toggle_btn,
    )

    header = build_header(
        "MKIT Broadcaster",
        clock_text,
        theme_toggle_row,
    )

    page.add(
        ft.Column(
            [
                header,
                ft.Row(
                    [
                        nav,
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            content, expand=True, alignment=ft.alignment.center
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
        )
    )

    # Initial logger bind for default page
    logger.bind(active_page=pages[0][0]).info(f"Active page: {pages[0][0]}")


if __name__ == "__main__":
    logger.info("Starting Flet app...")
    ft.app(target=main, view=ft.AppView.FLET_APP)
