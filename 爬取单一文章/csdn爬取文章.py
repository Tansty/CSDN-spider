import requests
import parsel
import tomd
import os
import re

#对一篇文章的爬取
def spider_csdn(title_url):    # 目标文章的链接
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
    "Referer": "https://blog.csdn.net/tansty_zh"
    }
    html=requests.get(url=title_url,headers=head).text
    page=parsel.Selector(html)
    #创建解释器
    title=page.css(".title-article::text").get()
    content=page.css("article").get()
    content=re.sub("<a.*?a>","",content)
    content = re.sub("<br>", "", content)
    content = re.sub("&lt;", "<", content)  # 新增
    content = re.sub("&gt;", ">", content) # 新增
    text=tomd.Tomd(content).markdown
    #转换为markdown 文件
    path = os.getcwd()  # 获取当前的目录路径
    file_name = "./passage"
    final_road = path + file_name
    try:
        os.mkdir(final_road)
        print('创建成功！')
    except:
        print('目录已经存在或异常')
    with open(final_road+r"./"+title+".md",mode="w",encoding="utf-8") as f:
        f.write("#"+title)
        f.write(text)

def main():
    print("本项目由tansty开发")
    url = input("请输入网址：")
    spider_csdn(url)

if __name__ == '__main__':
    main()
