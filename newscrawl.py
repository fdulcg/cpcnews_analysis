#coding:utf-8
import urllib.request
import logging
from bs4 import BeautifulSoup
import time
from lxml import etree
import sys
from pymongo import MongoClient

def createLogger():

    logger_name = "crawl"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler
    log_path = "error.log"
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARN)

    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger



def has_herf_and_traget(tag):
    return tag.has_attr('href') and tag.has_attr('target') and not tag.has_attr('coords') and not tag.has_attr('img')\


if __name__ == "__main__":
    logger = createLogger()
    client = MongoClient('mongodb://ip/')
    db_auth = client.XXX
    db_auth.authenticate('username', 'password')
    db = client.XXX

    # create logger
    urllist = []
    for page in range(1,8):
        url = 'http://cpc.people.com.cn/xuexi/GB/387489/index'+str(page)+'.html'
        print(page)
        try:
            response = urllib.request.urlopen(url)
            soup = BeautifulSoup(response,"lxml")
            for each in soup.find_all(has_herf_and_traget):
                # if 'http' in str(each) and 'paper' not in str(each)  and 'shtml':
                if 'class="red"' in str(each):
                    url = str(each).split('\"')
                    link = url[1]
                    if 'http' not in link:
                        link = 'http://cpc.people.com.cn'+link
                    if link not in urllist:
                        html = ''
                        title = ''
                        subtitle = ''
                        author = ''
                        contentlist = ''
                        secondTitle = ''

                        urllist.append(link)
                        artresp = urllib.request.urlopen(link)
                        html = artresp.read().decode('gbk')
                        root = etree.HTML(html)
                        textarea = root.xpath('//div[@class="text_c"]')
                        textarea2 = root.xpath('//div[@class="text_c clearfix"]')
                        textarea3 = root.xpath('//div[@class="d2_left d2txt_left fl"]')
                        if len(textarea)>0:
                            text = textarea[0]
                            subtitlepath = './h2'
                            contentpath = "./div[@class='show_text']/p"
                            contenttitlepath = "./div[@class='show_text']/p/strong"

                        elif len(textarea2)>0:
                            text = textarea2[0]
                            contentpath = "./div[@class='text_show']/p"
                            subtitlepath = './h4'
                            contenttitlepath = "./div[@class='text_show']/p/strong"
                        elif len(textarea3)>0:
                            text = textarea3[0]
                            contentpath = "./div[@class='d2txt_1 clear']/p"
                            subtitlepath = './h5'
                            contenttitlepath = "./div[@class='d2txt_1 clear']/p/strong"
                        else:
                            print('error    ' + link)
                        try:
                            title = text.find('./h1').text
                            subtitle = text.find(subtitlepath)

                            if subtitle is not None and len(subtitle)>0:
                                subtitle = subtitle.text
                            else:
                                subtitle = None
                            author = text.find("./p[@class='sou1']")
                            if author is not None and len(author)>0:
                                author = author.text
                            else:
                                author = None
                            content = text.findall(contentpath)
                            contenttitle = text.findall(contenttitlepath)
                            if len(content)>0:

                                for para in content:
                                    if para.text is not None:
                                        contentlist += para.text+'\n'
                            if len(contenttitle) > 0:

                                for t in contenttitle:
                                    if t.text is not None:
                                        secondTitle += t.text+'\n'
                        except Exception as es:
                            print(es)
                        db.update_one(
                            {'http':link},
                            {
                                '$set': {
                                    'html': html,
                                    'title':title,
                                    'subtitle':subtitle,
                                    'author':author,
                                    'content': contentlist,
                                    'titleInContent':secondTitle
                                }
                            },
                            upsert=True
                        )
                        # articlehtml = BeautifulSoup(artresp, "lxml")
                        # for line in articlehtml.find_all(style='text-indent: 2em;'):
                        #     print(line)

        except Exception as e1:
            print(url)
            print(e1)
            pass

        time.sleep(5)

    # import codecs
    # with codecs.open('url.txt','a','utf-8') as fin:
    #     for each in urllist:
    #         fin.writelines([each+'\n'])



    # soup = BeautifulSoup(html)