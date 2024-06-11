import requests
import time

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

def calc_klines():
    kline = {
        'open': 0,
        'high': 0,
        'low': 0,
        'close': 0,
        'color': ''
    }

    #   Recording primary data
    price = get_price()
    kline['open'] = price
    kline['high'] = price
    kline['low'] = price
    count_time = 0

    while True:
        start_time = time.time()
        price = get_price()
        if kline['high'] < price:
            kline['high'] = price
        if kline['low'] > price:
            kline['low'] = price
        count_time += 1

        print(f'High: {kline["high"]}\nLow: {kline["low"]}\n\n')
        end_time = time.time()
        print(end_time - start_time)
        time.sleep(1.3)

####################################################################### разделение между таймфреймами ######################################################################

        if count_time == 900:
            kline['close'] = get_price()
            kline['color'] = 'red' if kline['close'] < kline['open'] else 'green'
            print(kline)
            count_time
            with open('drb/_klines.cat', 'a+') as fr:
                fr.write(str(kline) + '\n')
        continue
calc_klines()
