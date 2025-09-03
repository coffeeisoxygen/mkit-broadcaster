import flet as ft

from views.broadcast import broadcast_page
from views.dashboard import dashboard_page
from views.settings import settings_page


async def main(page: ft.Page):
    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT

    selected_index = ft.Ref[int]()
    selected_index.current = 0

    pages = [
        ("Dashboard", dashboard_page),
        ("Broadcast", broadcast_page),
        ("Settings", settings_page),
    ]
    content = ft.Container(content=pages[0][1](page), expand=True)

    def on_nav_change(e):
        idx = e.control.selected_index
        selected_index.current = idx
        content.content = pages[idx][1](page)
        page.update()

    # NavigationRail versi mini
    nav = ft.NavigationRail(
        selected_index=selected_index.current,
        on_change=on_nav_change,
        label_type=ft.NavigationRailLabelType.ALL,  # bisa: NONE, SELECTED, ALL
        extended=False,  # biar ga panjang full
        min_width=60,  # lebar minimal (ikon doang)
        group_alignment=-0.9,  # biar item naik ke atas
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
                content,
            ],
            expand=True,
        )
    )


ft.app(target=main, view=ft.AppView.FLET_APP)
