from tron_utils import TronManager

TRONGRID_URI = "https://api.trongrid.io/"
TRONGRID_APIKEY = '767b77ae-fbd7-498d-a86d-724b6e04ea32'

proxies = None#{'http': 'http://127.0.0.1:9998/', 'https': 'http://127.0.0.1:9998/'}
nile_priv_key = '0ef65b198e9c235688bf1f9b216a42d121f1c9ce6aa69d2b81dc34a1ab2107bc'# add: TWxF2SmEtXS3WG65K8uhtA2Et92vbybRZR

trm = TronManager(private_key=nile_priv_key, node_uri='', node_api_key='', test=True, proxies=proxies)
# trm = TronManager(private_key=nile_priv_key, node_uri=TRONGRID_URI, node_api_key=TRONGRID_APIKEY, test=False, proxies=proxies)

txm = trm.send_token(amount=1000000000.0, to_address='TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA', coin_code='USDT')
bal = trm.get_balance(coin_code='USDT')
bal
