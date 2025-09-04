import flet as ft


def build_sidebar(
    nav_rail_ref,
    selected_index_ref,
    on_nav_change,
    on_toggle,
    sidebar_toggle_btn,
) -> ft.NavigationRail:
    """Reusable sidebar component."""
    return ft.NavigationRail(
        ref=nav_rail_ref,
        selected_index=selected_index_ref.current,
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
    )
