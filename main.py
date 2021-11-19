import telebot
from dotenv import load_dotenv
import os
from CommandsImpl import CommandsImpl


load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_API_KEY'))

commands_impl = CommandsImpl(bot)


@bot.message_handler(commands=['start'])
def start(message):
    commands_impl.send_start_message(message)

@bot.message_handler(commands=['monitoredcryptos'])
def monitored_cryptos_command(message):
    commands_impl.send_monitored_cryptos(message)

@bot.message_handler(commands=['searchcrypto'])
def search_crypto_command(message):
    sent = bot.send_message(message.chat.id, "Insert the name of the crypto you would like to know more about.")
    bot.register_next_step_handler(sent, commands_impl.search_crypto)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_monitored":
        commands_impl.send_monitored_cryptos(call.message)
    elif call.data == "cb_search":
        sent = bot.send_message(call.message.chat.id, "Insert the name of the crypto you would like to know more about.")
        bot.register_next_step_handler(sent, commands_impl.search_crypto)

    elif call.data == "cb_add_crypto":
        sent = bot.send_message(call.message.chat.id, "Insert the name of the crypto you would like monitor.")
        bot.register_next_step_handler(sent, commands_impl.save_crypto)


bot.polling()


