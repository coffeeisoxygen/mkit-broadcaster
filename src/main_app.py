import flet as ft
from loguru import logger
from src.config import get_settings
from src.schemas.sch_user import UserCreate

from controller.user_check_controller import seed_user_if_empty, user_exists
from core.state import app_state
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
    settings = get_settings()
    admin_data = settings.ADM
    try:
        if not await user_exists():
            logger.info("Seeding admin user: {}", admin_data.username)
            user_create = UserCreate(
                username=admin_data.username,
                full_name=admin_data.full_name,
                password=admin_data.password,
            )
            await seed_user_if_empty(user_create)
        else:
            logger.info("Admin user already exists: {}", admin_data.username)
    except Exception as e:
        logger.error("Error seeding admin user: {}", e)


async def main_app(page: ft.Page):
    """Entry point utama aplikasi Flet MKIT Broadcaster.

    Mengatur layout utama dari builder modular.
    """
    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT

    await seed_admin(page)  # <-- panggil seeder di awal

    def goto_dashboard():
        app_state.is_logged_in = True
        show_dashboard(page)

    def goto_login():
        app_state.is_logged_in = False
        show_login(page)

    # Pass navigation callbacks to login page
    if not app_state.is_logged_in:
        page.on_login_success = goto_dashboard
        goto_login()
    else:
        goto_dashboard()
