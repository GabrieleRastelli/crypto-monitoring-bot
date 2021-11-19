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
        price_eur = str(self.converter.convert(float(price_usd), 'USD', 'EUR'))
        market_cap_usd = json_string["market_cap_usd"]
        formatted_message="name: "+name+ \
                          "\nsymbol: " + symbol + \
                          "\nrank: " + rank + \
                          "\nprice_usd: " + price_usd + \
                          "\nprice_eur: " + price_eur + \
                          "\nmarket_cap_usd: " + market_cap_usd + '\n\n'

        return formatted_message


