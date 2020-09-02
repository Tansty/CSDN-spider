import requests
import parsel
import tomd
import os
import re
from selenium import webdriver


head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
    "Referer": "https://blog.csdn.net/tansty_zh"
    }

def filter_str(desstr,restr=''):
    #过滤除中英文及数字以外的其他字符
    res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    return res.sub(restr, desstr)
#对一篇文章的爬取
def spider_one_csdn(title_url):    # 目标文章的链接
    html=requests.get(url=title_url,headers=head).text
    page=parsel.Selector(html)
    #创建解释器
    title=page.css(".title-article::text").get()
    title=filter_str(title)
    print(title)
    content=page.css("article").get()
    content=re.sub("<a.*?a>","",content)
    content = re.sub("<br>", "", content)
    #过滤a标签和br标签
    text=tomd.Tomd(content).markdown
    #转换为markdown 文件
    path = os.getcwd()  # 获取当前的目录路径
    file_name = "./passage"
    final_road = path + file_name
    try:
        os.mkdir(final_road)
        print('创建成功！')
    except:
        # print('目录已经存在或异常')
        pass
    with open(final_road+r"./"+title+".md",mode="w",encoding="utf-8") as f:
        f.write("#"+title)
        f.write(text)

def get_article_link(user):
    #获取某个博主的所有文章
    page=1
    while True:
        link = "https://blog.csdn.net/{}/article/list/{}".format(user, page)
        print("现在爬取第", page, "页")
        html = requests.get(url=link, headers=head).text
        cel = parsel.Selector(html)
        name_link = cel.css(".article-list h4 a::attr(href) ").getall()
        if not name_link:
            break
            #没有文章就退出
        for name in name_link:
            spider_one_csdn(name)
        page+=1


def nb_bozhu():
    #获取前十博主的csdn名称
    driver=webdriver.Chrome("chromedriver.exe")
    driver.implicitly_wait(10)
    driver.get("https://blog.csdn.net/rank/writing_rank")
    names=driver.find_elements_by_xpath("//div[@class='rank-item-box d-flex align-items-center']//div[@class='name d-flex align-items-center']/h2/a")
    name_list=[]
    for name in names:
        final_name=name.get_attribute("outerHTML")
        final_name=re.sub('<a href="https://blog.csdn.net/',"",final_name)
        final_name=re.sub('">.*</a>','',final_name)
        name_list.append(final_name)
        print(final_name)
    driver.quit()
    return name_list

def main():
    print("本项目由tansty开发")
    #name=input("请输入博主的名称：")
    #get_article_link(name)
    names=nb_bozhu()
    for name in names:
        get_article_link(name)
        break

if __name__ == '__main__':
    main()