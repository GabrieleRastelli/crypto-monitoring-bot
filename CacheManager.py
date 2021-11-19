
class CacheManager:

    # this dictionary contains (user -> list of its watched crypto) <- this is VOLATILE !!!
    users_cryptos = dict()

    def __init__(self):
        return


    def add_watched_crypto_for_user(self, received_user, received_crypto):
        if received_user not in self.users_cryptos:
            # adds user to cache
            crypto_list = [str(received_crypto)]
            self.users_cryptos.update({received_user: crypto_list})
        else:
            # adds crypto to the already watched ones
            self.users_cryptos[received_user].append(received_crypto)

        return

    def get_user_cryptos(self, received_user):
        if received_user in self.users_cryptos:
            return self.users_cryptos[received_user]
        else:
            return None
