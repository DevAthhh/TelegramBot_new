import telebot
import threading
import time
import datetime

from src import bs, solves, calcKlines
from src.config import TOKEN

bot = telebot.TeleBot(TOKEN)

def main():
    thr_writing.start()
    thr_bs.start()
    thr_sl.start()

def buy_or_sell():
    while True:
        bot.send_message(-4217228648, bs_())
        time.sleep(1805)


def bs_():
    with open('drb/_balance.cat', 'r') as fr:
        balance = float(fr.readlines()[0])
        fr.close()
    with open('drb/_transactions.cat', 'r') as fr:
        trans = int(fr.readlines()[0])
        fr.close()
    
    req = solves.oracle_move()
    if req == 'NONE':
        return 'Ну там данных недостаточно, сорян'
    res_ = bs.get_signal(req[0], req[1])
    if res_ == 'BUY':
        balance -= float(calcKlines.get_price())
        with open('drb/_last_price.cat', 'w') as fw:
            fw.write(str(calcKlines.get_price()))
            fw.close()
        trans += 1
    elif res_ == 'SELL':
        balance += float(calcKlines.get_price()) * trans
        trans = 0
    balance = 0 if balance < 0 else balance
    
    with open('drb/_balance.cat', 'w') as fw:
        fw.write(str(balance))
        fw.close()
    with open('drb/_transactions.cat', 'w') as fw:
        fw.write(str(trans))
        fw.close()

    return f'Текущий баланс: {balance} 💵\nТекущее количество купленных коинов: {trans}🔥\nЧто я сделал? - {res_} ❤️'

def stop_loss():
    while True:
        res_ = bs.stop_loss()
        with open('drb/_balance.cat', 'r') as fr:
            balance = float(fr.readlines()[0])
            fr.close()
        with open('drb/_transactions.cat', 'r') as fr:
            trans = int(fr.readlines()[0])
            fr.close()

        if res_ == 'BUY':
            balance -= float(calcKlines.get_price())
            with open('drb/_last_price.cat', 'w') as fw:
                fw.write(str(calcKlines.get_price()))
                fw.close()
            bot.send_message(-4217228648, f'STOP_LOSS\n\nКрч, я чет купил.')
            trans += 1
        elif res_ == 'SELL':
            balance += float(calcKlines.get_price()) * trans
            bot.send_message(-4217228648, f'STOP_LOSS\n\nКрч, я все продал.')
            trans = 0
        balance = 0 if balance < 0 else balance

thr_writing = threading.Thread(target=calcKlines.calc_klines)
thr_bs = threading.Thread(target=buy_or_sell)
thr_sl = threading.Thread(target=stop_loss)

# main()

print('CAT\'s project\nAll licenses are owned by CAT Corporation.')
while True:
    current_time = datetime.datetime.now().time()
    print('waiting for 30 or 00 minutes...\n', str(current_time))
    if str(current_time)[3:5] == '00' or  str(current_time)[3:5] == '30':
        main()
        break
    time.sleep(10)
