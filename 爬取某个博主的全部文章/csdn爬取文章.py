import requests
import parsel
import tomd
import os
import re

#对一篇文章的爬取
def spider_one_csdn(title_url):    # 目标文章的链接
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
    "Referer": "https://blog.csdn.net/tansty_zh"
    }
    html=requests.get(url=title_url,headers=head).text
    page=parsel.Selector(html)
    #创建解释器
    title=page.css(".title-article::text").get()
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
    page=1
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
        "Referer": "https://blog.csdn.net/tansty_zh"
        }
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

def main():
    print("本项目由tansty开发")
    name=input("请输入博主的名称：")
    get_article_link(name)


if __name__ == '__main__':
    main()