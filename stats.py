from requests_html import HTMLSession
from OsmoExceptions import *
import asyncio
from typing import Dict, Optional, Any
import time

#       TODOS
#   fix bug with prerender pair not found when IBC values are stored


class Tokens:
    url = 'https://info.osmosis.zone/token'

    def __init__(self) -> None:
        self._render(self.url)        
    
    def _render(self, url:str, wait:int=6) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=wait)

    def _fetch_price(self, asset:str, standalone:bool=False):
        if(standalone):
            url = self.url + '/' + asset
            self._render(url)

        price = self.r.html.xpath('//*[@id="root"]/div/div[3]/div/div/p', first=True)

        if(price == None):
            raise NotFoundError
        else:
            return {'price': price.text.strip('$')}

    def _fetch_liq(self, asset:str, standalone:bool=False) -> str:
        if(standalone):
            url = self.url + '/' + asset
            self._render(url)

        liq = self.r.html.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div[1]/div/div[1]/p[2]', first=True)

        if(liq == None):
            raise NotFoundError
        else:
            return {'liquidity': liq.text.strip('$')}

    def _fetch_24h_vol(self, asset:str, standalone:bool=False) -> str:
        if(standalone):
            url = self.url + '/' + asset
            self._render(url)

        vol = self.r.html.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div[1]/div/div[2]/p[2]', first=True)

        if(vol == None):
            raise NotFoundError
        else:
            return {'24h volume': vol.text.strip('$')}

    #PUBLIC METHODS
    def get_info(self, asset:str) -> dict:
        url = self.url + '/' + asset
        self._render(url)

        price = self._fetch_price(asset)

        if(price == None):
            raise NotFoundError
        else:
            liq = self._fetch_liq(asset)
            vol = self._fetch_24h_vol(asset)
            return {price, liq, vol}

    def get_liq(self, asset:str) -> dict:
        return self._fetch_liq(asset, standalone=True)

    def get_price(self, asset:str) -> dict:
        return self._fetch_price(asset, standalone=True)

    def get_24h_vol(self, asset:str) -> dict:
        return self._fetch_24h_vol(asset, standalone=True)


