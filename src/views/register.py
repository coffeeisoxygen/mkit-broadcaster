import flet as ft


async def register_form(page: ft.Page):
    username_input = ft.TextField(label="Username")
    full_name_input = ft.TextField(label="Full Name")
    password_input = ft.TextField(label="Password", password=True)
    register_btn = ft.ElevatedButton("Register")
    return ft.Column(
        [
            ft.Text("Register User", size=20, weight=ft.FontWeight.BOLD),
            username_input,
            full_name_input,
            password_input,
            register_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
