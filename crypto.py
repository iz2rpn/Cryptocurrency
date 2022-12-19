import json
import shutil
import requests
from PIL import Image


class Crypto:

    def __init__(self, crypto_name: str):
        self.crypto_name = crypto_name
        self.error = False
        self.data = self.get_data()
        self.name = self.get_name()
        self.logoUrl = self.get_logoUrl()
        self.logoImg = self.get_logo()
        self.value = self.get_current_value()
        self.volume = self.get_current_volume()

    def get_data(self):
        try:
            current_data = requests.get(
                url=f'https://query1.finance.yahoo.com/v7/finance/quote?&symbols={self.crypto_name}-EUR',
                headers={'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                                        'AppleWebKit/537.36 (KHTML, like Gecko)'
                                        'Chrome/108.0.0.0 Safari/537.36')},
                stream=True)
            response = json.loads(current_data.text)["quoteResponse"]

            if len(response["result"]) > 0:
                return response["result"][0]

            else:
                self.error = True
        except requests.ConnectionError or KeyError or IndexError:
            self.error = True


    def get_current_value(self):
        if not self.error:
            return self.get_data()["regularMarketPrice"]
        return 0

    def get_current_volume(self):
        if not self.error:
            return self.get_data()["regularMarketVolume"]
        return 0

    def get_name(self):
        if not self.error:
            return self.get_data()["shortName"]
        return "NOT FOUND"

    def get_logoUrl(self):
        if not self.error:
            return self.data["logoUrl"]

    def get_logo(self):
        if self.error:
            return "img/error.png"
        self.save_logo()
        return "img/logo.png"

    def save_logo(self):

        if not self.error:
            res = requests.get(url=self.logoUrl,
                               headers={'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                                                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                                                       'Chrome/108.0.0.0 Safari/537.36')},
                               stream=True)
            if res.status_code == 200:
                with open("img/logo.png", "wb") as data:
                    shutil.copyfileobj(res.raw, data)
            
            image = Image.open("img/logo.png")
            image = image.resize((64, 64))
            image.save("img/logo.png")
