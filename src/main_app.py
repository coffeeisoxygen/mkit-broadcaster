import flet as ft
from loguru import logger
from src.config import get_settings
from src.schemas.sch_user import UserCreate, UserLogin

from controller.auth_controller import login as login_service
from controller.user_check_controller import seed_user_if_empty, user_exists
from core.state import LoginState, app_state
from views.main_layout import build_main_layout


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

    def show_login_modal():
        login_state = LoginState()
        username_input = ft.TextField(
            label="Username",
            on_change=lambda e: setattr(login_state, "username", e.control.value),
        )
        password_input = ft.TextField(
            label="Password",
            password=True,
            on_change=lambda e: setattr(login_state, "password", e.control.value),
        )
        error_text = ft.Text(value="", color="#EF5350")
        dialog = ft.AlertDialog(
            title=ft.Text("Login"),
            open=True,
            modal=True,
        )

        async def handle_login(_: ft.ControlEvent):
            login_state.loading = True
            page.update()
            try:
                user_input = UserLogin(
                    username=login_state.username,
                    password=login_state.password,
                )
                await login_service(user_input)
                app_state.login({"username": login_state.username})
                dialog.open = False
                show_dashboard(page)
            except Exception as ex:
                login_state.error = str(ex)
                error_text.value = login_state.error
                dialog.content = error_text
            page.update()
            login_state.loading = False

        login_btn = ft.ElevatedButton("Login", on_click=handle_login)
        dialog.content = ft.Column([
            username_input,
            password_input,
            login_btn,
            error_text,
        ])
        page.overlay.append(dialog)
        page.update()

    if not app_state.is_logged_in:
        show_login_modal()
    else:
        show_dashboard(page)
