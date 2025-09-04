import flet as ft
from loguru import logger

from config import get_settings
from controller.auth_controller import login as login_service
from controller.user_check_controller import seed_user_if_empty, user_exists
from core.state import LoginState, app_state
from schemas.sch_user import UserCreate, UserLogin
from views.main_layout import build_main_layout


def show_dashboard(page: ft.Page):
    page.clean()
    layout = build_main_layout(page)
    page.add(layout)


async def seed_admin():
    """Cek DB, kalau kosong seed default admin."""
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


def show_login_modal(page: ft.Page):
    """Modal login Flet dengan state handling."""
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

    login_btn = ft.ElevatedButton("Login")
    cancel_btn = ft.TextButton("Keluar")

    async def handle_login(_: ft.ControlEvent):
        login_state.loading = True
        login_btn.disabled = True
        page.update()

        try:
            user_input = UserLogin(
                username=login_state.username, password=login_state.password
            )
            await login_service(user_input)
            app_state.login({"username": login_state.username})

            # Tutup dialog & navigasi dashboard
            dialog.open = False
            page.update()
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            show_dashboard(page)
            logger.info("Login sukses: {}", login_state.username)

        except Exception as ex:
            login_state.error = str(ex)
            error_text.value = login_state.error

            # Fokus ke field yang perlu diperbaiki
            if "not found" in str(ex):
                username_input.focus()
            else:
                password_input.focus()

            page.update()
        finally:
            login_state.loading = False
            login_btn.disabled = False
            page.update()

    def handle_cancel(_: ft.ControlEvent):
        logger.info("User batal login, closing app.")
        page.window.close()

    login_btn.on_click = handle_login
    cancel_btn.on_click = handle_cancel

    dialog.content = ft.Column([
        username_input,
        password_input,
        login_btn,
        cancel_btn,
        error_text,
    ])

    if dialog not in page.overlay:
        page.overlay.append(dialog)
    page.update()


async def main_app(page: ft.Page):
    """Entry point utama aplikasi Flet MKIT Broadcaster."""
    page.title = "MKIT Broadcaster"
    page.theme_mode = ft.ThemeMode.LIGHT

    await seed_admin()  # seed admin di awal

    if not app_state.is_logged_in:
        show_login_modal(page)
    else:
        show_dashboard(page)
