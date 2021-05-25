'''

    B 站视频下载
'''

import requests
from pyquery import PyQuery as pq
import re
import json
import time
requests.packages.urllib3.disable_warnings()

def getHtml(baseurl):
    head = {    #模拟浏览器身份头向对方发送消息
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"
    }
    try:
        response = requests.get(url = baseurl, headers = head)
        # 200表示服务器接受请求，会传回网页源代码，所以把文本内容传回来就行了
        if response.status_code==200:
            return response.text
    except:
        print("请求失败")

# 传入网址、p序列号。这里说明一下，我下载的视频在下载系列时直接用p号命名，方便起见所以这个函数要用p号
def getVideo(baseurl,p):
    html = getHtml(baseurl)
    c=re.findall(r'''"baseUrl":"(.*?)"''', html, re.S)[-2]
    # print(c)
    doc = pq(html)		# pyquery库语法简洁些，所以先采用pyquery库
    title = doc('#viewbox_report > h1 > span').text()	# 设置视频标题获取规则
    pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'	# 设置类的获取规则
    result = re.findall(pattern, html)[0]
    temp = json.loads(result)
    print(temp)
    print(("开始下载--->")+title)
    title = str(p)
    video_url = temp['data']['dash']['video'][0]['baseUrl']
    audio_url = temp['data']['dash']['audio'][0]['baseUrl']
    fileDownload(homeurl=baseurl, url=video_url, title=title, typ=0)
    fileDownload(homeurl=baseurl, url=c, title=title, typ=1)
    # try:
    #
    # except Exception:
    #     video_url = temp['data']['durl'][0]['url']
    #     fileDownload(homeurl=baseurl, url=video_url, title=title, typ=0)

def fileDownload(homeurl, url, title, typ):
    # 添加请求头键值对,写上 refered:请求来源
    headers = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"
    }
    headers.update({'Referer': homeurl})
    if typ==0:
        filename = "./"+title+".flv"
    else:
        filename = "./"+title+".mp3"
    res = requests.Session()
    # 视频总大小
    res2 = requests.get(url=url, headers=headers, verify=False)
    print(len(res2.content))
    # 指定每次下载1M的数据
    begin = 0
    end = 1024*1024 - 1
    print(end)
    flag = 0
    temp = 0
    while True:
        # 添加请求头键值对,写上 range:请求字节范围
        headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
        # 获取视频分片
        res = requests.get(url=url, headers=headers,verify=False)
        temp +=len(res.content)
        if res.status_code != 416:
# 响应码不为416时有数据，由于我们不是b站服务器，最终那个数据包的请求range肯定会超出限度，所以传回来的http状态码是416而不是206
            begin = end + 1
            end = end + (1024*1024)*2
        else:
            headers.update({'Range': str(end + 1) + '-'})
            res = requests.get(url=url, headers=headers,verify=False)
            flag=1
        with open(filename, 'ab') as fp:
            fp.write(res.content)
            fp.flush()
            print("filename: ",filename)
        if flag == 1:
            fp.close()
            break
    print("大小: ",temp)

def main():
    print("B站视频下载器")
    bv=input("输入视频bv号: ")
    judge = input("你想获得一系列(y)视频还是一个单一(N)视频?\n[y/N]\n")
    if judge == "y" or judge == "Y":
        max = input("输入该系列视频的总数: ")
        for p in range(max):
            baseurl = "https://www.bilibili.com/video/BV"+str(bv)+"?p="+str(p)
            getVideo(baseurl,p)
    else:
        p=input("如果是系列视频，请任选一集输入视频p号<------>如果不是系列视频，请输入'1'\n")
        baseurl = "https://www.bilibili.com/video/BV"+str(bv)+"?p="+str(p)
        getVideo(baseurl,p)
    print("下载完毕")


main()