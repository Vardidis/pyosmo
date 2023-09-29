from requests_html import HTMLSession
import json

class Trade:
    address_book = {'osmo': 'osmo1ngr3cmq0utly0ej3ag5wfxgph02c266crnqj50',
                    'cosmos': 'cosmos1ngr3cmq0utly0ej3ag5wfxgph02c266ctgnzza',
                    'juno': 'juno1ngr3cmq0utly0ej3ag5wfxgph02c266ca6se9p',
                    'cheqd': 'cheqd1ngr3cmq0utly0ej3ag5wfxgph02c266c92lzfv'}

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