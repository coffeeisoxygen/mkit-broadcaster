# import flet as ft
# from src.config import get_settings

# from bot_core import TelegramBotScheduler
# from tg_helper import get_chat_id_by_username

# # Variabel global untuk menyimpan instance bot dan statusnya
# scheduler = None
# is_bot_running = False


# # Handler untuk cek chat_id (harus async dan di luar main)
# async def get_chat_id_handler(
#     e, page, channel_name_field, recipient_id_field, status_text
# ):
#     bot_token = get_settings().BOT__TOKEN
#     channel_name = (channel_name_field.value or "").strip()
#     if not bot_token or not channel_name:
#         status_text.value = "Status: Token atau Channel Name kosong!"
#         status_text.color = "red"
#         page.update()
#         return
#     status_text.value = "Status: Mencari chat_id..."
#     status_text.color = "blue"
#     page.update()
#     chat_id = await get_chat_id_by_username(bot_token, channel_name)
#     if chat_id:
#         recipient_id_field.value = str(chat_id)
#         status_text.value = f"Status: Chat ID ditemukan: {chat_id}"
#         status_text.color = "green"
#     else:
#         status_text.value = "Status: Gagal mendapatkan chat_id!"
#         status_text.color = "red"
#     page.update()


# def main(page: ft.Page):
#     global scheduler, is_bot_running
#     page.title = "Bot Telegram Scheduler"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER

#     # Elemen UI
#     channel_name_field = ft.TextField(label="Masukkan Channel Name (@namachannel)")
#     recipient_id_field = ft.TextField(label="ID Channel/Grup", disabled=True)
#     status_text = ft.Text("Status: Bot belum berjalan.")

#     start_button = ft.ElevatedButton("Mulai Bot")
#     stop_button = ft.ElevatedButton("Hentikan Bot", disabled=True)
#     get_id_button = ft.ElevatedButton("Cek Chat ID")

#     # Fungsi handler untuk tombol
#     def start_bot(e):
#         global scheduler, is_bot_running
#         if is_bot_running:
#             return

#         bot_token = get_settings().BOT__TOKEN
#         recipient_id = recipient_id_field.value

#         if not bot_token or not recipient_id:
#             status_text.value = (
#                 "Status: ERROR! Token atau Recipient ID tidak boleh kosong."
#             )
#             status_text.color = "red"
#             page.update()
#             return

#         status_text.value = "Status: Memulai bot..."
#         status_text.color = "blue"
#         page.update()

#         scheduler = TelegramBotScheduler(bot_token)
#         scheduler.start_scheduled_tasks(recipient_id)
#         scheduler.start_bot()

#         is_bot_running = True
#         start_button.disabled = True
#         stop_button.disabled = False
#         status_text.value = f"Status: Bot berjalan! ID: {recipient_id}"
#         status_text.color = "green"
#         page.update()

#     def stop_bot(e):
#         global scheduler, is_bot_running
#         if not is_bot_running:
#             return

#         status_text.value = "Status: Menghentikan bot..."
#         status_text.color = "blue"
#         page.update()

#         scheduler.stop_bot()

#         is_bot_running = False
#         start_button.disabled = False
#         stop_button.disabled = True
#         status_text.value = "Status: Bot telah dihentikan."
#         status_text.color = "black"
#         page.update()

#     start_button.on_click = start_bot
#     stop_button.on_click = stop_bot
#     # Handler sync, panggil fungsi async dengan asyncio.create_task

#     def get_id_button_click(e):
#         import asyncio

#         try:
#             loop = asyncio.get_running_loop()
#             loop.create_task(
#                 get_chat_id_handler(
#                     e, page, channel_name_field, recipient_id_field, status_text
#                 )
#             )
#         except RuntimeError:
#             asyncio.run(
#                 get_chat_id_handler(
#                     e, page, channel_name_field, recipient_id_field, status_text
#                 )
#             )

#     get_id_button.on_click = get_id_button_click

#     page.add(
#         ft.Column(
#             [
#                 ft.Text("Dashboard Bot Telegram", size=24, weight=ft.FontWeight.BOLD),
#                 channel_name_field,
#                 ft.Row(
#                     [get_id_button, recipient_id_field],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                 ),
#                 ft.Row(
#                     [start_button, stop_button], alignment=ft.MainAxisAlignment.CENTER
#                 ),
#                 status_text,
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         )
#     )


# if __name__ == "__main__":
#     ft.app(target=main)
