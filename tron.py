from enum import Enum
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey

TRONGRID_URI = "https://api.trongrid.io/"
TRONGRID_APIKEY = '767b77ae-fbd7-498d-a86d-724b6e04ea32'

class Contract(Enum):
    USDT = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'

class TronManager:

    def __init__(self, private_key:str, node_uri:str, node_api_key:str, node_timeout:float=10.0, test_net=False, proxies:dict=None) -> None:
        if test_net:
            self._client = Tron(network='nile')
        else:
            provider = HTTPProvider(endpoint_uri=node_uri, timeout=node_timeout, api_key=node_api_key)
            self._client = Tron(network='mainnet', provider=provider)
        if proxies:
            self._client.provider.sess.proxies = proxies
        self._private_key = PrivateKey(bytes.fromhex(private_key))
        self._address = self._private_key.public_key.to_base58check_address()
        # tether_contract = self._client.get_contract(Contract.USDT.value)

    def _send_tron(self, amount:int, to_address:str, memo:str=None, fee_limit:int=None):
        '''`amount` and `fee_limit` are in SUN. Awaits the tx to get in a block'''
        txn = self._client.trx.transfer(from_=self._address, to=to_address, amount=amount)
        if memo:
            txn = txn.memo(memo)
        if fee_limit:
            txn = txn.fee_limit(fee_limit)
        txn = txn.build().sign(self._private_key).broadcast().wait()
        return txn

    def send_token(self, amount:float, to_address:str, memo:str=None, coin:str=None):
        '''if no `coin` assigned, default network token (tron) is considered'''
        if not coin:
            sun = amount * 1_000_000
            if not sun.is_integer():
                raise Exception('"amount" must not have more that 6 decimal digits')
            return self._send_tron(amount=int(sun), to_address=to_address, memo=memo)

proxies = {'http': '127.0.0.1:9998', 'https': '127.0.0.1:9998'}
nile_priv_key = '0ef65b198e9c235688bf1f9b216a42d121f1c9ce6aa69d2b81dc34a1ab2107bc'
trm = TronManager(private_key=nile_priv_key, node_uri='', node_api_key='', test_net=True)
# trm = TronManager(private_key='', node_uri=TRONGRID_URI, node_api_key=TRONGRID_APIKEY, test_net=False)
txm = trm.send_token(amount=10000.0, to_address='TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA')
# trm._client.get_transaction()

# tether_contract = client.get_contract(USDT)
# print(tether_contract.functions.symbol())


# # Private key of TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3
# priv_key = 

# txn = (
#     client.trx.transfer("TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3", "TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA", 1_000)
#     .memo("test memo")
#     .build()
#     .inspect()
#     .sign(priv_key)
#     .broadcast()
# )

# print(txn)
# # > {'result': True, 'txid': '5182b96bc0d74f416d6ba8e22380e5920d8627f8fb5ef5a6a11d4df030459132'}
# print(txn.wait())
# # > {'id': '5182b96bc0d74f416d6ba8e22380e5920d8627f8fb5ef5a6a11d4df030459132', 'blockNumber': 6415370, 'blockTimeStamp': 1591951155000, 'contractResult': [''], 'receipt': {'net_usage': 283}}