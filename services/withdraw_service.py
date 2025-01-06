import time
import ccxt
import random

#----main-options----#
switch_cex = ""       # binance, mexc, kucoin, gate, okx, huobi, bybit
symbolWithdraw = ""      # символ токена
network = ""     # ID сети
proxy_server = ""

#----second-options----#
amount = []          # минимальная и максимальная сумма
decimal_places = 2           # количество знаков, после запятой для генерации случайных чисел
delay = []             # минимальная и максимальная задержка
shuffle_wallets = ""       # нужно ли мешать кошельки yes/no
#----end-all-options----#

class API:
    # binance API
    binance_apikey = ""
    binance_apisecret = ""
    # okx API
    okx_apikey = ""
    okx_apisecret = ""
    okx_passphrase = ""
    # bybit API
    bybit_apikey = ""
    bybit_apisecret = ""
    # gate API
    gate_apikey = ""
    gate_apisecret = ""
    # kucoin API
    kucoin_apikey = ""
    kucoin_apisecret = ""
    kucoin_passphrase = ""
    # mexc API
    mexc_apikey = ""
    mexc_apisecret = ""
    # huobi API
    huobi_apikey = ""
    huobi_apisecret = ""

proxies = {
  "http": proxy_server,
  "https": proxy_server,
}

def binance_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.binance({
        'apiKey': API.binance_apikey,
        'secret': API.binance_apisecret,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            tag=None,
            params={
                "network": network
            }
        )
        print(f'\n>>>[Binance] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[Binance] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def okx_withdraw(address, amount_to_withdrawal, wallet_number):
    try:
        # Используйте полный формат сети, например, "USDT-TRC20"
        chainName = f"{symbolWithdraw}-{network}"
        fee = get_withdrawal_fee(symbolWithdraw, chainName)

        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_server,
                'https': proxy_server
            },
        })

        exchange.withdraw(symbolWithdraw, amount_to_withdrawal, address,
                          params={
                              "toAddress": address,
                              "chainName": chainName,
                              "dest": 4,
                              "fee": fee,
                              "pwd": '-',
                              "amt": amount_to_withdrawal,
                              "network": network
                          }
                          )

        print(f'\n>>>[OKx] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[OKx] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)

def bybit_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.bybit({
        'apiKey': API.bybit_apikey,
        'secret': API.bybit_apisecret,
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            tag=None,
            params={
                "forceChain": 1,
                "network": network
            }
        )
        print(f'\n>>>[ByBit] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[ByBit] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def gate_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.gate({
        'apiKey': API.gate_apikey,
        'secret': API.gate_apisecret,
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            params={
                "network": network
            }
        )
        print(f'\n>>>[Gate.io] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[Gate.io] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def kucoin_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.kucoin({
        'apiKey': API.kucoin_apikey,
        'secret': API.kucoin_apisecret,
        'password': API.kucoin_passphrase,
        'enableRateLimit': True,
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            params={
                "network": network
            }
        )
        print(f'\n>>>[Kucoin] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[Kucoin] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def mexc_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.mexc({
        'apiKey': API.mexc_apikey,
        'secret': API.mexc_apisecret,
        'enableRateLimit': True,
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            params={
                "network": network
            }
        )
        print(f'\n>>>[MEXC] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[MEXC] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def huobi_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.huobi({
        'apiKey': API.huobi_apikey,
        'secret': API.huobi_apisecret,
        'enableRateLimit': True,
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            params={
                "network": network
            }
        )
        print(f'\n>>>[Huobi] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[Huobi] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def choose_cex(address, amount_to_withdrawal, wallet_number):
    if switch_cex == "binance":
        binance_withdraw(address, amount_to_withdrawal, wallet_number)
    elif switch_cex == "okx":
        okx_withdraw(address, amount_to_withdrawal, wallet_number)
    elif switch_cex == "bybit":
        print(f"\n>>> Bybit в больнице, у них API заболело, sorry") #bybit_withdraw(address, amount_to_withdrawal, wallet_number)
    elif switch_cex == "gate":
        gate_withdraw(address, amount_to_withdrawal, wallet_number)
    elif switch_cex == "huobi":
        huobi_withdraw(address, amount_to_withdrawal, wallet_number)
    elif switch_cex == "kucoin":
        kucoin_withdraw(address, amount_to_withdrawal, wallet_number)
    elif switch_cex == "mexc":
        mexc_withdraw(address, amount_to_withdrawal, wallet_number)
    else:
        raise ValueError("Неверное значение CEX. Поддерживаемые значения: binance, okx, bybit, gate, huobi, kucoin, mexc.")


def get_withdrawal_fee(symbolWithdraw, chainName):
    exchange = ccxt.okx({
        'apiKey': API.okx_apikey,
        'secret': API.okx_apisecret,
        'password': API.okx_passphrase,
        'enableRateLimit': True,
        'proxies': {
            'http': proxy_server,
            'https': proxy_server
        },
    })

    try:
        # Вывод для отладки
        print(f"Searching fee for symbol: {symbolWithdraw}, chain: {chainName}")

        currencies = exchange.fetch_currencies()

        # Вывод всех доступных валют для проверки
        print("Available currencies:", list(currencies.keys()))

        if symbolWithdraw not in currencies:
            raise ValueError(f"Символ {symbolWithdraw} не найден в списке валют")

        currency_info = currencies[symbolWithdraw]
        network_info = currency_info.get('networks', {})

        # Вывод всех сетей для данной валюты
        print(f"Available networks for {symbolWithdraw}:", list(network_info.keys()))

        for network, network_data in network_info.items():
            if network_data['id'] == chainName or network == chainName:
                withdrawal_fee = network_data.get('fee', 0)
                print(f"Found fee: {withdrawal_fee} for network {network}")
                return withdrawal_fee

        raise ValueError(f"Не найдена сеть {chainName} для {symbolWithdraw}")

    except Exception as e:
        print(f"Ошибка при получении комиссии: {e}")
        # Возвращаем стандартное значение комиссии, если не удалось определить
        return 0

def shuffle(wallets_list, shuffle_wallets):
    numbered_wallets = list(enumerate(wallets_list, start=1))
    if shuffle_wallets.lower() == "yes":
        random.shuffle(numbered_wallets)
    elif shuffle_wallets.lower() == "no":
        pass
    else:
        raise ValueError("\n>>> Неверное значение переменной 'shuffle_wallets'. Ожидается 'yes' или 'no'.")
    return numbered_wallets

if __name__ == "__main__":
    with open("wallets.txt", "r") as f:
        wallets_list = [row.strip() for row in f if row.strip()]
        numbered_wallets = shuffle(wallets_list, shuffle_wallets)
        print(f'developed by th0masi [https://t.me/thor_lab]')
        print(f'Number of wallets: {len(wallets_list)}')
        print(f"CEX: {switch_cex}")
        print(f"Amount: {amount[0]} - {amount[1]} {symbolWithdraw}")
        print(f"Network: {network}")
        time.sleep(random.randint(2, 4))

        for wallet_number, address in numbered_wallets:
            amount_to_withdrawal = round(random.uniform(amount[0], amount[1]), decimal_places)
            choose_cex(address, amount_to_withdrawal, wallet_number)
            time.sleep(random.randint(delay[0], delay[1]))



