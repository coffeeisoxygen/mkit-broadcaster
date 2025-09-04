import flet as ft
from loguru import logger
from src.custom.exception.base_exc import AppExceptionError
from src.schemas.sch_user import UserLogin

from controller.auth_controller import login


class LoginState:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.error = ""
        self.success = ""
        self.loading = False
        self.dialog_open = False


def login_page(page: ft.Page) -> ft.Column:
    """Login page UI with state and controller integration."""
    state = LoginState()
    username_input = ft.TextField(
        label="Username",
        on_change=lambda e: setattr(state, "username", e.control.value),
    )
    password_input = ft.TextField(
        label="Password",
        password=True,
        on_change=lambda e: setattr(state, "password", e.control.value),
    )
    error_text = ft.Text(value="", color="#EF5350")
    success_text = ft.Text(value="", color="#66BB6A")
    dialog = ft.AlertDialog(
        title=ft.Text("Login Result"), content=error_text, open=False
    )
    page.overlay.append(dialog)

    async def handle_login(_: ft.ControlEvent):
        state.loading = True
        page.update()
        logger.info(
            f"Login attempt: username='{state.username}', password='{state.password}'"
        )
        try:
            user_input = UserLogin(username=state.username, password=state.password)
            logger.info(f"Calling auth_controller.login with: {user_input}")
            await login(user_input)
            state.success = "Login berhasil!"
            state.error = ""
            success_text.value = state.success
            error_text.value = ""
            dialog.content = success_text
        except AppExceptionError as app_ex:
            logger.exception(f"Login error: {app_ex}")
            state.error = app_ex.message
            state.success = ""
            error_text.value = state.error
            success_text.value = ""
            dialog.content = error_text
        except Exception as ex:
            logger.exception(f"Login error: {ex}")
            state.error = str(ex)
            state.success = ""
            error_text.value = state.error
            success_text.value = ""
            dialog.content = error_text
        dialog.open = True
        page.update()
        state.loading = False

    login_btn = ft.ElevatedButton("Login", on_click=handle_login, disabled=False)

    return ft.Column(
        [
            ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
            username_input,
            password_input,
            login_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
