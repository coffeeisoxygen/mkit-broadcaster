"""Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from loguru import logger
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import get_settings


class BotApp:
    def __init__(self):
        self.log = logger.bind(module="main")
        self.log.add("file_{time}.log", rotation="500 MB")
        self.settings = get_settings()
        self.application = Application.builder().token(self.settings.BOT__TOKEN).build()
        self._register_handlers()
        self._is_running = False

    def _register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_handler))
        self.application.add_handler(CommandHandler("help", self.help_handler))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo_handler)
        )
        # Handler for unknown commands (must be last)
        self.application.add_handler(
            MessageHandler(filters.COMMAND, self.unknown_handler)
        )

    async def start_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        chat_id = update.effective_chat.id if update.effective_chat else None
        username = getattr(user, "username", "unknown") if user else "unknown"
        self.log.info(
            "/start command issued by user: {} | chat_id: {}", username, chat_id
        )
        if chat_id is not None and user is not None:
            await context.bot.send_message(
                chat_id=chat_id, text=f"Hi {user.mention_html()}!", parse_mode="HTML"
            )

    async def help_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        chat_id = update.effective_chat.id if update.effective_chat else None
        self.log.info("/help command issued | chat_id: {}", chat_id)
        if chat_id is not None:
            await context.bot.send_message(chat_id=chat_id, text="Help!")

    async def echo_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        text = update.message.text if update.message and update.message.text else ""
        chat_id = update.effective_chat.id if update.effective_chat else None
        self.log.info("Echo message: {} | chat_id: {}", text, chat_id)
        if chat_id is not None:
            await context.bot.send_message(chat_id=chat_id, text=text)

    async def unknown_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        chat_id = update.effective_chat.id if update.effective_chat else None
        self.log.info("Unknown command received | chat_id: {}", chat_id)
        if chat_id is not None:
            await context.bot.send_message(
                chat_id=chat_id, text="Sorry, I didn't understand that command."
            )

    def start(self):
        """Start polling bot."""
        self.log.info("Starting bot application")
        self._is_running = True
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def stop(self):
        """Stop polling bot."""
        self.log.info("Stopping bot application")
        self._is_running = False
        await self.application.stop()


def main():
    """Entrypoint for bot app."""
    bot = BotApp()
    bot.start()


if __name__ == "__main__":
    main()
