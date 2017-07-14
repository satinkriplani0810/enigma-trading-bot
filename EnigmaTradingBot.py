import configparser
import json
import logging

from urllib.request import urlopen
from telegram.ext import CommandHandler
from telegram.ext import Updater


class EnigmaTradingBot:
    def __init__(self, token):
        self.bot_token = token
        self.updater = Updater(token=self.bot_token)
        self.dispatcher = self.updater.dispatcher
        self.error_msg = "Please see correct usage in /start"
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s', level=logging.INFO)

    def generate_handler(self, method):
        handler = CommandHandler(method, getattr(self, method), pass_args=True)
        self.dispatcher.add_handler(handler)

    def initialize_bot(self):
        self.generate_handler('start')
        self.generate_handler('fetch')
        self.updater.start_polling()

    def start(self, bot, update, args):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Usage:\n"
                              "/start - Usage Details\n"
                              "/fetch - fetch <currency1> <currency2> ~ "
                              "Get current trading rates of currency2 against currency1")
        logging.info('start')

    def fetch(self, bot, update, args):
        url = "https://poloniex.com/public?command=returnTicker"
        all_currency = urlopen(url)
        currency_in_json = json.loads(all_currency.read())
        try:
            query = args[0].upper() + '_' + args[1].upper()
            bot.send_message(chat_id=update.message.chat_id,
                             text="Current : " + currency_in_json[query]['last'] +
                                  "\nHighest Bid : " + currency_in_json[query][
                                 'highestBid'] + "\nLowest Ask : " + currency_in_json[query]['lowestAsk'])
            logging.info(query + ' details fetched successfully')
        except (KeyError, IndexError) as e:
            bot.send_message(chat_id=update.message.chat_id, text=self.error_msg)
            logging.error(e)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('conf.cfg')
    enigma_bot = EnigmaTradingBot(config.get('TELEGRAM', 'BOT_TOKEN'))
    enigma_bot.initialize_bot()
