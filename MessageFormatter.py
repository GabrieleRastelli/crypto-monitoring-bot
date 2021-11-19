import json
from currency_converter import CurrencyConverter
from MyCoinloreClient import MyCoinloreClient

class MessageFormatter:
    converter = CurrencyConverter()
    client = MyCoinloreClient()

    def __init__(self):
        return

    #method that nicely formats crypto in json string format
    def format_crypto_json_message(self, string):
        json_string = json.loads(string)
        name = json_string["name"]
        symbol = json_string["symbol"]
        rank = str(json_string["rank"])
        price_usd = json_string["price_usd"]
        try:
            price_eur = str(self.converter.convert(float(price_usd), 'USD', 'EUR'))
        except ValueError:
            price_eur = price_usd

        market_cap_usd = json_string["market_cap_usd"]
        try:
            market_cap_eur = str(self.converter.convert(float(json_string["market_cap_usd"]), 'USD', 'EUR'))
        except ValueError:
            market_cap_eur = market_cap_usd

        formatted_message="name: "+name+ \
                          "\nsymbol: " + symbol + \
                          "\nrank: " + rank + \
                          "\nprice_usd: " + price_usd + \
                          "\nprice_eur: " + price_eur + \
                          "\nmarket_cap_usd: " + market_cap_usd + \
                          "\nmarket_cap_eur: " + market_cap_eur + '\n\n'

        return formatted_message


