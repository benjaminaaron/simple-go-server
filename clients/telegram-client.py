from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import websocket
import sys


class TelegramClient:

    def __init__(self, _url, _token):
        self.url = _url
        self.token = _token
        self.socket = None
        self.bot = None
        self.chat_id = None
        self.connect_to_websocket()
        self.init_telegram_bot()

    def init_telegram_bot(self):
        updater = Updater(token)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.on_telegram_start_command))
        dp.add_handler(CommandHandler("stop", self.on_telegram_stop_command))
        dp.add_handler(CommandHandler("help", self.on_telegram_help_command))
        dp.add_handler(MessageHandler(Filters.text, self.on_telegram_message))
        dp.add_error_handler(self.on_telegram_error)
        updater.start_polling()
        updater.idle()

    def connect_to_websocket(self):
        self.socket = websocket.WebSocketApp(self.url, on_open=self.on_websocket_open,
                                             on_message=self.on_websocket_message,
                                             on_error=self.on_websocket_error, on_close=self.on_websocket_close)
        threading.Thread(target=self.socket.run_forever).start()

    # ------ WebSocket methods ------

    def on_websocket_message(self, ws, message):
        if self.bot is None:
            print('Telegram bot not yet available to pass on message from WebSocket')
            return
        self.bot.send_message(chat_id=self.chat_id, text=message)

    @staticmethod
    def on_websocket_open(ws):
        print('Connected to ' + ws.url)

    @staticmethod
    def on_websocket_error(ws, error):
        print(error)

    @staticmethod
    def on_websocket_close(ws):
        print("### closed ###")

    # ------ Telegram methods ------

    def on_telegram_start_command(self, bot, update):
        self.bot = bot
        self.chat_id = update.message.chat_id
        update.message.reply_text('Connection to WebSocket established.')

    def on_telegram_stop_command(self, bot, update):
        self.socket.close()
        self.socket = None
        self.bot = None
        self.chat_id = None
        update.message.reply_text('Connection to WebSocket is closed. Use /start to reconnect.')

    def on_telegram_message(self, bot, update):
        if self.socket is None:
            update.message.reply_text('No connection to WebSocket. Use /start first.')
            return
        self.socket.send(update.message.text)

    @staticmethod
    def on_telegram_help_command(bot, update):
        update.message.reply_text('TODO write help text')

    @staticmethod
    def on_telegram_error(bot, update, error):
        print(update, error)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print('Enter the WebSocket URL:')
        url = input()
    if not url.startswith('ws://'):
        url = 'ws://' + url

    token = ''  # intentionally not committed to the repository

    TelegramClient(url, token)
