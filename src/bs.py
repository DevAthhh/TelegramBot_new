from src.calcKlines import get_price

last_action = 'SELL'  # Начальное состояние - не было покупок

def get_signal (probability, up_down):
    global last_action
    if probability > 60 and up_down == 'UP':
        if last_action == 'SELL':
            last_action = 'BUY'
            return 'BUY'
        else:
            return 'WAIT'
    elif probability < 60 and up_down == 'UP':
        if last_action == 'BUY':
            last_action = 'SELL'
            return 'SELL'
        else:
            return 'WAIT'
    elif up_down == 'DOWN':
        if last_action == 'BUY':
            last_action = 'SELL'
            return 'SELL'
        else:
            return 'WAIT'

def stop_loss ():
    global last_action
    buy_price = 0

    with open('drb/_last_price.cat', 'r') as fr:
        buy_price = float(fr.readlines()[0])
        fr.close()

    actual_price = float(get_price())
    if actual_price <= buy_price - 50 and last_action == 'BUY':
        return 'BUY'
    elif actual_price <= buy_price - 100 and last_action == 'BUY':
        last_action = 'SELL'
        return 'SELL'
