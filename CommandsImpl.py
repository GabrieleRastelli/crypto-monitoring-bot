import telebot
from dotenv import load_dotenv
import os
import json
import logging
from MyCoinloreClient import MyCoinloreClient
from MessageFormatter import MessageFormatter
from CacheManager import CacheManager
from MarkupUtils import MarkupUtils


load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_API_KEY'))
my_coinlore_client = MyCoinloreClient()
message_formatter = MessageFormatter()
cache_manager = CacheManager()


class CommandsImpl:
    logging.basicConfig(level=logging.INFO)
    markup_utils = MarkupUtils()
    my_bot = None

    def __init__(self, bot):
        self.my_bot = bot
        return

    def send_start_message(self, message):
        logging.info(message.from_user.username + ' sending back /start message')

        bot.send_photo(message.chat.id,
                       photo='https://static.vecteezy.com/ti/vecteur-libre/t2/581882-pictogram-graph-icon-illustrationle-gratuit-vectoriel.jpg',
                       caption="*Crypto Monitoring Bot*\n"
                               "With this bot you can track your favourite cryptos.\n"
                               "You can also search for some informations about a particular crypto.",
                       parse_mode='Markdown',
                       reply_markup=self.markup_utils.gen_markup(2, {"Monitered cryptos": "cb_monitored",
                                                                     "Search crypto": "cb_search"}))

    def send_monitored_cryptos(self, message):

        logging.info(message.from_user.username + ' requested monitored cryptos.')

        bot.send_message(message.chat.id, 'Sure, wait a second...')
        cryptos_ids = cache_manager.get_user_cryptos(message.chat.id)

        # if user does have some monitored cryptos
        if cryptos_ids is not None and len(cryptos_ids) > 0:
            logging.info(message.from_user.username + ' has some monitored cryptos.')
            formatted_message = "Here are your watched cryptos:\n"
            for crypto_id in cryptos_ids:
                formatted_message += message_formatter.format_crypto_json_message(
                    my_coinlore_client.get_crypto_by_id(crypto_id))
        else:
            logging.info(message.from_user.username + ' doesn\'t have any monitored cryptos.')
            formatted_message = 'You don\'t have any watched crypto'

        bot.send_message(message.chat.id, formatted_message, parse_mode='Markdown',
                         reply_markup=self.markup_utils.gen_markup(2, {"Add crypto": "cb_add_crypto"}))

    def search_crypto(self, message):
        crypto_to_search=message.text
        logging.info(message.from_user.username + ' searched for crypto: '+crypto_to_search)

        bot.send_message(message.chat.id, 'Sure, wait a second...')
        json_crypto = my_coinlore_client.get_crypto_by_name(crypto_to_search)
        if (json_crypto != None):
            logging.info(message.from_user.username + ' crypto: ' + crypto_to_search + ' found.')
            msg_to_send = message_formatter.format_crypto_json_message(json_crypto)
        else:
            logging.warning(message.from_user.username + ' crypto: ' + crypto_to_search + ' not found.')
            msg_to_send = 'Crypto not found'
        bot.send_message(message.chat.id, msg_to_send, parse_mode='Markdown',)

    def save_crypto(self, message):
        crypto_name=message.text
        logging.info(message.from_user.username + ' sent request to save crypto: ' + crypto_name)

        bot.send_message(message.chat.id, 'Saving crypto..')
        crypto = my_coinlore_client.get_crypto_by_name(crypto_name)
        if (crypto != None):
            logging.info(message.from_user.username + ' crypto: ' + crypto_name + ' saved.')
            crypto_id = json.loads(crypto)["id"]
            cache_manager.add_watched_crypto_for_user(message.chat.id, crypto_id)
            bot.send_message(message.chat.id, 'Crypto saved!')
        else:
            logging.info(message.from_user.username + ' crypto: ' + crypto_name + ' not found. Cannot save it.')
            bot.send_message(message.chat.id, 'Crypto not found. Cannot save crypto.')
