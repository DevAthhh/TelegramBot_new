last_action = 'SELL'  # Начальное состояние - не было покупок

def get_signal (probability, up_down):

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
    if actual_price() <= get_price() - 50 and last_action == 'BUY':
        return 'BUY'
    elif actual_price() <= get_price() - 100 and last_action == 'BUY':
        return 'SELL'
        last_action = 'SELL'
