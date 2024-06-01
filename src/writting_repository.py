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