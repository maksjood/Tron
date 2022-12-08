from dataclasses import dataclass
from enum import Enum
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey

@dataclass
class Coin:
    contract: str
    decimals: int

class TestCoins(Enum):
    USDT = Coin(contract='TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj', decimals=6)
    TRX = Coin(contract='', decimals=6)

class Coins(Enum):
    USDT = Coin(contract='TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', decimals=6)
    TRX = Coin(contract='', decimals=6, )


class TronManager:

    def __init__(self, private_key:str, node_uri:str, node_api_key:str, node_timeout:float=10.0, test=False, proxies:dict=None) -> None:
        self.test = test
        if test:
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

    def _get_coin(self, coin: str) -> 'Coin':
        return TestCoins[coin].value if self.test else Coins[coin].value

    def send_token(self, coin_code:str, amount:float, to_address:str, memo:str=None, fee_limit:int=None):
        '''`amount` in large coin unit. `fee_limit` in SUN'''
        coin = self._get_coin(coin_code)
        tx_value = amount * 10**coin.decimals
        if not tx_value.is_integer():
            raise Exception(f'"amount" must not have more that {coin.decimals} decimal digits')
        tx_value = int(tx_value)
        if not coin.contract:
            txn = self._client.trx.transfer(from_=self._address, to=to_address, amount=amount)
        else:
            contract = self._client.get_contract(coin.contract)
            txn = contract.functions.transfer(to_address, tx_value).with_owner(self._address)
        if memo:
            txn = txn.memo(memo)
        if fee_limit:
            txn = txn.fee_limit(fee_limit)
        txn = txn.build().sign(self._private_key).broadcast().wait()
        if txn.get('result', '')=='FAILED':
            # if b'transfer amount exceeds balance' in bytes.fromhex(txm['contractResult'][0])
            return False, txn
        return True, txn

    def get_balance(self, coin_code:str):
        coin = self._get_coin(coin_code)
        if not coin.contract:
            return self._client.get_account_balance(self._address)
        else:
            return self._client.get_contract(coin.contract).functions.balanceOf(self._address)