kline = 0
with open('drb/_klines.cat', 'r') as fr:
            str_kline = fr.readlines()
            for i in range(len(str_kline)):
                str_kline[i] = eval(str_kline[i])
            kline = str_kline
            fr.close()

print(kline)