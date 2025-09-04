import flet as ft
from loguru import logger

from main_app import main_app

if __name__ == "__main__":
    logger.info("Starting Flet app...")
    ft.app(target=main_app, view=ft.AppView.FLET_APP)
