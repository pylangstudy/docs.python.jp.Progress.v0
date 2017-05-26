#!python3
#encoding: utf-8
import requests
from bs4 import BeautifulSoup
import os
import os.path
import urllib.parse
"""
https://docs.python.jp/3/contents.htmlから見出しを取り出してTSV化する。
URL,タイトル,リポジトリURLの3列。リポジトリURLは手入力する。今回はURLとタイトルだけを出力すればいい。
"""
class Main(object):
    def __init__(self):
        self.__base_dir = os.path.abspath(os.path.dirname(__file__))
    
    def Run(self):
        self.__MakeTsv(self.__HttpGetPyDocToC())
    
    def __HttpGetPyDocToC(self):
        if not os.path.isfile(self.__GetHtmlFilePath()):
            url = 'https://docs.python.jp/3/contents.html'
            r = requests.get(url)
            r.raise_for_status()
            print(r.encoding) # ISO-8859-1
            r.encoding = r.apparent_encoding # http://qiita.com/nittyan/items/d3f49a7699296a58605b
            print(r.encoding) # utf-8
            with open(self.__GetHtmlFilePath(), 'w', encoding='utf-8') as f:
                f.write(r.text)
        with open(self.__GetHtmlFilePath()) as f:
            return BeautifulSoup(f.read(), 'lxml') # html.parser, lxml
            
    def __GetHtmlFilePath(self):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'contents.html')
    
    def __MakeTsv(self, soup):
        if not os.path.isfile('contents.tsv'):
            tree = soup.find('div', class_='toctree-wrapper compound') # 2個目に取得できるものは空だから1個目を取る
            tsv_str = ''
            tsv_str += 'DocumentUrl' + '\t' + 'Title' + '\t' + 'GitHubUrl' + '\n'
            for a in tree.find_all('a'):
                print(a.get('href'))
                print(''.join(a.stripped_strings))
                tsv_str += a.get('href') + '\t' + ''.join(a.stripped_strings) + '\t' + '\n'
            with open('contents.tsv', mode='w', encoding='utf-8') as f:
                f.write(tsv_str)    


if __name__ == '__main__':
    m = Main()
    m.Run()

