import flet as ft

from views.component.header import build_header
from views.component.sidebar import build_sidebar
from views.component.theme import build_theme_switch
from views.events.main_events import (
    MainPageState,
    bind_logger_active_page,
    on_nav_change,
    on_theme_toggle,
    toggle_sidebar,
)
from views.pages.registry import PAGES
from views.services.clock_service import run_clock
from views.utils.window_config import configure_window


def build_main_layout(page: ft.Page):
    state = MainPageState(page)
    configure_window(page)
    clock_text = ft.Text(value="", size=15, weight=ft.FontWeight.W_600)
    page.run_task(run_clock, clock_text, page)
    state.pages = PAGES
    state.content = ft.Container(
        content=state.pages[0][1](page),
        expand=True,
        width=700,
        padding=20,
        alignment=ft.alignment.center,
    )
    # Theme
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    state.theme_switch, theme_toggle_row = build_theme_switch(
        is_dark, lambda e: on_theme_toggle(e, state)
    )
    # Sidebar toggle btn
    state.sidebar_toggle_btn = ft.IconButton(
        icon=ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED,
        tooltip="Toggle Navigation",
        on_click=lambda e: toggle_sidebar(e, state),
    )
    nav = build_sidebar(
        state.nav_rail,
        state.selected_index,
        lambda e: on_nav_change(e, state),
        lambda e: toggle_sidebar(e, state),
        state.sidebar_toggle_btn,
    )
    header = build_header(
        "MKIT Broadcaster",
        clock_text,
        theme_toggle_row,
    )
    layout = ft.Column(
        [
            header,
            ft.Row(
                [
                    nav,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        state.content, expand=True, alignment=ft.alignment.center
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        expand=True,
    )
    bind_logger_active_page(state.pages[0][0])
    return layout
