#!python3
#encoding: utf-8
import requests
from bs4 import BeautifulSoup
import os
import os.path
import urllib.parse
import csv
from decimal import Decimal
"""
TSVから集計する。
* 完了: http://
* 成果物なし完了: -
* 未完: (未入力)
"""
class Aggregate(object):
    def __init__(self):
        self.__unfinished_num = 0
        self.__finished_num = 0
        self.__zero_num = 0
    
    def Run(self):
        self.__LoadTsv()
    
    @property
    def Total(self):
        return self.__total_num
    @property
    def Unfinished(self):
        return self.__unfinished_num
    @property
    def Finished(self):
        return self.__finished_num
    @property
    def ZeroFinished(self):
        return self.__zero_num
    @property
    def ProgressRate(self):
        return Decimal(self.__finished_num + self.__zero_num) / Decimal(self.__total_num) * Decimal(100)

    def __LoadTsv(self):
        self.__total_num = sum(1 for line in open('contents.tsv')) - 1 # 1行目のヘッダ行を読み飛ばす
        with open('contents.tsv', mode='r', encoding='utf-8') as f:
            tsv = csv.reader(f, delimiter='\t')
            next(tsv) # 1行目のヘッダ行を読み飛ばす
            for row in tsv:
                row2 = row[2].strip()
                if '' == row2:
                    self.__unfinished_num += 1
                elif '-' == row2:
                    self.__zero_num += 1
                elif row2.startswith('http://') or row2.startswith('https://'):
                    self.__finished_num += 1
                else:
                    raise Exception('tsvの3列目には空値,-,URLのどれかを記入してください。: {0}'.format(row))
            print('self.__total_num={0}'.format(self.__total_num))
            print('self.__unfinished_num={0}'.format(self.__unfinished_num))
            print('self.__finished_num={0}'.format(self.__finished_num))
            print('self.__zero_num={0}'.format(self.__zero_num))


if __name__ == '__main__':
    m = Aggregate()
    m.Run()

