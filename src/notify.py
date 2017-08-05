from _config import TelegramConfig

from virtualenv import PathEnv


class TelegramBot:
    """Get TOKEN from Telegram Bot Father"""
    def __init__(self):
        PathEnv.apply_virtualenv('.py3')
        from telegram import Bot
        self.telegram_bot = Bot(token=TelegramConfig.TOKEN)

    def send_message(self, message):
        self.telegram_bot.send_message(chat_id=TelegramConfig.BOT_CHAT_ID, text=message)
