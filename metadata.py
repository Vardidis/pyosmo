from requests_html import HTMLSession
import json

class Metadata:
    ADDRESS_BOOK = {}

    API_SUBDOMAINS = {'osmo': 'lcd-osmosis.keplr.app',
                    'juno': 'lcd-juno.keplr.app',
                    'atom': 'lcd-cosmoshub.keplr.app',
                    'luna': 'lcd-columbus.keplr.app',
                    'cro': 'lcd-crypto-org.keplr.app',
                    'ust': 'lcd-columbus.keplr.app',
                    'scrt': 'lcd-secret.keplr.app',
                    'neta': 'lcd-juno.keplr.app',
                    'stars': 'rest.stargaze-apis.com',
                    'huahua': 'api.chihuahua.wtf',
                    'xprt': 'lcd-persistence.keplr.app',
                    'krt': 'lcd-columbus.keplr.app',
                    'akt': 'lcd-akash.keplr.app',
                    'regen': 'lcd-regen.keplr.app',
                    'dvpn': 'lcd-sentinel.keplr.app',
                    'iris': 'lcd-iris.keplr.app',
                    'iov': 'lcd-iov.keplr.app',
                    'ngm': 'lcd-emoney.keplr.app',
                    'microrick': 'lcd-microtick.keplr.app',
                    'like': 'mainnet-node.like.co',
                    'ixo': 'lcd-impacthub.keplr.app',
                    'bcna': 'lcd.bitcanna.io',
                    'btsg': 'lcd.explorebitsong.com',
                    'xki': 'api-mainnet.blockchain.ki',
                    'med': 'api.gopanacea.org',
                    'boot': 'lcd.bostrom.cybernode.ai',
                    'cmdx': 'rest.comdex.one',
                    'cheqd': 'api.cheqd.net',
                    'lum': 'node0.mainnet.lum.network',
                    'vdl': 'mainnet-lcd.vidulum.app',
                    'dsm': 'api.mainnet.desmos.network',
                    'dig': 'api-1-dig.notional.ventures',
                    'somm': 'lcd-sommelier.keplr.app',
                    'rowan': 'api-int.sifchain.finance',
                    'band': 'laozi1.bandchain.org',
                    'darc': 'node1.konstellation.tech:1318',
                    'umee': 'api.aphrodite.main.network.umee.cc',
                    'grav': 'gravitychain.io:1317'
                    }

    token_list = []

    def __init__(self) -> None:
        self._render(url='https://api-osmosis.imperator.co/tokens/v1/all')
        for i in json.loads(self.r.content):
            self.token_list.append({'name': i['name'], 'symbol': i['symbol']})

        
    
    def _render(self, url:str) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=1)
    
    def get_token_list(self) -> list:
        return self.token_list
