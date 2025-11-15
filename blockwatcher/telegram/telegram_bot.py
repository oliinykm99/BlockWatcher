from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, CHAT_ID

class TelegramBotHandler:
    def __init__(self, token, chat_id):
        self.chat_id = chat_id
        self.bot = Bot(token=token)
        self.application = ApplicationBuilder().token(token).build()

        # /start handler
        start_handler = CommandHandler("start", self.handle_start)
        self.application.add_handler(start_handler)

    async def send_alert(self, message: str):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message, 
                                        parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            print(f"❌ Failed to send message to Telegram: {e}")

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.effective_user.first_name
        message = (
            f"Hi {user_name}! 👋 Welcome to BlockWatcher Bot.\n\n"
            "To receive alerts on large transactions, join our channel:\n"
            "[BlockWatcher Alerts](https://t.me/BlockWatcher_Alerts)"
        )
        await update.message.reply_text(message, parse_mode="Markdown")

    async def start(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

telegram_bot_handler = TelegramBotHandler(TELEGRAM_TOKEN, CHAT_ID)