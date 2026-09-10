#怎么发送请求
#pip install requests
import requests

#pip install lxml
from lxml import etree

#发送给谁
url = "https://www.wyshu.com/wl/douluodaliu/216992.html"
with open("斗罗大陆.txt", "w", encoding="utf-8") as f:
    pass

#while循环
while True:

    #伪装自己
    headers ={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36 Edg/152.0.0.0"
        }

        #发送请求
    response = requests.get(url,headers=headers)


        #设置编码
    response.encoding = "utf-8"

        #响应信息
        #print(response.text)

    e = etree.HTML(response.text)
    info = "\n".join(e.xpath("//article[@class='article-post']/p/text()"))
    title = e.xpath("//title/text()")[0]
    url = "https://www.wyshu.com" + e.xpath("//div[@class='col-md-12 col-lg-10']/p[1]/a/@href")[0]
    #last_url = e.xpath("//div[@class='col-md-12 col-lg-10']/p[2]/a/@href")[0]
        #查找具体文本信息（可有可无，纯熟自找）
        #text = response.text
        #print("大魂师是什么意思？" in text)
        #print(text.find("什么是觉醒仪式"))
        #print(text[15210:16510])
        #遍历列表"\xao"字符替换为空格并去掉首尾空格，l.append返回的值是None，l列表才是我们想要的
    l = []
    #for i in info:
        #l.append(i.replace("\xa0"," ").strip())
        #x = "\n".join(l)
        #print(x)

    print(title)
        #保存
    with open("斗罗大陆.txt","a",encoding="utf-8") as f:
        f.write(title + '\n\n' + info +'\n\n')
    
    if "本书完" in response.text:
        print("小说已经结束")
        break