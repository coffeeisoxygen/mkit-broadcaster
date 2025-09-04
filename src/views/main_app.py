import flet as ft

from controller.user_check_controller import seed_user_if_empty
from views.main_layout import build_main_layout
from views.pages.login import login_page


def show_login(page):
    page.clean()
    page.add(login_page(page))


def show_dashboard(page):
    page.clean()
    layout = build_main_layout(page)
    page.add(layout)


async def seed_admin(page):
    await seed_user_if_empty({"username": "admin", "password": "admin"})


def main_app(page: ft.Page):
    """Entry point utama aplikasi Flet MKIT Broadcaster.

    Mengatur layout utama dari builder modular.
    """
    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Cek session login
    if not page.session.get("is_logged_in"):
        show_login(page)
    else:
        show_dashboard(page)
