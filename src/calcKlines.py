import requests
import time
from datetime import datetime, timedelta
import pytz # Для работы с временными зонами
def get_price():
    type_coin = 'BTC'

    try:
        with open('drb/config.txt', 'r') as f:
            str_cfg = f.readlines()[0]
            str_cfg = str_cfg[str_cfg.find('=') + 1:].upper()
            type_coin = str_cfg
            f.close()
    except Exception as e:
        print('<global> the file was not found')


    url = "https://api.bybit.com/v2/public/tickers?symbol=BTCUSD"
    response = requests.get(url)
    data = response.json()
    if data and 'result' in data:
        for item in data['result']:
            if item['symbol'] == f'{type_coin}USD':
                return item['last_price']
    return "Цена не найдена"

############################################################### Получение объемов с coingecko ###########################################################################
def get_btc_volume():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    return data['market_data']['total_volume']['usd']


############################################################### Конец ###########################################################################

def calc_klines():
    kline = {
        'open': 0,
        'high': 0,
        'low': 0,
        'close': 0,
        'color': '',
        'volume': 0
    }

    #   Recording primary data
    price = get_price()
    kline['open'] = price
    kline['high'] = price
    kline['low'] = price
    count_time = 0
    temp_vol = get_btc_volume()

    while True:
        price = get_price()
        if kline['high'] < price:
            kline['high'] = price
        if kline['low'] > price:
            kline['low'] = price
        count_time += 1

        print(f'High: {kline["high"]}\nLow: {kline["low"]}\n\n')
        time.sleep(2)

####################################################################### разделение между таймфреймами ######################################################################

        if count_time == 900:
            kline['close'] = get_price()
            kline['color'] = 'RED' if kline['close'] < kline['open'] else 'GREEN'

            #   Recording volume
            kline['volume'] = get_btc_volume() - temp_vol
            temp_vol = get_btc_volume()

            print(kline)
            count_time = 0
            with open('drb/_klines.cat', 'a+') as fr:
                fr.write(str(kline) + '\n')
                fr.close()
            
        continue

calc_klines()
