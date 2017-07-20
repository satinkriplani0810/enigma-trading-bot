import configparser
import json
import logging
from poloniex import poloniex
from Bittrex import Bittrex

from urllib.request import urlopen
from telegram.ext import CommandHandler
from telegram.ext import Updater


class EnigmaTradingBot:
    def __init__(self, token):
        self.bot_token = token
        self.updater = Updater(token=self.bot_token)
        self.dispatcher = self.updater.dispatcher
        self.error_msg = "Please see correct usage in /start"
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s', level=logging.DEBUG)

    def generate_handler(self, method):
        handler = CommandHandler(method, getattr(self, method), pass_args=True)
        self.dispatcher.add_handler(handler)

    def initialize_bot(self):
        self.generate_handler('start')
        self.generate_handler('ticker')
        self.updater.start_polling()

    def start(self, bot, update, args):
        reply = "*[Available Commands]*\n\n Get currency ticker:\n /ticker BTC ETH\n"
        bot.send_message(chat_id=update.message.chat_id,
                        text=reply,
                        parse_mode="Markdown")
        logging.info('start')

    def ticker(self, bot, update, args):
        bittrex = Bittrex("xyz", "xyz")

        #Generating the market pair from the user input arguments
        selected_pair = args[0].upper() + "-" + args[1].upper()
        currency = args[0].upper()

        #Bittrex
        try:
            response = bittrex.get_ticker(selected_pair)
            logging.debug("Response: " + str(response))

            if(response['success'] == True):
                formatted_reply = "*[" + selected_pair + "]*\n"
                formatted_reply += "Current: " + str(response['result']['Last']) + " " + currency +\
                    "\nAsk: " + str(response['result']['Ask']) + " " + currency +\
                    "\nBid: " + str(response['result']['Bid']) + " " + currency
            else:
                formatted_reply = "Error: "  + str(response['message']).replace('_', ' ')

        except Exception as e:
            formatted_reply = "Error in invoking Bittrex API."           
            logging.error(e)

        finally: 
            bot.send_message(chat_id=update.message.chat_id,
                text=formatted_reply,
                parse_mode="Markdown")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('conf.cfg')
    enigma_bot = EnigmaTradingBot(config.get('TELEGRAM', 'BOT_TOKEN'))
    enigma_bot.initialize_bot()
