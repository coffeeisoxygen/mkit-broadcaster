import asyncio

import aiohttp
from loguru import logger


class TelegramSender:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def _post(self, endpoint: str, data=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            if files:
                # aiohttp butuh cara khusus untuk multipart/form-data
                form = aiohttp.FormData()
                if data:
                    for k, v in data.items():
                        form.add_field(k, str(v))
                for k, v in files.items():
                    form.add_field(k, v, filename=getattr(v, "name", "file"))
                async with session.post(url, data=form) as resp:
                    return await self._handle_response(resp)
            else:
                async with session.post(url, data=data) as resp:
                    return await self._handle_response(resp)

    async def _handle_response(self, resp):
        if resp.status == 200:
            logger.success("✅ Success: {}", await resp.text())
            return await resp.json()
        else:
            error = await resp.text()
            logger.error("❌ Error {}: {}", resp.status, error)
            return {"ok": False, "error": error}

    # --------------------------
    # Public methods
    # --------------------------
    async def send_text(self, text: str, parse_mode: str = "Markdown"):
        return await self._post(
            "sendMessage",
            {"chat_id": self.chat_id, "text": text, "parse_mode": parse_mode},
        )

    async def send_photo(
        self, photo_path: str, caption: str = None, parse_mode: str = "Markdown"
    ):
        with open(photo_path, "rb") as photo_file:
            files = {"photo": photo_file}
            data = {"chat_id": self.chat_id}
            if caption:
                data["caption"] = caption
                data["parse_mode"] = parse_mode
            return await self._post("sendPhoto", data, files)

    async def send_document(
        self, file_path: str, caption: str = None, parse_mode: str = "Markdown"
    ):
        with open(file_path, "rb") as doc_file:
            files = {"document": doc_file}
            data = {"chat_id": self.chat_id}
            if caption:
                data["caption"] = caption
                data["parse_mode"] = parse_mode
            return await self._post("sendDocument", data, files)


# --------------------------
# Sample usage
# --------------------------
async def main():
    TOKEN = "8489362184:AAGdQoBfA42Fx5cyqy17lc2YOfy0861MfRw"
    CHAT_ID = "-1003090883152"

    bot = TelegramSender(TOKEN, CHAT_ID)

    # Send text
    await bot.send_text("*Halo* bro 🚀\n\n_Teks pake Markdown_ `inline`")

    # Send photo
    # await bot.send_photo("path/to/image.jpg", caption="Foto dengan *Markdown*")

    # Send document
    # await bot.send_document("path/to/file.pdf", caption="Ini dokumen PDF")


if __name__ == "__main__":
    asyncio.run(main())
