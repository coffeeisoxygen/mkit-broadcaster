import flet as ft


def build_header(
    title: str, clock_text: ft.Text, theme_toggle_row: ft.Row
) -> ft.Container:
    """Reusable header component."""
    return ft.Container(
        ft.Row(
            [
                ft.Text(value=title, size=17, weight=ft.FontWeight.BOLD),
                clock_text,
                ft.Container(
                    content=theme_toggle_row,
                    alignment=ft.alignment.center_right,
                    padding=0,
                    width=140,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(left=20, right=20, top=12, bottom=8),
        bgcolor="#1dd0d6",
        shadow=ft.BoxShadow(blur_radius=8, color="#0D010121", offset=(0, 2)),
    )
