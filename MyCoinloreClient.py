from coinlore.client import Client
import json


class MyCoinloreClient:
    client = Client()

    def __init__(self):
        return

    # search for a crypto by name (the call must be made with a 100 coins limit at a time)
    # @returns a json representation of it
    def get_crypto_by_name(self, crypto_name):
        start_index = 0
        end_index = 100
        coins = self.client.getcoins(str(start_index), str(end_index))

        while len(coins.get('data')) > 0:
            coins_data = coins.get('data')
            for coin_data in coins_data:
                if (coin_data['name'].lower() == crypto_name.lower()) or (coin_data['symbol'].lower() == crypto_name.lower()):
                    return json.dumps(coin_data)
            start_index += 100
            end_index += 100
            coins = self.client.getcoins(str(start_index), str(end_index))

        return None

    # search for a crypto by id
    # @returns a json representation of it
    def get_crypto_by_id(self, crypto_id):

        return json.dumps(self.client.getcoin(int(crypto_id)))