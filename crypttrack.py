import datetime
import json
import sys
import traceback
from calendar import monthrange

import requests
from github import Github
from web3 import Web3

g = Github('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')
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.defibit.io/"))
WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
limit_orders_abi = json.loads(
    '[{"inputs":[{"internalType":"address","name":"adr","type":"address"}],"name":"authorize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"cancelOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"collectFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"orderIDs","type":"uint256[]"}],"name":"fulfilMany","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"fulfilOrder","outputs":[{"internalType":"bool","name":"filled","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"OrderCancelled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"orderID","type":"uint256"},{"indexed":false,"internalType":"address","name":"broker","type":"address"}],"name":"OrderFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"orderID","type":"uint256"},{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountIn","type":"uint256"},{"indexed":false,"internalType":"address","name":"tokenIn","type":"address"},{"indexed":false,"internalType":"address","name":"tokenOut","type":"address"},{"indexed":false,"internalType":"uint256","name":"targetAmountOut","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"minAmountOut","type":"uint256"}],"name":"OrderPlaced","type":"event"},{"inputs":[{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"targetAmountOut","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"}],"name":"placeBNBTokenOrder","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"targetAmountOut","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"}],"name":"placeTokenBNBOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"targetAmountOut","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"}],"name":"placeTokenTokenOrder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"state","type":"bool"}],"name":"setBlacklist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"state","type":"bool"}],"name":"setWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"state","type":"bool"}],"name":"setWhitelistState","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"adr","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"adr","type":"address"}],"name":"unauthorize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"addressOrders","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"blacklisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"canFulfilOrder","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getBNBSpotPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"getCurrentAmountOut","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getNextReadyOrder","outputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"getOrder","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"enum IBogLimitOrdersV1.OrderStatus","name":"status","type":"uint8"},{"internalType":"enum IBogLimitOrdersV1.OrderType","name":"swapType","type":"uint8"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"targetAmountOut","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint256","name":"feePaid","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"adr","type":"address"}],"name":"getOrdersForAddress","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPendingOrders","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pair","type":"address"},{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"getReserves","outputs":[{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRouterAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"}],"name":"getTokenTokenPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextOrder","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"orders","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"pendingIndex","type":"uint256"},{"internalType":"uint256","name":"addressIndex","type":"uint256"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"enum IBogLimitOrdersV1.OrderStatus","name":"status","type":"uint8"},{"internalType":"enum IBogLimitOrdersV1.OrderType","name":"swapType","type":"uint8"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"address","name":"pair","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"targetAmountOut","type":"uint256"},{"internalType":"uint256","name":"minAmountOut","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint256","name":"feePaid","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRICE_DECIMALS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"router","outputs":[{"internalType":"contract IPancakeRouter02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"orderID","type":"uint256"}],"name":"shouldFulfilOrder","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"sortTokens","outputs":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"UINT_MAX","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WBNB","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
Bep_20_api = json.loads(
    '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
address = '0x0Bd91f45FcA6428680C02a79A2496D6f97BDF24a'
address = web3.toChecksumAddress(address)
contract = web3.eth.contract(address=address, abi=limit_orders_abi)


def crypt_log(value, date, blowlist):
    # print(blowlist)
    if len(blowlist) > 2201:
        blowlist.pop(2)
    temp_dict = {value: date}
    blowlist.append(temp_dict)
    # print(blowlist)


def decimal_str(y, decimals=15):
    return format(y, f".{decimals}f").lstrip().rstrip('0')


def getDecimal(w3, bep, tok):
    Dcontract = w3.eth.contract(address=tok, abi=bep)
    decimals = Dcontract.functions.decimals().call()
    return decimals


def direct_coin_request(token_id, token_name):
    print(token_name)
    bnb_token = True

    def test(t):
        p = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/")).eth.contract(address=address,
                                                                                      abi=limit_orders_abi).functions.getTokenTokenPrice(
            t, WBNB).call()
        return p

    w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
    badtok = False
    try:
        price = test(token_id)
    except Exception:
        try:
            new_token = Web3.toChecksumAddress(token_id)
            price = test(new_token)
        except Exception as notokerr:
            print(f'bad BNB token! {notokerr}')
            bnb_token = False
        badtok = True
    if bnb_token is False:
        try:
            header = {'X-MBX-APIKEY': 'ZGMLcJIdgFcUB603rTl0kQ4M4AzStoBMfJl9tyl0csswBOyafOMVR2LJi7mbBJj9'}
            avg_price_url = 'https://api.binance.com/api/v3/avgPrice'
            symbol = token_name + "USDT"
            params = {"symbol": symbol}
            r = requests.get(avg_price_url, params=params, headers=header)
            if "Invalid symbol" in r.text:
                try:
                    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9d820f3b5df74983aaed0167188c0c37'))
                    uni_contract = w3.toChecksumAddress('0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f')
                    ERC_20_API = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
                    uni_api = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
                    token_id = w3.toChecksumAddress(token_id)
                    ETH = w3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
                    ERC_contract = w3.eth.contract(address=uni_contract, abi=uni_api)
                    x = ERC_contract.functions.getPair(token_id, ETH).call()
                    ERC_contract = w3.eth.contract(address=x, abi=ERC_20_API)
                    t1, t2, t3 = ERC_contract.functions.getReserves().call()
                    ETH_price = get_ETH_price()
                    final_price = (t2 * ETH_price / t1)
                    return final_price
                except Exception:
                    print(Exception)
            else:
                ERC_price = float(r.text.split('price":"', 1)[1].rsplit('"', 1)[0])
                print(f'the price is: {ERC_price}')
                return ERC_price
        except:
            try:
                w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9d820f3b5df74983aaed0167188c0c37'))
                uni_contract = w3.toChecksumAddress('0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f')
                ERC_20_API = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
                uni_api = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
                token_id = w3.toChecksumAddress(token_id)
                ETH = w3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
                ERC_contract = w3.eth.contract(address=uni_contract, abi=uni_api)
                x = ERC_contract.functions.getPair(token_id, ETH).call()
                ERC_contract = w3.eth.contract(address=x, abi=ERC_20_API)
                t1, t2, t3 = ERC_contract.functions.getReserves().call()
                ETH_price = get_ETH_price()
                final_price = (t2 * ETH_price / t1)
                return final_price
            except Exception:
                print(Exception)
    else:
        if badtok:
            Dcontract = w3.eth.contract(address=new_token, abi=Bep_20_api)
            tokenIn = Dcontract.functions.decimals().call()
            Dcontract = w3.eth.contract(address=WBNB, abi=Bep_20_api)
            tokenOut = Dcontract.functions.decimals().call()
        else:
            Dcontract = w3.eth.contract(address=token_id, abi=Bep_20_api)
            tokenIn = Dcontract.functions.decimals().call()
            Dcontract = w3.eth.contract(address=WBNB, abi=Bep_20_api)
            tokenOut = Dcontract.functions.decimals().call()
        price = price / pow(10, tokenOut - tokenIn)
        USDprice = ((price / pow(10, 10)) * (contract.functions.getBNBSpotPrice().call()) / pow(10, 10))

        final = USDprice / pow(10, 16)
        return final


def get_BNB_price():
    return contract.functions.getBNBSpotPrice().call()


def get_ETH_price():
    avg_price_url = 'https://api.binance.com/api/v3/avgPrice'
    params = {"symbol": 'ETHUSDT'}
    header = {'X-MBX-APIKEY': 'ZGMLcJIdgFcUB603rTl0kQ4M4AzStoBMfJl9tyl0csswBOyafOMVR2LJi7mbBJj9'}
    r = requests.get(avg_price_url, params=params, headers=header)
    print(r.text)
    parse = float(r.text.split('price":"', 1)[1].rsplit('"', 1)[0])
    return parse


def get_token_bnb_value(token):
    badtok = False
    try:
        price = contract.functions.getTokenTokenPrice(token, WBNB).call()
    except Exception:
        try:
            new_token = Web3.toChecksumAddress(token)
            price = contract.functions.getTokenTokenPrice(new_token, WBNB).call()
        except Exception as badtoken:
            print(f'bad token! {badtoken}')
            return
        badtok = True
    if badtok:
        tokenIn = getDecimal(web3, Bep_20_api, new_token)
        tokenOut = getDecimal(web3, Bep_20_api, WBNB)
    else:
        tokenIn = getDecimal(web3, Bep_20_api, token)
        tokenOut = getDecimal(web3, Bep_20_api, WBNB)
    price = price / pow(10, tokenOut - tokenIn) / pow(10, 18)
    return price


def check_BNB_token(token):
    try:
        contract.functions.getTokenTokenPrice(token, WBNB).call()
        return True
    except Exception as badtoken:
        print(f'bad token! {badtoken}')
        try:
            new_token = Web3.toChecksumAddress(token)
            contract.functions.getTokenTokenPrice(new_token, WBNB).call()
            return True
        except Exception as badtoken:
            print(f'bad token! {badtoken}')
            return False


def check_BINANCE_token(token):
    try:
        token_name = parse_ERC_token(token)
    except Exception:
        print('token name not found!')
        return False
    header = {'X-MBX-APIKEY': 'ZGMLcJIdgFcUB603rTl0kQ4M4AzStoBMfJl9tyl0csswBOyafOMVR2LJi7mbBJj9'}
    all_symbols_url = "https://api.binance.com/api/v3/ticker/price"
    try:
        r = requests.get(all_symbols_url, headers=header)
        if token_name in r.text:
            return True
        else:
            return False
    except Exception as badtoken:
        print(f'error! bad token {badtoken}')
        return False


def check_uni_token(token):
    try:
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9d820f3b5df74983aaed0167188c0c37'))
        uni_contract = w3.toChecksumAddress('0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f')
        ERC_20_API = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
        uni_api = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
        token_id = w3.toChecksumAddress(token)
        ETH = w3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
        ERC_contract = w3.eth.contract(address=uni_contract, abi=uni_api)
        x = ERC_contract.functions.getPair(token_id, ETH).call()
        ERC_contract = w3.eth.contract(address=x, abi=ERC_20_API)
        t1, t2, t3 = ERC_contract.functions.getReserves().call()
        ETH_price = get_ETH_price()
        (t2 * ETH_price / t1)
        return True
    except Exception:
        print(Exception)
        return False


async def add_token_git(name, token, h, client):
    try:
        text = f'Name {name}\ntoken {token}'
        repo = h.get_repo('ghostofcoolidge/cryptobot')
        repo.create_file(f"crypt/{name}_list.txt", "start", text)
        print('finish adding token to github')
    except Exception:
        try:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            await err_message.send(z)
            await err_message.send(y)
        except Exception:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            print(y)
            print(z)
            await err_message.send('error too long to send through discord; please check Heroku')


async def remove_token_get(name, h, client):
    repo = h.get_repo('ghostofcoolidge/cryptobot')
    try:
        contents = repo.get_contents(f"crypt/{name}_list.txt")
        repo.delete_file(contents.path, 'remove token', contents.sha)
        return True
    except Exception:
        try:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            await err_message.send(z)
            await err_message.send(y)
        except Exception:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            print(y)
            print(z)
            await err_message.send('error too long to send through discord; please check Heroku')


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


def parse_BNB_token(tokenid):
    r = requests.get(f'https://www.bscscan.com/token/{tokenid}')
    x = str(r.content).split("symbol\\': \\'", 1)[1].split('\\', 1)[0]
    print(x)
    x2 = x.replace('.', '')
    if x2.isalnum():
        print('token name found!')
        return x
    else:
        print('could not parse token name')
        return False


def parse_ERC_token(tokenid):
    r = requests.get(f'https://explorer.bitquery.io/ethereum/token/{tokenid}')
    x = str(r.content)
    print(x)
    parse = x.split('(', 1)[1].split(') ERC20', 1)[0]
    parse = parse.replace('.', '')
    if parse.isalnum():
        print('token name found!')
        return parse
    else:
        print('could not parse token name')
        return False


def ticker_mess(string):
    x = 0
    tl = []
    tl2 = []
    for item in string.split(' split '):
        x = x + len(item)
        tl.append(item)
        if x > 1700:
            tl2.append(tl)
            tl = []
            x = 0
    if tl:
        tl2.append(tl)
    return tl2


# THIS IS WHERE WRAPPER FUNCTION WOULD BE USEFUL; NEED TO LEARN HOW TO IMPLEMENT
async def percent(num, message, length, ptime):
    if ptime == '24 hours':
        head = f'**Prices for the past {ptime}:**\n\n\n'
    else:
        head = f'**Prices for the past {length} {ptime}:**\n\n\n'
    price = ''
    for item in num:
        # print(item)
        if item == num[0]:
            price = price + f'**${decimal_str(item)}**\n\n'
        else:
            n = num.index(item) - 1
            an = ((item - num[n]) / num[n])
            perc = round(an * 100, 2)
            # print(f'{perc}%')
            price = price + f'**${decimal_str(item)}**\n(*{perc}%*)\n\n'
    total = round(((num[-1] - num[0]) / num[0]) * 100, 2)
    await message.channel.send(f'{head}{price}total percentage change:\n***({total})%***')


async def hourly(crypt_list, message):
    htime = 'hours'
    if len(crypt_list) < 9:
        await message.channel.send('not enough data stored.')
        return
    else:
        temp_cr_li = []
        for i in crypt_list:
            # print(f'item: {i}')
            if isfloat(i):
                temp_cr_li.append(float(i))
        temp_list = temp_cr_li[-6:]
        length = len(temp_list)
        # print(temp_list)
        await percent(temp_list, message, length, htime)


async def daily(crypt_list, token, token_name, message):
    dtime = '24 hours'
    if len(crypt_list) < 123:
        await message.channel.send('not enough data stored.')
        return
    else:
        temp_cr_li = []
        for i in crypt_list:
            if isfloat(i):
                temp_cr_li.append(float(i))
        temp_val = direct_coin_request(token, token_name)
        temp_cr_li.append(temp_val)
        temp_list = temp_cr_li[-25::24]
        length = len(temp_list)
        await percent(temp_list, message, length, dtime)


async def days(crypt_list, token, token_name, message):
    daytime = 'days'
    if len(crypt_list) < 123:
        await message.channel.send('not enough data stored.')
        return
    else:
        temp_cr_li = []
        for i in crypt_list:
            if isfloat(i):
                temp_cr_li.append(float(i))
        temp_val = direct_coin_request(token, token_name)
        temp_cr_li.append(temp_val)
        temp_list = temp_cr_li[::-24][:5]
        length = len(temp_list)
        await percent(temp_list, message, length, daytime)


async def weekly(crypt_list, token, token_name, message):
    wtime = 'weeks'
    if len(crypt_list) < 386:
        await message.channel.send('not enough data stored.')
        return
    else:
        temp_cr_li = []
        for i in crypt_list:
            if isfloat(i):
                temp_cr_li.append(float(i))
        temp_val = direct_coin_request(token, token_name)
        temp_cr_li.append(temp_val)
        temp_list = temp_cr_li[::-96][:4]
        length = len(temp_list)
        await percent(temp_list, message, length, wtime)


async def monthly(crypt_list, token, token_name, message):
    mtime = 'months'
    if len(crypt_list) < 2162:
        await message.channel.send('not enough data stored.')
        return
    else:
        temp_cr_li = []
        for i in crypt_list:
            if isfloat(i):
                temp_cr_li.append(float(i))
        temp_val = direct_coin_request(token, token_name)
        temp_cr_li.append(temp_val)
        temp_list = temp_cr_li[::-720][:3]
        length = len(temp_list)
        await percent(temp_list, message, length, mtime)


def percent_check_hourly(li, pernum):
    if len(li) < 5:
        print('not enough data stored.')
        return False, False, False, False
    else:
        temp = []
        for item in li:
            # print(item)
            if isfloat(item):
                temp.append(float(item))
        # print(temp)
        new = temp[-1]
        old = temp[-2]
        if old == 0:
            perc = 0
            return True, new, old, perc
        perc = round(((new - old) / old * 100), 2)
        print(f'hourly percentage: {perc}')
        if perc >= pernum or perc <= (-1 * pernum):
            return True, new, old, perc
        else:
            return False, new, old, perc


def percent_check_quarterly(li, pernum):
    if len(li) < 11:
        print('not enough data stored.')
        return False, False, False, False
    else:
        temp = []
        for item in li:
            # print(item)
            if isfloat(item):
                temp.append(float(item))
        # print(temp)
        new = temp[-1]
        old = temp[-7]
        if old == 0:
            perc = 0
            return True, new, old, perc
        perc = round(((new - old) / old * 100), 2)
        print(f'hourly percentage: {perc}')
        if perc >= pernum or perc <= (-1 * pernum):
            return True, new, old, perc
        else:
            return False, new, old, perc


def percent_check_daily(li, pernum):
    if len(li) < 28:
        print('not enough data stored.')
        return False, False, False, False
    else:
        temp = []
        for i in li:
            if isfloat(i):
                temp.append(float(i))
        # print(temp)
        new = temp[-1]
        old = temp[-25]
        if old == 0:
            perc = 0
            return True, new, old, perc
        # print(old)
        perc = round(((new - old) / old * 100), 2)
        print(f'daily percentage: {perc}')
        if perc >= pernum or perc <= (-1 * pernum):
            return True, new, old, perc
        else:
            return False, new, old, perc


def percent_check_weekly(li, pernum):
    if len(li) < 172:
        print('not enough data stored.')
        return False, False, False, False
    else:
        temp = []
        for i in li:
            if isfloat(i):
                temp.append(float(i))
        new = temp[-1]
        old = temp[-169]
        if old == 0:
            perc = 0
            return True, new, old, perc
        perc = round(((new - old) / old * 100), 2)
        print(f'weekly percentage: {perc}')
        if perc >= pernum or perc <= (-1 * pernum):
            return True, new, old, perc
        else:
            return False, new, old, perc


def percent_check_monthly(li, pernum):
    current_time = datetime.datetime.today()
    year = current_time.year
    previous_month = current_time.month - 1
    if previous_month == 0:
        previous_month = 12
        year = year - 1
    hours = monthrange(year, previous_month)[1]
    hours = (hours * 24) + 1
    if len(li) < hours + 3:
        print('not enough data stored.')
        return False, False, False, False
    else:
        temp = []
        for i in li:
            if isfloat(i):
                temp.append(float(i))
        new = temp[-1]
        old = temp[-hours]
        if old == 0:
            perc = 0
            return True, new, old, perc
        perc = round(((new - old) / old * 100), 2)
        print(f'monthly percentage: {perc}')
        if perc >= pernum or perc <= (-1 * pernum):
            return True, new, old, perc
        else:
            return False, new, old, perc


def ticker_percent(current, hour):
    if hour == 0:
        tick_percent = 0
        return tick_percent
    tick_percent = ((current - hour) / hour) * 100
    return tick_percent


# def ticker_percent_24h(current,coin_list):
#     if len(coin_list) > 26:
#         daily = coin_list[-25]
#         daily_percent = ((current - daily)/ daily) * 100
#     return daily_percent


# TODO CHANGE FLAG NUMBERING SYSTEM: MAKE IT CHECK THE HIGHEST FLAG NUMBER IN THE DICT AND THEN ADD 1
def add_flag_percent(message, all_coin, token, flag_percent, flaglist):
    if float(flag_percent) == 0:
        response = 'please use a number other than zero'
        return response
    token_check = False
    for item in all_coin:
        if token == item["Name"]:
            token_value = direct_coin_request(item["token"], item["Name"])
            token_check = True
            break
    if token_check:
        flag_dict = {}
        user_id = message.author.id

        flagnum = len(flaglist) + 1
        flag_dict.update({
            "user": user_id,
            "token": token,
            "token_value": float(token_value),
            "percent": float(flag_percent),
            "flagnum": flagnum})
        flaglist.append(flag_dict)
        response = f'flag stored! Flag number is: {flagnum}'
        return response
    else:
        response = 'token not found in list: please choose a token that is being tracked by the bot'
        return response


# TODO FIX REMOVE FUNCTION!
async def remove_flag(message, flag_list_percent, flag_list_abs, flagnum):
    user_id = message.user.id
    for item in flag_list_percent:
        if flagnum == item["flagnum"] and user_id == item["user"]:
            flag_list_percent.remove(item)
            await message.channel.send('flag has been removed from bot archive')
            return
    for item in flag_list_abs:
        if flagnum == item["flagnum"] and user_id == item["user"]:
            flag_list_percent.remove(item)
            await message.channel.send('flag has been removed from bot archive')
            return


def update_flag_text(flli, flagtext):
    print('updating flag text...')
    print(flli)
    strlist = ''
    for item in flli:
        for k, v in item.items():
            strlist = strlist + str(k) + f' {str(v)}\n'
        strlist = strlist + ',' + '\n'
    repo = g.get_repo(f'ghostofcoolidge/cryptobot')
    contents = repo.get_contents(flagtext)
    repo.update_file(contents.path, 'update', strlist, contents.sha)
    print('done')


async def check_flags(client, flag_list_percent, flagprcenttext, dict_prices):
    if len(flag_list_percent) < 1:
        return
    else:
        for item in flag_list_percent:
            token_found = False
            for k, v in dict_prices.items():
                if item["token"] == k:
                    current_price = v
                    token_found = True
                    break
                else:
                    continue
            if token_found:
                perc_check = ((current_price - item["token_value"]) / item["token_value"]) * 100
                if item["percent"] > 0:
                    if perc_check >= float(item["percent"]):
                        print('flag triggered!')
                        channel = client.get_channel(833260192850247710)
                        user = client.get_user(int(item["user"]))
                        user_id = user.id
                        # await user.send(
                        #     f'FLAG TRIGGERED: {item["token"]} has increased {round(perc_check), 2}% in value!\n*${decimal_str(current_price, 15)}*')
                        await channel.send(
                            f'<@!{user_id}> FLAG TRIGGERED: {item["token"]} has increased {round(perc_check), 2}% in value!\n*${decimal_str(current_price, 15)}*')
                        flag_list_percent.remove(item)
                        update_flag_text(flag_list_percent, flagprcenttext)
                elif item["percent"] < 0:
                    if perc_check <= float(item["percent"]):
                        print('flag triggered!')
                        channel = client.get_channel(833260192850247710)
                        user = client.get_user(item["user"])
                        user_id = user.id
                        await channel.send(
                            f'<@!{user_id}> FLAG TRIGGERED: {item["token"]} has decreased {round(perc_check), 2}% in value!\n*${decimal_str(current_price, 15)}*')
                        flag_list_percent.remove(item)
                        update_flag_text(flag_list_percent, flagprcenttext)
            else:
                print('item not found in coin archive!')
                flag_list_percent.remove(item)
                update_flag_text(flag_list_percent, flagprcenttext)
                continue
