from telegram.ext import Updater
from telegram.ext import CommandHandler
import ConfigParser
import logging


class EnigmaTradingBot:

    def __init__(self, token):
        self.bot_token = token
        self.updater = Updater(token=self.bot_token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def generate_handler(self, method):
        handler = CommandHandler(method, getattr(self, method))
        self.dispatcher.add_handler(handler)

    def initialize_bot(self):
        self.generate_handler('start')
        self.generate_handler('hello')
        self.updater.start_polling()

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        logging.info('start')

    def hello(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hi! Wassup!")
        logging.info('hello')


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('conf.cfg')
    enigma_bot = EnigmaTradingBot(config.get('TELEGRAM', 'BOT_TOKEN'))
    enigma_bot.initialize_bot()
