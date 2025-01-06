import requests
from typing import Dict, Tuple, Optional
from config import CMC_API_KEY, CRYPTO_LIST

class CryptoService:
    @staticmethod
    def get_crypto_rates() -> Optional[Dict]:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
        params = {'symbol': ','.join(CRYPTO_LIST), 'convert': 'USD'}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()

            rates = {
                coin: {
                    'price': data['data'][coin]['quote']['USD']['price'],
                    'change_24h': data['data'][coin]['quote']['USD']['percent_change_24h']
                } for coin in CRYPTO_LIST
            }

            rates['bitcoin_dominance'] = round(data['data']['BTC']['quote']['USD'].get('market_cap_dominance', 'N/A'), 1)
            return rates
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return None

    @staticmethod
    def get_fear_and_greed_index() -> Tuple[str, str]:
        url = 'https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest'
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            return (
                str(data['data']['value']), 
                data['data']['value_classification']
            )
        except Exception as e:
            print(f"Ошибка при получении индекса страха и жадности: {e}")
            return 'N/A', 'N/A'

    @staticmethod
    def get_top_performer():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
        params = {
            'limit': '1000',
            'sort': 'percent_change_24h',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()

            top_100_performers = [
                coin for coin in data['data'] 
                if coin['cmc_rank'] <= 100 and coin['quote']['USD']['market_cap'] > 700_000_000
            ]

            if top_100_performers:
                top_performer = top_100_performers[0]
                return {
                    'name': top_performer.get('name', 'N/A'),
                    'symbol': top_performer.get('symbol', 'N/A'),
                    'price': top_performer.get('quote', {}).get('USD', {}).get('price', 'N/A'),
                    'change_24h': top_performer.get('quote', {}).get('USD', {}).get('percent_change_24h', 'N/A')
                }
            else:
                return {
                    'name': 'N/A',
                    'symbol': 'N/A',
                    'price': 'N/A',
                    'change_24h': 'N/A'
                }
        except Exception as e:
            print(f"Ошибка при получении данных о топ-выигрывающих монетах: {e}")
            return {
                'name': 'N/A',
                'symbol': 'N/A',
                'price': 'N/A',
                'change_24h': 'N/A'
            }

    @staticmethod
    def calculate_altcoin_season_index():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {'X-CMC_PRO_API_KEY': CMC_API_KEY}
        params = {'limit': '100', 'convert': 'USD', 'sort': 'market_cap'}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()

            if 'data' not in data or not data['data']:
                return None

            excluded_tokens = {'USDT', 'USDC', 'DAI', 'WBTC', 'stETH', 'cLINK', 'BUSD'}
            top_100_coins = [coin for coin in data['data'] if coin['symbol'] not in excluded_tokens]

            bitcoin = next((coin for coin in data['data'] if coin['symbol'] == 'BTC'), None)
            if not bitcoin:
                return None

            bitcoin_90d_change = bitcoin['quote']['USD'].get('percent_change_90d', 0)
            outperforming_coins = [
                coin for coin in top_100_coins
                if coin['quote']['USD'].get('percent_change_90d', 0) > bitcoin_90d_change
            ]

            altcoin_season_index = (len(outperforming_coins) / len(top_100_coins)) * 100
            return round(altcoin_season_index, 1)
        except Exception as e:
            print(f"Ошибка при расчете индекса альт-сезона: {e}")
            return None

    @staticmethod
    def get_season_visualization(index):
        if index is None:
            return "<b>BTC -</b>🟧🟧🟧🟦🟦🟦🟦🟦🟦<b>- ALT.</b>", 50

        btc_percentage = 100 - index
        btc_blocks = int(btc_percentage // 10)
        alt_blocks = int(index // 10)

        visualization = f"<b>BTC -</b>" + "🟧" * btc_blocks + "🟦" * alt_blocks + "<b>- ALT.</b>"
        return visualization, btc_percentage