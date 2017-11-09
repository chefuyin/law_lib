import re
import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.http import Request
from ..items import LawLibItem   #..为相对引用
import lxml.html
from urllib.parse import quote,unquote

class Myspider(scrapy.Spider):
    name='law_lib' #only one
    allowed_domains=['law-lib.com']
    base_url='http://law-lib.com/law/'
    department_index='bbdw-zy.htm'
    new_law_zy_index='http://www.law-lib.com/law/lawmlnew-zy.asp'
    new_law_df_index='http://www.law-lib.com/law/lawmlnew-df.asp'
    def start_requests(self):
        index_urls = [self.new_law_zy_index,self.new_law_df_index]
        for index_url in index_urls:
            yield Request(index_url,self.parse)
        # index_url=self.base_url+self.department_index#从中央单位开始爬
        # req= requests.get(index_url)
        # req.encoding='gb2312'
        # selector=lxml.html.fromstring(req.text)
        # urls=selector.xpath('//div[@class="law_df"]/p/a/@href')
        # department_urls=[]
        # for url in urls:
        #     if len(url.split('/'))==1:
        #         decode_url=url.split('=')[0]+'='+quote(url.split('=')[1],encoding='gb2312')
        #         url=self.base_url+decode_url
        #         department_urls.append(url)
        #     else:
        #         decode_url = url.split('=')[0] + '=' + quote(url.split('=')[1],encoding='gb2312')
        #         department_urls.append(decode_url)
        # for url in department_urls:
        #     yield Request(url,self.parse)

    def parse(self, response):
        selector=lxml.html.fromstring(response.text)
        list_pages=selector.xpath('//p[@class="p_fenye"]/a/@href')
        list=[]
        for page in list_pages:
            if len(page.split('/'))==1:
                page=self.base_url+page
                list.append(page)
            else:
                list.append(page)
        list.append(response.url)
        for url in list:
            yield Request(url,self.get_law_list)

    def get_law_list(self,response):
        selector=lxml.html.fromstring(response.text)
        law_list=selector.xpath('//ul[@class="law_list"]/li//span')
        for law in law_list:
            href=law[0].get('href')#law[0]==a标签
            if len(href.split('/'))==1:
                url=self.base_url+href.replace('law_view.','law_view1.')
            else:
                url=href.replace('law_view.','law_view1.')
            title=law[0].get('title')
            yield Request(url,self.get_law_page,meta={'title':title,'url':url})

    def get_law_page(self,response):
        selector = lxml.html.fromstring(response.text)
        db=selector.xpath('//div[@class="content_view"]/a/text()')
        if type(db)!=list:
            pass
        elif  db!=[]:
            if db[-1] == '在线数据库':
                pass
        else:
            item=LawLibItem()
            item['law_lib_url']=response.meta['url']
            item['title']=response.meta['title']
            infos=selector.xpath('//ul[@class="left_conul"]/li/text()')
            # print(infos)
            ptn1=re.compile(r"【颁布单位】.*?\Z")
            ptn2=re.compile(r"【颁布时间】.*?\Z")
            ptn3 = re.compile(r"【失效时间】.*?\Z")
            ptn4 = re.compile(r"【发文字号】.*?\Z")
            ptn5 = re.compile(r"【法规来源】.*?\Z")
            department=None
            publish_date=None
            invalid_date=None
            publish_number=None
            source=None
            for i in infos:
                match1=ptn1.findall(i)
                match2 = ptn2.findall(i)
                match3 = ptn3.findall(i)
                match4 = ptn4.findall(i)
                match5 = ptn5.findall(i)
                if match1:
                    result=match1[0].replace('【颁布单位】','')
                    if result!='':
                        department=result
                if match2:
                    result = match2[0].replace('【颁布时间】', '')
                    if result != '':
                        publish_date = result
                if match3:
                    result = match3[0].replace('【失效时间】', '')
                    if result != '':
                        invalid_date = result
                if match4:
                    result = match4[0].replace('【发文字号】', '')
                    if result != '':
                        publish_number = result
                if match5:
                    result = match5[0].replace('【法规来源】', '')
                    if result != '':
                        source = result
            # print(department,publish_date,invalid_date,publish_number,source)
            item['department']=department
            item['publish_date'] = publish_date
            item['invalid_date'] = invalid_date
            item['publish_number'] = publish_number
            item['source'] = source
            contents=selector.xpath('//div[@class="content_view"]/text()')
            content_list=[]
            for c in contents:
                if c.strip()=='':
                    pass
                else:
                    content_list.append(c.strip())
            content='\r\n'.join(content_list)
            item['content']=content
            return item
            # print(item)





