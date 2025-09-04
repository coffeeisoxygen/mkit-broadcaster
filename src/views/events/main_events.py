import flet as ft
from loguru import logger


class MainPageState:
    """State object for main page UI and logic."""

    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.nav_rail: ft.Ref[ft.NavigationRail] = ft.Ref[ft.NavigationRail]()
        self.selected_index: ft.Ref[int] = ft.Ref[int]()
        self.selected_index.current = 0
        self.sidebar_toggle_btn: ft.IconButton | None = None
        self.theme_switch: ft.Switch | None = None
        self.content: ft.Container | None = None
        self.pages: list | None = None


# Event Handlers


def on_nav_change(e: ft.ControlEvent, state: MainPageState) -> None:
    """Handle navigation change event."""
    if state.pages and state.content:
        idx = e.control.selected_index
        state.selected_index.current = idx
        state.content.content = state.pages[idx][1](state.page)
        bind_logger_active_page(state.pages[idx][0])
        state.page.update()


def toggle_sidebar(_: ft.ControlEvent, state: MainPageState) -> None:
    """Handle sidebar toggle event."""
    if state.nav_rail.current:
        state.nav_rail.current.extended = not state.nav_rail.current.extended
        # update icon
        if state.sidebar_toggle_btn:
            if state.nav_rail.current.extended:
                state.sidebar_toggle_btn.icon = ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED
            else:
                state.sidebar_toggle_btn.icon = ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED
        state.page.update()


def on_theme_toggle(_: ft.ControlEvent, state: MainPageState) -> None:
    """Handle theme toggle event."""
    if state.theme_switch:
        state.page.theme_mode = (
            ft.ThemeMode.DARK if state.theme_switch.value else ft.ThemeMode.LIGHT
        )
        logger.info(f"Theme changed to: {state.page.theme_mode}")
        state.page.update()


# Logger helper


def bind_logger_active_page(page_name: str) -> None:
    """Bind logger with active page info."""
    logger.bind(active_page=page_name).info(f"Active page: {page_name}")
