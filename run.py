import telebot
import threading
import time

from src import bs, solves, calcKlines
from src.config import TOKEN

bot = telebot.TeleBot(TOKEN)

def main():
    thr_writing.start()
    thr_bs.start()

def buy_or_sell():
    while True:
        bot.send_message(-4217228648, bs_())
        time.sleep(1804)


def bs_():
    with open('drb/_balance.cat', 'r') as fr:
        balance = float(fr.readlines()[0])
        fr.close()
    with open('drb/_transactions.cat', 'r') as fr:
        trans = int(fr.readlines()[0])
        fr.close()
    
    req = solves.oracle_move()
    res_ = bs.get_signal(req[0], req[1])
    if res_ == 'BUY':
        balance -= float(calcKlines.get_price())
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

    return f'Текущий баланс: {balance}💵\nТекущее количество купленных коинов: {trans}🔥\nЧто я сделал? - {res_}❤️'

thr_writing = threading.Thread(target=calcKlines.calc_klines)
thr_bs = threading.Thread(target=buy_or_sell)

main()
print('Хей!')