import requests
class Cachet:
    # init and pass url and api_token
    def __init__(self, url, api_token):
        self.url = url
        self.api_token = api_token
        self.headers = {'content-type': 'application/json', 'X-Cachet-Token': self.api_token, 'User-Agent': 'Mozilla/5.0'}

    
    def update(self, path, payload):
        try:
            return requests.request("PUT", self.url + path, data=payload, headers=self.headers)
        except:
            return False