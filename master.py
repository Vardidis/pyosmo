from requests_html import HTMLSession
import json
from OsmoExceptions import *
from trade import Trade
from metadata import Metadata

class Tokens:
    token_list = []
    
    def __init__(self) -> None:
        pass

    def _render(self, url:str) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=1)
    
    #PUBLIC METHODS
    def get_asset_price(self, asset:str=None) -> dict:
        for i in range(0, len(json.loads(self.r.content))+1):
            if(json.loads(self.r.content)[i]['symbol'] == asset):
                return {'price': json.loads(self.r.content)[i]['price']}
        raise NotFoundError

    def get_asset_liquidity(self, asset:str=None) -> dict:
        for i in range(0, len(json.loads(self.r.content))+1):
            if(json.loads(self.r.content)[i]['symbol'] == asset):
                return {'liquidity': json.loads(self.r.content)[i]['liquidity']}
        raise NotFoundError

    def get_asset_denom(self, asset:str=None) -> dict:
        for i in range(0, len(json.loads(self.r.content))+1):
            if(json.loads(self.r.content)[i]['symbol'] == asset):
                return {'denom': json.loads(self.r.content)[i]['denom']}
        raise NotFoundError

    def get_asset_volume_24h(self, asset:str=None) -> dict:
        for i in range(0, len(json.loads(self.r.content))+1):
            if(json.loads(self.r.content)[i]['symbol'] == asset):
                return {'volume_24h': json.loads(self.r.content)[i]['volume_24h']}
        raise NotFoundError

    def get_asset_info(self, asset:str=None) -> dict:
        for i in range(0, len(json.loads(self.r.content))+1):
            if(json.loads(self.r.content)[i]['symbol'] == asset or json.loads(self.r.content)[i]['name'] == asset):
                return {'name': json.loads(self.r.content)[i]['name'],
                        'symbol': json.loads(self.r.content)[i]['symbol'],
                        'denom': json.loads(self.r.content)[i]['denom'],
                        'price': json.loads(self.r.content)[i]['price'],
                        'liquidity': json.loads(self.r.content)[i]['liquidity'],
                        'volume_24h': json.loads(self.r.content)[i]['volume_24h']}
        raise NotFoundError

    def get_all_asset_prices(self, currency='usd') -> list:
        aux = []
        if(currency=='usd'):
            self._render(url='https://api.coingecko.com/api/v3/simple/price?ids=osmosis,ion,cosmos,akash-network,sentinel,iris-network,crypto-com-chain,persistence,regen,starname,e-money,e-money-eur,juno-network,likecoin,terrausd,terra-luna,bitcanna,terra-krw,secret,medibloc,comdex,cheqd-network,vidulum,band-protocol,sifchain&vs_currencies=usd')
            for i in json.loads(self.r.content):
                aux.append({i: json.loads(self.r.content)[i]})
        elif(currency=='eur'):
            self._render(url='https://api.coingecko.com/api/v3/simple/price?ids=osmosis,ion,cosmos,akash-network,sentinel,iris-network,crypto-com-chain,persistence,regen,starname,e-money,e-money-eur,juno-network,likecoin,terrausd,terra-luna,bitcanna,terra-krw,secret,medibloc,comdex,cheqd-network,vidulum,band-protocol,sifchain&vs_currencies=eur')
            for i in json.loads(self.r.content):
                aux.append({i: json.loads(self.r.content)[i]})
        else:
            raise CurrencyError
        return aux

class Pools:

    def __init__(self) -> None:
        self._render(url='https://api-osmosis.imperator.co/pools/v1/all')

    def _render(self, url:str) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=1)

    #PUBLIC METHODS
    def get_all_pools(self, min:int=0) -> list[dict]:
        aux = []
        for i in range(1, len(json.loads(self.r.content))):
            asset1 = json.loads(self.r.content)[str(i)][0]['symbol']
            asset2 = json.loads(self.r.content)[str(i)][1]['symbol']
            if(asset1 != '' and asset2 != ''):
                if(json.loads(self.r.content)[str(i)][1]['liquidity'] >= min):
                    aux.append({'pool': asset1+'/'+asset2, 'liquidity': json.loads(self.r.content)[str(i)][1]['liquidity'], 'volume_7d': json.loads(self.r.content)[str(i)][1]['volume_7d'], 'volume_24h': json.loads(self.r.content)[str(i)][1]['volume_24h']})
        return aux


class Epochs:

    def __init__(self) -> None:
        self._render(url='https://lcd-osmosis.keplr.app/osmosis/epochs/v1beta1/epochs')

    def _render(self, url) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=1)

    #PUBLIC METHODS
    def get_current_epoch(self, identifier:str) -> dict:
        assert identifier=='day' or identifier=='week'
        if(identifier=='day'):
            return {'current_epoch': json.loads(self.r.content)['epochs'][0]['current_epoch'], 'current_epoch_start_time': json.loads(self.r.content)['epochs'][0]['current_epoch_start_time'], 'duration': json.loads(self.r.content)['epochs'][0]['duration']}
        elif(identifier=='week'):
            return {'current_epoch': json.loads(self.r.content)['epochs'][1]['current_epoch'], 'current_epoch_start_time': json.loads(self.r.content)['epochs'][1]['current_epoch_start_time'], 'duration': json.loads(self.r.content)['epochs'][1]['duration']}
        else:
            raise IdentifierError

class Assets:

    def _render(self, url) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=1)

    def get_balance(self, asset:str):
        for i in Tokens.token_list:
            if(asset == i['symbol']):
                addr = Trade.address_book[asset.lower()]
                self._render(url='https://lcd-' + asset.lower() + '.keplr.app/bank/balances/' + addr)
                for j in json.loads(self.r.content)['result']:
                    if(j['denom'] == 'u' + asset.lower()):
                        return j['amount']