class Pools:       
    pools_table = []
    incentives = False

    def __init__(self):
        self._pre_render()

    def _render(self, url:str, wait:int=5) -> None:
        session = HTMLSession()
        self.r = session.get(url)
        self.r.html.render(sleep=wait)

    def _finalize(self, info:list[dict], liq:str, *args) -> Dict:
        aux = []
        for element in args:
            element = element.text.strip('%').split(' ')[1]
            aux.append(element)
        return {'liq': liq, '1d_APR': aux[0], '7d_APR': aux[1], '14d_APR': aux[2]}

    def _fetch_liq(self, n:int=None, standalone:bool=False) -> Dict:
        if(standalone):
            url = 'https://app.osmosis.zone/pool/' + str(n)
            self._render(url)

        liq = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[1]/div[1]/div/section/div[2]/ul[1]/li[1]/div/h4', first=True)

        if(liq == None):
            raise RenderError
        else:
            liq = liq.text.strip('$')

        return {'liq': liq}

    def _fetch_APRs(self, n:int=None, standalone:bool=False):
        if(standalone):
            url = 'https://app.osmosis.zone/pool/' + str(n)
            self._render(url)

        day1 = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[2]/div/div[2]/div/table/tbody/tr[1]/td[2]/p', first=True)
        day7 = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[2]/div/div[2]/div/table/tbody/tr[2]/td[2]/p', first=True)
        day14 = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[2]/div/div[2]/div/table/tbody/tr[3]/td[2]/p', first=True)

        if(day1 == None):
            raise RenderError
        else:
            day1 = day1.text.strip('%')
            day7 = day7.text.strip('%')
            day14 = day14.text.strip('%')

        return {'day1': day1, 'day7': day7, 'day14': day14}

    def _fetch_swap_fee(self, n:int=None, standalone:bool=False) -> str:
        if(standalone):
            url = 'https://app.osmosis.zone/pool/' + str(n)
            self._render(url)

        swap_fee = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[1]/div[1]/div/section/div[2]/ul[2]/li[2]/div/h6', first=True)
        swap_fee = swap_fee.text.strip('%')

        return {'swap_fee': swap_fee}

    def _fetch_pool_catalyst(self, n:int=None, standalone:bool=False) -> Dict:
        if(standalone):
            url = 'https://app.osmosis.zone/pool/' + str(n)
            self._render(url)

        asset1 = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div/div/ul/li[1]/section[1]/div/p', first=True).text
        asset1_perc = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div/div/ul/li[1]/section[1]/div/h4', first=True)
        asset1_perc = asset1_perc.text.strip('%')
        asset1_amount = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div/div/ul/li[1]/section[2]/div[1]/h6', first=True)
        asset1_amount = asset1_amount.text.split(' ')[0]

        asset2 = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div/div/ul/li[2]/section[1]/div/p', first=True).text
        asset2_perc = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div/div/ul/li[2]/section[1]/div/h4', first=True)
        asset2_perc = asset2_perc.text.strip('%')
        asset2_amount = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div/div/ul/li[2]/section[2]/div[1]/h6', first=True)
        asset2_amount = asset2_amount.text.split(' ')[0]

        return {'first_asset': {'name': asset1, 'percentage': asset1_perc, 'amount': asset1_amount}, 'second_asset': {'name': asset2, 'percentage': asset2_perc, 'amount': asset2_amount}}

    def _poolInfo(self, pair:str, n:int, w=8) -> dict:
        print(pair, n)
        url = 'https://app.osmosis.zone/pool/' + str(n)
        self._render(url, w)
             
        liq = self._fetch_liq()     
        day1, day7, day14 = self._fetch_APRs()
            
        assert liq and day1 and day7 and day14

        swap_fee = self._fetch_swap_fee()
        pool_catalyst = self._fetch_pool_catalyst()
        
        assert swap_fee and pool_catalyst
        
        return {'liq': liq, 'swap_fee': swap_fee, 'aprs': {'1d_APR(%)': day1, '7d_APR(%)': day7, '14d_APR(%)': day14}, 'pool_catalyst': pool_catalyst} 

    def _pre_render(self) -> None:
        url = 'https://app.osmosis.zone/pools'
        self._render(url, wait=10)
        n = 6
        li = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/section[3]/div/ul/li')

        while(li is None or len(li) == 0):
            n += 2
            self._render(url, wait=n)
            li = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/section[3]/div/ul/li')
            if(n >= 10):
                raise RenderError          

        for i in range(1, len(li)+1):
            pair = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/section[3]/div/ul/li['+str(i)+']/section/div/p', first=True)
            pool_no = self.r.html.xpath('//*[@id="app"]/div[1]/div/div[3]/div/section[3]/div/ul/li['+str(i)+']/section/div/h5', first=True)
            pool_no = pool_no.text.split('#')
            self.pools_table.append({'pair': pair.text, 'no': pool_no[1]})
   
    def _find_pool(self, pair:str) -> int:
        assert self.pools_table
        for pool in self.pools_table:
            if(pool['pair'] == pair):
                return int(pool['no'])
        return -1
        
    #PUBLIC METHODS
    def show(self):
        for i in self.pools_table:
            print(i)

    def get_info(self, pair:str) -> dict:
        num = self._find_pool(pair)
        if(num != -1):
            return {'pool': pair, 'pool_number': num, 'pool_info': self._poolInfo(pair, num)}
        else:
            raise NotFoundError

    def get_liq(self, pair:str) -> dict:
        num = self._find_pool(pair)
        if(num != -1):
            return self._fetch_liq(num, standalone=True)
        else:
            raise NotFoundError

    def get_APRs(self, pair:str) -> dict:
        num = self._find_pool(pair)
        if(num != -1):
            return self._fetch_APRs(num, standalone=True)
        else:
            raise NotFoundError

    def get_swap_fee(self, pair:str) -> dict:
        num = self._find_pool(pair)
        if(num != -1):
            return self._fetch_swap_fee(num, standalone=True)
        else:
            raise NotFoundError

    def get_pool_catalyst(self, pair:str) -> dict:
        num = self._find_pool(pair)
        if(num != -1):
            return self._fetch_pool_catalyst(num, standalone=True)
        else:
            raise NotFoundError
