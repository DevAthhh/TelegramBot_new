def oracle_move():
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

    kline = 0.0

    try: 
        with open('drb/_klines.cat', 'r') as fr:
            str_kline = fr.readlines()
            for i in range(len(str_kline)):
                str_kline[i] = eval(str_kline[i])
            kline = str_kline
            fr.close()
            kline.reverse()
        for i in range(len(kline)):
            kline[i]['open'] = float(kline[i]['open'])
            kline[i]['close'] = float(kline[i]['close'])
            kline[i]['high'] = float(kline[i]['high'])
            kline[i]['low'] = float(kline[i]['low'])
            kline[i]['volume'] = float(kline[i]['volume'])
    except Exception as e:
        print('Попытка получить данные не увенчалась успехом')
                
    # Функция для расчета тренда
    try:
        if kline[25]['close'] > kline[1]['close']:
            trend = 'DOWN'
        elif kline[25]['close'] < kline[1]['close']:
            trend = 'UP'
        else:
            trend = 'NEUTRAL'
    except Exception as e:
        print('Недостаточное количество данных для записи тренда')

    for i in range(8):
        if kline[i]['close'] > kline[i + 1]['close']:
            up_level = kline[i]['close']
        elif kline[i]['close'] < kline[i + 1]['close']:
            down_level = kline[i]['close']

    # Функция для расчета потенциала
    try:
        if kline[4]['close'] > kline[1]['close']:
            potential = 'DOWN'
        elif kline[4]['close'] < kline[1]['close']:
            potential = 'UP'
        else:
            potential = 'NEUTRAL'
    except Exception as e:
        print('Недостаточное количество данных для записи потенциала')

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
    if kline[1]['color'] == 'GREEN' and up_level - 50 < kline[1]['close'] < up_level + 50:
        coefficient += ratings['veryBad']
    elif kline[1]['color'] == 'RED' and down_level + 50 > kline[1]['close'] > down_level - 50:
        coefficient += ratings['veryGood']

    # Тела последних
    body_1 = abs(kline[1]['open'] - kline[1]['close']) # тело предпоследней свечи
    body_2 = abs(kline[2]['open'] - kline[2]['close']) # тело пред предпоследней свечи

    # Тени предпоследней
    if kline[1]['color'] == 'GREEN': # Бычья свеча (green)
        upper_shadow = kline[1]['high'] - kline[1]['close']
        lower_shadow = kline[1]['open'] - kline[1]['low']
    else:  # Медвежья свеча (красная)
        upper_shadow = kline[1]['high'] - kline[1]['open']
        lower_shadow = kline[1]['close'] - kline[1]['low']

    # Коэффициент в зависимости от теней
    if upper_shadow + lower_shadow < body_1 * .2 and kline[1]['color'] == 'GREEN':
        coefficient += ratings['veryGood']
    elif upper_shadow + lower_shadow < body_1 * .3 and kline[1]['color'] == 'GREEN':
        coefficient += ratings['good']
    elif upper_shadow + lower_shadow < body_1 * .3 and kline[1]['color'] == 'RED':
        coefficient += ratings['bad']
    elif upper_shadow + lower_shadow < body_1 * .3 and kline[1]['color'] == 'RED':
        coefficient += ratings['veryBad']

    # Коэффициент в зависимости от тела
    if body_1 > body_2 and kline[1]['color'] == 'GREEN':
        coefficient += ratings['veryGood']
    elif body_1 == body_2 and kline[1]['color'] == 'GREEN':
        coefficient += ratings['good']
    elif body_1 == body_2 and kline[1]['color'] == 'RED':
        coefficient += ratings['bad']
    elif body_1 > body_2 and kline[1]['color'] == 'RED':
        coefficient += ratings['veryBad']

    if kline[1]['volume'] >= kline[2]['volume'] and kline[1]['color'] == 'GREEN':
        coefficient += ratings['veryGood']
    elif kline[2]['volume'] - 10 < kline[1]['volume'] < kline[2]['volume'] and kline[1]['color'] == 'GREEN':
        coefficient += ratings['good']
    elif kline[1]['volume'] >= kline[2]['volume'] and kline['color'][1] == 'RED':
        coefficient += ratings['veryBad']
    elif kline[2]['volume'] - 10 < kline[1]['volume'] < kline[2]['volume'] and kline[1]['color'] == 'RED':
        coefficient += ratings['bad']

    max_coeff = 16
    min_coeff = -16

    if coefficient >= 0:
        probability = (coefficient / max_coeff) * 100
    else:
        probability = (coefficient / min_coeff) * 100  

    # Результат
    if coefficient > 0:
        return [probability, 'UP']
    elif coefficient < 0:
        return [probability, 'DOWN']



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