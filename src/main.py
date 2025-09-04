import flet as ft
from loguru import logger

from views.broadcast import broadcast_page
from views.dashboard import dashboard_page
from views.profile import profile_page
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

    nav = ft.NavigationRail(
        ref=nav_rail,
        selected_index=selected_index.current,
        on_change=on_nav_change,
        label_type=ft.NavigationRailLabelType.NONE,
        extended=False,
        min_width=60,
        min_extended_width=150,
        group_alignment=-0.9,
        leading=sidebar_toggle_btn,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.SEND, label="Broadcast"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Settings"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Profile"),
        ],
        # trailing dihapus, theme switch akan dipindah ke pojok kiri bawah window
    )

    # Header di atas, berisi judul dan theme switch di kanan atas
    header = ft.Container(
        ft.Row(
            [
                ft.Text(value="MKIT Broadcaster", size=17, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=theme_toggle_row,
                    alignment=ft.alignment.center_right,
                    padding=0,
                    width=140,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(left=20, right=20, top=12, bottom=8),
        bgcolor="#1dd0d6",  # warna permukaan terang
        shadow=ft.BoxShadow(blur_radius=8, color="#0D010121", offset=(0, 2)),
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
