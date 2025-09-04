import asyncio
from datetime import datetime

import flet as ft


async def run_clock(clock_text: ft.Text, page: ft.Page):
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        clock_text.value = now
        page.update()
        await asyncio.sleep(1)
