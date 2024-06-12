class TradingSignal:
    def __init__(self):
        self.last_action = 'SELL'  # Начальное состояние - не было покупок

    def get_signal(self, probability, up_down):
        if probability > 60 and up_down == 'UP':
            if self.last_action == 'SELL':
                self.last_action = 'BUY'
                return 'BUY'
            else:
                return 'WAIT'
        elif probability < 60 and up_down == 'UP':
            if self.last_action == 'BUY':
                self.last_action = 'SELL'
                return 'SELL'
            else:
                return 'WAIT'
        elif up_down == 'DOWN':
            if self.last_action == 'BUY':
                self.last_action = 'SELL'
                return 'SELL'
            else:
                return 'WAIT'


# Создаем объект класса TradingSignal
signal = TradingSignal()
