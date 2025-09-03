from telegram.ext import Application


class TelegramBotCore:
    """Core setup bot Telegram: hanya inisialisasi dan lifecycle dasar."""

    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.is_running = False

    async def initialize(self):
        await self.application.initialize()

    async def start(self):
        await self.application.start()
        self.is_running = True

    async def shutdown(self):
        await self.application.shutdown()
        self.is_running = False
