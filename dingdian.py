from selenium import webdriver
from bs4 import BeautifulSoup
from selenium .webdriver.common.keys import Keys
from multiprocessing import Pool
import requests
import time
import re
import os

class Dingdian(object):
    def __init__(self, search_name):
        self.search_name = search_name
        self.driver = webdriver.Firefox()

    def search_book(self,search_name):
        self.driver.get('http://www.23us.com/')
        assert"顶点" in self.driver.title
        print ('正在搜素请等待')
        elem = self.driver.find_element_by_name('search-btn')
        elem.send_keys(self.search_name)
        elem.send_keys(Keys.RETURN)
        self.driver.switch_to.window(self.driver.window_handles[1])
        info = self.driver.page_source
        print('已获取信息')
        return info


    def get_search_url(self,search_name):
        info = self.search_book(search_name)
        p = r'<a cpos="title" href="(.*?)" title="(.*?)"'
        result = re.findall(p,info)
        if result:
            for i in result:
                if search_name in i :
                    print(i[0])
                    return i[0]
                else:
                    pass
        else:
            print('找不到结果，正则匹配或许有误')


    def get_all_url(self,search_name):
        li = []
        url = self.get_search_url(search_name)
        soup = BeautifulSoup(self.get_html(url),'lxml')
        all_td = soup.find_all('td',class_="L")
        for a in all_td:
            try:
                html = a.find('a').get('href')
                htmls = url + html
                li.append(htmls)
            except:
                pass
        return li

    def download_book(self,search_name):
        lis = self.get_all_url(search_name)
        for e in lis:
            soup = BeautifulSoup(self.get_html(e),'lxml')
            title = soup.title.text.split('-')[1]
            all_info = soup.find('dd',id="contents")
            p = r'<dd id="contents">(.*?)</dd>'
            try:
                info = re.findall(p,str(all_info),re.S)[0]
                with open(title+'.txt','w',encoding='gbk',errors='ignore')as f:
                    f.write(info.replace('<br/>','\n'))
                    print('save sucessful:%s' % title)

            except:
                print('faild to print %s' % title)
    def get_html(self,url):
        headers ={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html = requests.get(url,headers=headers).content

        return html


if __name__ == '__main__'
    search_name = input('请输入要下载的小说名字：')
    test = Dingdian(search_name)
  
    
