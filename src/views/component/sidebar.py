from collections.abc import Callable

import flet as ft
from flet import ControlEvent, IconButton, NavigationRail, Ref

from views.pages.registry import SIDEBAR_DESTINATIONS


def build_sidebar(
    nav_rail_ref: Ref[NavigationRail],
    selected_index_ref: Ref[int],
    on_nav_change: Callable[[ControlEvent], None],
    sidebar_toggle_btn: IconButton,
) -> NavigationRail:
    """Reusable sidebar component."""
    return NavigationRail(
        ref=nav_rail_ref,
        selected_index=selected_index_ref.current,
        on_change=on_nav_change,
        label_type=ft.NavigationRailLabelType.NONE,
        extended=False,
        min_width=60,
        min_extended_width=150,
        group_alignment=-0.9,
        leading=sidebar_toggle_btn,
        destinations=SIDEBAR_DESTINATIONS,
    )
