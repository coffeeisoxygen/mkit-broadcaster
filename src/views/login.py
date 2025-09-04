import flet as ft


async def login_form(page: ft.Page):
    username_input = ft.TextField(label="Username")
    password_input = ft.TextField(label="Password", password=True)
    login_btn = ft.ElevatedButton("Login")
    return ft.Column(
        [
            ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
            username_input,
            password_input,
            login_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
