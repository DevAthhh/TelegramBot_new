import websocket
import threading
import _thread
import json
import time

from src.helper import helpers

def wr_main():
    print(helpers.debug_msg('wr', 'start'))
    threading.Thread(target=SocketConnection, args=('wss://stream.bybit.com/v5/public/linear', ['kline.30.BTCUSDT'])).start()

class SocketConnection(websocket.WebSocketApp):
    def __init__(self, url, params=[]):
        super().__init__(url=url, on_open=self.on_open)

        self.params = params
        self.on_message = lambda ws, msg: self.message(msg)
        self.on_error = lambda ws, error: print(helpers.debug_msg('wr', f'error -{error}'))
        self.on_close = lambda ws: print('Closing')

        self.run_forever()

    def on_open(self, ws,):
        print(helpers.debug_msg('wr', 'websocket was opened'))

        def run(*args):
            tradeStr = {'op': 'subscribe', 'args': self.params}
            ws.send(json.dumps(tradeStr))

        _thread.start_new_thread(run, ())
    
    def message(self, msg):
        temp = ''
        with open('analysis_kline.ssb', 'a+') as file:
            file.write('{"open": ' + str(eval(msg.replace('f', 'F').replace('t', 'T'))['daTa'][0]['open']) + ', "close": ' 
                       + str(eval(msg.replace('f', 'F').replace('t', 'T'))['daTa'][0]['close']) + ', "low": '
                       + str(eval(msg.replace('f', 'F').replace('t', 'T'))['daTa'][0]['low']) + ', "high": '
                       + str(eval(msg.replace('f', 'F').replace('t', 'T'))['daTa'][0]['high']) + ', "volume": '
                       + str(eval(msg.replace('f', 'F').replace('t', 'T'))['daTa'][0]['volume']) + '}\n')
            file.close()
        print(helpers.debug_msg('wr', 'writing to the file is finished'))
        time.sleep(120)

def get_info():
    with open('analysis_kline.ssb', 'r') as file:
        lst_7_kline = file.read().split('\n')[-8:-1]
        file.close()
    for i in range(len(lst_7_kline)):
        lst_7_kline[i] = eval(lst_7_kline[i])
    
    #   Potential _res_pot
    _res_pot = 0
    _res_trend = 0

    for i in range(len(lst_7_kline) - 1):
        if lst_7_kline[i]['open'] > lst_7_kline[i + 1]['open']:
            _res_pot += 1
        else:
            _res_pot -= 1
        
        if lst_7_kline[i]['open'] > lst_7_kline[i + 1]['open']:
            _res_trend += 1
        else:
            _res_trend -= 1

    _res_pot = 'down' if _res_pot > 0 else 'up'
    _res_trend = 'down' if _res_trend > 0 else 'up'

    #   color _res_color_arr
    _res_color_arr = []
    for i in range(len(lst_7_kline)):
        if lst_7_kline[i]['open'] < lst_7_kline[i]['close']:
            _res_color_arr.append('green')
        else:
            _res_color_arr.append('red')

    #   trend _res_trend

    #   up level _res_up
    _res_up = 0
    _res_down = 0

    for i in range(len(lst_7_kline) - 1):
        if _res_color_arr[i] == 'green':
            if lst_7_kline[i]['close'] > lst_7_kline[i + 1]['close']:
                _res_up = lst_7_kline[i]['close']
        else:
            if lst_7_kline[i]['open'] > lst_7_kline[i + 1]['open']:
                _res_up = lst_7_kline[i]['close']
        
        if _res_color_arr[i] == 'green':
            if lst_7_kline[i]['close'] < lst_7_kline[i + 1]['close']:
                _res_down = lst_7_kline[i]['close']
        else:
            if lst_7_kline[i]['open'] < lst_7_kline[i + 1]['open']:
                _res_down = lst_7_kline[i]['close']
    
    #   down level _res_down

    #   length shadow _res_l_shadow_arr_high
    _res_l_shadow_arr_high = []
    _res_l_shadow_arr_low = []
    for i in range(len(lst_7_kline) - 1):
        _res_l_shadow_arr_high.append(lst_7_kline[i]['high'] - lst_7_kline[i]['close'])
        _res_l_shadow_arr_low.append(lst_7_kline[i]['low'] - lst_7_kline[i]['open'])
    
    #   body _res_body_arr
    _res_body_arr = []
    _res_volumes = []

    for i in range(len(lst_7_kline)):
        _res_body_arr.append(lst_7_kline[i]['close'] - lst_7_kline[i]['open'])
        _res_body_arr[i] = _res_body_arr[i] * -1 if _res_body_arr[i] < 0 else _res_body_arr[i]
        _res_volumes.append(lst_7_kline[i]['volume'])
    
    return [_res_trend, _res_color_arr, _res_up, _res_down, _res_volumes, [_res_l_shadow_arr_high, _res_l_shadow_arr_low], _res_body_arr, _res_pot]

print(get_info())