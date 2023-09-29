from requests_html import HTMLSession
import json

class Metadata:
    ADDRESS_BOOK = {'osmo': 'osmo1ngr3cmq0utly0ej3ag5wfxgph02c266crnqj50',
                    'cosmos': 'cosmos1ngr3cmq0utly0ej3ag5wfxgph02c266ctgnzza',
                    'juno': 'juno1ngr3cmq0utly0ej3ag5wfxgph02c266ca6se9p',
                    'cheqd': 'cheqd1ngr3cmq0utly0ej3ag5wfxgph02c266c92lzfv',
                    'scrt': 'secret1ra9qfcmh3uqa08raz24dvcp453yk77g0qzu34m',
                    'akt': 'akash1ngr3cmq0utly0ej3ag5wfxgph02c266cxn79m8',
                    'cro': 'cro19vpvvqmkxnexeadw5x69297l8gn6dc3r2mkm3v',
                    'iov': 'star180uqgj673w77ymm7h7kvwlqqz5rrk2e40j03v0',
                    'rowan': 'sif1ngr3cmq0utly0ej3ag5wfxgph02c266cw4u5dk',
                    'ctk': 'certik1ngr3cmq0utly0ej3ag5wfxgph02c266cvq04rk',
                    'iris': 'certik1ngr3cmq0utly0ej3ag5wfxgph02c266cvq04rk',
                    'regen': 'regen1ngr3cmq0utly0ej3ag5wfxgph02c266c52c75e',
                    'xprt': 'persistence1s4thg0h7tgm0wyckyt9sg462hz4tuqkl5zugmc',
                    'dvpn': 'sent1ngr3cmq0utly0ej3ag5wfxgph02c266csn9mxj',
                    'kava': 'kava1zypusfk4f962zaykw5drrutgwl63w6kccraum9',
                    'ixo': 'ixo1ngr3cmq0utly0ej3ag5wfxgph02c266c5adsxw',
                    'ngm': 'emoney1ngr3cmq0utly0ej3ag5wfxgph02c266cytfk4q',
                    'bld': 'agoric1q55fnazkpaum25fr2fvqtz9pt38mww7pdrqz7h',
                    'boot': 'bostrom1ngr3cmq0utly0ej3ag5wfxgph02c266cgm83u6',
                    'stars': 'stars1ngr3cmq0utly0ej3ag5wfxgph02c266cl5ylfv',
                    'axl': 'axelar1ngr3cmq0utly0ej3ag5wfxgph02c266c0x92fu',
                    'somm': 'somm1ngr3cmq0utly0ej3ag5wfxgph02c266c85uwnh',
                    'umee': 'umee1ngr3cmq0utly0ej3ag5wfxgph02c266ce7wax0',
                    'str': 'str1ngr3cmq0utly0ej3ag5wfxgph02c266ca0m365',
                    'huahua': 'chihuahua1ngr3cmq0utly0ej3ag5wfxgph02c266cga7vrl',
                    'nom': 'nomic1ngr3cmq0utly0ej3ag5wfxgph02c266chsqc3h',
                    'axl': 'axelar1ngr3cmq0utly0ej3ag5wfxgph02c266c0x92fu',
                    'like': 'cosmos1ngr3cmq0utly0ej3ag5wfxgph02c266ctgnzza',
                    'atom': 'cosmos1ngr3cmq0utly0ej3ag5wfxgph02c266ctgnzza',
                    'microtick': 'micro1ngr3cmq0utly0ej3ag5wfxgph02c266cesw9mf',
                    'bcna': 'bcna1ngr3cmq0utly0ej3ag5wfxgph02c266c3crr20',
                    'btsg': 'bitsong1a6h2e5jcl80xtsxht92uhwevfm4g30qlh424dc',
                    'grav': 'gravity1ngr3cmq0utly0ej3ag5wfxgph02c266c0cp684'
                    }

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