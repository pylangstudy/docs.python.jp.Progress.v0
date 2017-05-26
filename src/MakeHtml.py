#!python3
#encoding: utf-8
import requests
from bs4 import BeautifulSoup
import os
import os.path
import urllib.parse
import csv
import Aggregate
"""
https://docs.python.jp/3/contents.htmlから見出しを取り出したTSVを使ってHTMLを出力する。
"""
class Main(object):
    def __init__(self):
        self.__aggregate = Aggregate.Aggregate()
        self.__base_dir = os.path.abspath(os.path.dirname(__file__))
    
    def Run(self):
        self.__aggregate.Run()
        self.__MakeHtml(self.__LoadTsv())
    
    def __LoadTsv(self):
        with open('contents.tsv', mode='r', encoding='utf-8') as f:
            return csv.reader(f, delimiter='\t')

    def __MakeHtml(self, tsv):
#        html_str = '<html><head>{html_head}</head><body><table id="Aggregate">{aggregate}</table><table id="List">{header_list}</table></body></html>'.format(html_head=self.__CreateHtmlHeader(), aggregate=self.__CreateAggregateTable(), header_list=self.__CreateHeadingTable())
#        html_str = '<html><head>{html_head}</head><body><table id="Aggregate">{aggregate}</table><table id="List">{header_list}</table></body></html>'.format(html_head=self.__CreateHtmlHeader(), aggregate=self.__CreateAggregateTable(), header_list="")
        html_str = '<html><head>{html_head}</head><body><table id="Aggregate">{aggregate}</table><table id="List">{header_list}</table></body></html>'.format(html_head=self.__CreateHtmlHeader(), aggregate="", header_list="")
        with open('index.html', mode='w', encoding='utf-8') as f:
            f.write(html_str)
    
    def __CreateHtmlHeader(self):
        return ('<meta charset="UTF-8">' + 
        '<link rel="stylesheet" href="ContentsView.css">' + 
        '<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.7.2/d3.min.js"></script>' + 
        '<script type="text/javascript" src="ContentsView.js"></script>')
        
    def __CreateAggregateTable(self):
        return ('<tr><th>進捗率</th><td>{0} % ({1}/{2})</td></tr>'.format(self.__aggregate.ProgressRate, (self.__aggregate.Finished + self.__aggregate.ZeroFinished), self.__aggregate.Total) + 
            '<tr><th title="完了 成果物あり"><img src="http://www.google.com/s2/favicons?domain=github.com"></img></th><td>{0}</td></tr>'.format(self.__aggregate.Finished) + 
            '<tr><th title="完了 成果物なし"><span>-</span></th><td>{0}</td></tr>'.format(self.__aggregate.ZeroFinished) + 
            '<tr><th title="未完">未</th><td>{0}</td></tr>'.format(self.__aggregate.Unfinished))
        
    def __CreateHeadingTable(self):
        th_str = '<tr><th title="成果物">果</th><th>参照元</th></tr>'
        td_str = ''
        with open('contents.tsv', mode='r', encoding='utf-8') as f:
            tsv = csv.reader(f, delimiter='\t')
            next(tsv) # 1行目のヘッダ行を読み飛ばす
            for row in tsv:
                td_str += '<tr class="{0}"><td>{1}</td><td>{2}</td></tr>'.format(
                    self.__GetClass(row[2]), 
                    self.__GetArtifactsHtml(row),
                    self.__GetReferenceHtml(row))
        return th_str + td_str
    
    def __GetClass(self, github_url):
        if '' == github_url:
            return 'Unfinished'
        elif '-' == github_url:
            return 'ZeroFinished'
        elif github_url.startswith('http://') or github_url.startswith('https://'):
            return 'Finished'
        else:
            raise Exception('tsvの3列目には空値,-,URLのどれかを記入してください。: {0}'.format(row))
        
    def __GetArtifactsHtml(self, row):
        if '' == row[2]:
            return '<span>未</span>'
        elif '-' == row[2]:
            return '<span>-</span>'
        elif row[2].startswith('http://') or row[2].startswith('https://'):
            return '<a href="{0}" title="{1}"><img src="http://www.google.com/s2/favicons?domain={2}"></a></img>'.format(row[2], os.path.basename(row[2]), urllib.parse.urlparse(row[2]).netloc)
        else:
            raise Exception('tsvの3列目には空値,-,URLのどれかを記入してください。: {0}'.format(row))
    
    def __GetReferenceHtml(self, row):
        return '<a href="https://docs.python.jp/3/{0}">{1}</a>'.format(row[0], row[1])
    
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

