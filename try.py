from requests_html import HTMLSession
import json

def merge_pair(asset1, asset2):
    return asset1 + '/' + asset2
wallet_addr = 'cosmos...za'
url = 'https://lcd-cosmoshub.keplr.app/auth/accounts/' + wallet_addr

session = HTMLSession()
r = session.get(url)                                                ##### 2.5 validate auth
r.html.render(sleep=1)

#auth info
auth_info = json.loads(r.content)
print(auth_info)

#latest blocks
url = 'https://lcd-osmosis.keplr.app/blocks/latest'                 ##### 2
session = HTMLSession()
r = session.get(url)
r.html.render(sleep=1)

latest_blocks = json.loads(r.content)

#unknown info
url = 'https://rpc-osmosis.keplr.app/status'                        ##### finally
session = HTMLSession()
r = session.get(url)
r.html.render(sleep=1)

osmo_wallet_addr = 'osmo...50'    ##### 1
#current asset balance (all assets) None if no assets present
url = 'https://lcd-'+pair e.g. 'osmosis' or 'juno' + '.keplr.app/bank/balances/' + osmo_wallet_addr
session = HTMLSession()
r = session.get(url)
r.html.render(sleep=1)
#checq -> 'https://api.cheqd.net/bank/balances/cheqd...fv'
