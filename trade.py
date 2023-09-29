from requests_html import HTMLSession
import json

class Trade:
    address_book = {'osmo': 'osmo...50',
                    'cosmos': 'cosmos...za',
                    'juno': 'juno...9p',
                    'cheqd': 'cheqd...fv'}

    def __init__(self) -> None:
        pass

    def _render(self, url:str) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=1)

    def _connect(self, asset:str):
        url = 'https://lcd-cosmoshub.keplr.app/auth/accounts/' + asset
        self._render(url)
        auth_info = json.loads(r.content)

    def _auth():
        pass

    def deposit(self, asset:str):
        pass
