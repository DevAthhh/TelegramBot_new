import math

from src.helper import helpers
from src.writting_repository import get_info

def s_main():
    print(helpers.debug_msg('s', 'start'))
    data_for_solves = get_info()
    return solves(data_for_solves[0], data_for_solves[1], data_for_solves[2], data_for_solves[3], data_for_solves[4], data_for_solves[5], data_for_solves[6], data_for_solves[7])

def solves(trend, candle_array,
                up_level, down_level,
                volumes, shadows, body, 
                potential):
    coeff = 0

    # плюс - открытие вверх, минус - открытие вниз, чем больше модуль, тем увереннее открытие

    # ОПРЕДЕЛЕНИЕ КОЭФФИЦИЕНТОВ ПОД ТИПы СВЕЧИ
    if candle_array[1] == 'green':
        veryGood = 3
        good = 2
        ok = 1
        bad = -2
        veryBad = -3
    elif candle_array[1] == 'red':
        veryGood = -3
        good = -2
        ok = -1
        bad = 2
        veryBad = 3

    # РАЗМЕР ПРЕДПОСЛЕДНЕЙ СВЕЧИ
    if body[1] > body[2]:
        coeff += veryGood
    elif body[1] == body[2]:
        coeff += good

    # РАЗМЕР ТЕНИ ПРЕДПОСЛЕДНЕЙ ТЕНИ
    if shadows[1][1] < body[1] * .2:
        coeff += veryGood
    elif body[1] * .3 > shadows[1] > body[1] * .2:
        coeff += good
    elif body[1] * .4 > shadows[1] > body[1] * .3:
        coeff += ok
    else:
        coeff += veryBad

    # УЧЕТ ОБЪЕМОВ
    if volumes[1] > volumes[2]:
        coeff += veryGood
    elif volumes[1] == volumes[2]:
        coeff += good
    else:
        coeff -= veryBad

    # УРОВНИ СОПРОТИВЛЕНИЯ/ПОДДЕРЖКИ
    if candle_array == 'green' and up_level:
        coeff -= 3
    elif candle_array =='red' and down_level:
        coeff += 3

    # ТРЕНД
    if trend == 'UP':
        coeff += 1
    elif trend == 'DOWN':
        coeff -= 1
    
    # ПОТЕНЦИАЛ
    if potential == 'UP':
        coeff += 2
    elif potential == 'DOWN':
        coeff -= 2

    # ПОТЕНЦИАЛ И ТРЕНД
    if trend == 'UP' and potential == 'UP':
        coeff += 3
    elif trend == 'DOWN' and potential == 'DOWN':
        coeff -= 3
    
    if coeff > 0:
        return 'UP '
    elif coeff < 0:
        return 'DOWN '
    else:
        return 'ХЗ '

s_main()