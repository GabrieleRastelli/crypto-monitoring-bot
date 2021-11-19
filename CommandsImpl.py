import telebot
from dotenv import load_dotenv
import os
from MyCoinloreClient import MyCoinloreClient
from MessageFormatter import MessageFormatter
from CacheManager import CacheManager
from MarkupUtils import MarkupUtils
import json

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_API_KEY'))
my_coinlore_client = MyCoinloreClient()
message_formatter = MessageFormatter()
cache_manager = CacheManager()


class CommandsImpl:
    markup_utils = MarkupUtils()
    my_bot = None

    def __init__(self, bot):
        self.my_bot = bot
        return

    def send_start_message(self, message):
        bot.send_photo(message.chat.id,
                       photo='https://static.vecteezy.com/ti/vecteur-libre/t2/581882-pictogram-graph-icon-illustrationle-gratuit-vectoriel.jpg',
                       caption="*Cripto Monitoring Bot*\n"
                               "With this bot you can configure scheduled telegram "
                               "messages to let you know the current price of your favourite cryptos.\n"
                               "You can also search for some informations about a particular crypto",
                       parse_mode='Markdown',
                       reply_markup=self.markup_utils.gen_markup(2, {"Monitered cryptos": "cb_monitored",
                                                                     "Search crypto": "cb_search"}))

    def send_monitored_cryptos(self, message):

        cryptos_ids = cache_manager.get_user_cryptos(message.chat.id)

        # if user does have some monitored cryptos
        if cryptos_ids is not None and len(cryptos_ids) > 0:
            formatted_message = "Here are your watched cryptos:\n"
            for crypto_id in cryptos_ids:
                formatted_message += message_formatter.format_crypto_json_message(
                    my_coinlore_client.get_crypto_by_id(crypto_id))
        else:
            formatted_message = 'You don\'t have any watched crypto'

        bot.send_message(message.chat.id, formatted_message,
                         reply_markup=self.markup_utils.gen_markup(2, {"Add crypto": "cb_add_crypto"}))

    def search_crypto(self, message):
        bot.send_message(message.chat.id, 'Sure, wait a second...')
        json_crypto = my_coinlore_client.get_crypto_by_name(message.text)
        if (json_crypto != None):
            msg_to_send = message_formatter.format_crypto_json_message(json_crypto)
        else:
            msg_to_send = 'Crypto not found'
        bot.send_message(message.chat.id, msg_to_send)

    def save_crypto(self, message):
        bot.send_message(message.chat.id, 'Saving crypto...')
        crypto_searched = my_coinlore_client.get_crypto_by_name(message.text)
        if (crypto_searched != None):
            crypto_id = json.loads(crypto_searched)["id"]
            cache_manager.add_watched_crypto_for_user(message.chat.id, crypto_id)
            bot.send_message(message.chat.id,
                             'How often would you like to be sent a message with crypto\'s informations?',
                             reply_markup=self.markup_utils.gen_markup(2,
                                                                       {"Every 1 h": "cb_oneh", "Every 6 h": "cb_sixh",
                                                                        "Every 24 h": "cb_twentyfourh",
                                                                        "Never": "cb_never"}))
        else:
            bot.send_message(message.chat.id, 'Crypto not found. Cannot save crypto.')
