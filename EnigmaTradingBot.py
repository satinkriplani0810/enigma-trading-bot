import ConfigParser
import json
import logging
import urllib2

from telegram.ext import CommandHandler
from telegram.ext import Updater


class EnigmaTradingBot:
    def __init__(self, token):
        self.bot_token = token
        self.updater = Updater(token=self.bot_token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def generate_handler(self, method):
        handler = CommandHandler(method, getattr(self, method), pass_args=True)
        self.dispatcher.add_handler(handler)

    def initialize_bot(self):
        self.generate_handler('start')
        self.generate_handler('hello')
        self.generate_handler('fetch')
        self.updater.start_polling()

    def start(self, bot, update, args):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        logging.info('start')

    def hello(self, bot, update, args):
        bot.send_message(chat_id=update.message.chat_id, text="Hi! Wassup!")
        logging.info('hello')

    def fetch(self, bot, update, args):
        url = "https://poloniex.com/public?command=returnTicker"
        all_currency = urllib2.urlopen(url)
        currency_in_json = json.loads(all_currency.read())
        query = args[0].upper() + '_' + args[1].upper()
        bot.send_message(chat_id=update.message.chat_id,
                         text="Current : " + currency_in_json[query]['last'] + "\nHighest Bid : " + currency_in_json[query][
                             'highestBid'] + "\nLowest Ask : " + currency_in_json[query]['lowestAsk'])
        logging.info(query + ' details fetched successfully')


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('conf.cfg')
    enigma_bot = EnigmaTradingBot(config.get('TELEGRAM', 'BOT_TOKEN'))
    enigma_bot.initialize_bot()
