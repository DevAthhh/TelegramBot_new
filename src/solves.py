# Изначальный коэффициент
coefficient = 0

# Словарь для хранения оценок
ratings = {
    "veryGood": 4,
    "good": 2,
    "ok": 0,
    "bad": -2,
    "veryBad": -4
}
kline = {
    'open': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    'high': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    'low': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    'color': ['GREEN', 'RED', 'GREEN', 'RED', 'GREEN', 'GREEN', 'GREEN']
}
              
# Функция для расчета тренда
if len(kline['close']) < 25:
    raise ValueError("Недостаточно данных для расчета тренда")

if kline['close'][25] > kline['close'][1]:
    trend = 'DOWN'
elif kline['close'][25] < kline['close'][1]:
    trend = 'UP'
else:
    trend = 'NEUTRAL'

# Функция для расчета потенциала
if len(kline['close']) < 4:
    raise ValueError("Недостаточно данных для расчета потенциала")

if kline['close'][4] > kline['close'][1]:
    potential = 'DOWN'
elif kline['close'][4] < kline['close'][1]:
    potential = 'UP'
else:
    potential = 'NEUTRAL'

# Коэффициент в зависимости от тренда и потенциала
if trend == potential == 'UP':
    coefficient += ratings['veryGood']
elif trend == potential == 'DOWN':
    coefficient += ratings['veryBad']
elif trend != potential and potential == 'UP':
    coefficient += ratings['good']
elif trend != potential and potential == 'DOWN':
    coefficient += ratings['bad']
elif trend == potential == 'NEUTRAL':
    coefficient += ratings['ok']

# Коэффициент в зависимости от областей поддержки и сопротивления
if kline[1]['color'] == 'GREEN' and # ОБЛАСТЬ СОПРОТИВЛЕНИЯ - 10 < klines[1]['close'] < ОБЛАСТЬ СОПРОТИВЛЕНИЯ + 10: 
    coefficient += ratings['bad']
elif kline[1]['color'] == 'RED' and # ОБЛАСТЬ ПОДДЕРЖКИ + 10 < klines[1]['close'] < ОБЛАСТЬ СОПРОТИВЛЕНИЯ - 10: 
    coefficient += ratings['good']

# Тела последних
body_1 = abs(kline['open'][1] - kline['close'][1]) # тело предпоследней свечи
body_2 = abs(kline['open'][2] - kline['close'][2]) # тело пред предпоследней свечи

# Тени предпоследней
if kline['color'][1] == 'GREEN': # Бычья свеча (green)
    upper_shadow = kline['high'][1] - kline['close'][1]
    lower_shadow = kline['open'][1] - kline['low'][1]
else:  # Медвежья свеча (красная)
    upper_shadow = kline['high'][1] - kline['open'][1]
    lower_shadow = kline['close'][1] - kline['low'][1]

# Коэффициент в зависимости от теней
if upper_shadow + lower_shadow < body_1 * .2 and kline['color'][1] == 'GREEN':
    coefficient += ratings['veryGood']
elif upper_shadow + lower_shadow < body_1 * .3 and kline['color'][1] == 'GREEN':
    coefficient += ratings['good']
elif upper_shadow + lower_shadow < body_1 * .3 and kline['color'][1] == 'RED':
    coefficient += ratings['bad']
elif upper_shadow + lower_shadow < body_1 * .3 and kline['color'][1] == 'RED':
    coefficient += ratings['veryBad']

# Коэффициент в зависимости от тела
if body_1 > body_2 and kline['color'][1] == 'GREEN':
    coefficient += ratings['veryGood']
elif body_1 == body_2 and kline['color'][1] == 'GREEN':
    coefficient += ratings['good']
elif body_1 == body_2 and kline['color'][1] == 'RED':
    coefficient += ratings['bad']
elif body_1 > body_2 and kline['color'][1] == 'RED':
    coefficient += ratings['veryBad']

# Коэффициент в зависимости от объемов
if volume[1] >= volume[2] and kline['color'][1] == 'GREEN':
    coefficient += ratings['veryGood']
elif volume[2] - 10 < volume[1] < volume[2] and kline['color'][1] == 'GREEN':
    coefficient += ratings['good']
elif volume[1] >= volume[2] and kline['color'][1] == 'RED':
    coefficient += ratings['veryBad']
elif volume[2] - 10 < volume[1] < volume[2] and kline['color'][1] == 'RED':
    coefficient += ratings['bad']

# Результат
if coefficient > 0:
    print("UP")
elif coefficient < 0:
    print("DOWN")



# Функция для определения свечи молот
# Функция для определения свечи доджи
# Функция для определения поглощения

# Индикатор RSI
# Индикатор MACD
# Скользящие средние (50 и 200)
# EMA (Exponential Moving Average)
# Bollinger Bands
# Stochastic Oscillator
# ADX (Average Directional Movement Index)
# Объемы (Rolling average for smoothing)