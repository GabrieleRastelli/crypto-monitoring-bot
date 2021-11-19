from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class MarkupUtils:

    def __init__(self):
        return

    def gen_markup(self, row_width, titles_callbacks):
        markup = InlineKeyboardMarkup()
        markup.row_width = row_width

        for title, callback in titles_callbacks.items():
            markup.add(InlineKeyboardButton(title, callback_data=callback))

        return markup

