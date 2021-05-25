'''

    B站视频 封面获取
'''

import requests
import re
import urllib3
import USER_AGENT
from IPAgent import IPagent
import os
import sys

# 消除 已经关闭认证（verify=False）情况下，控制台会输出以下错误
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 获取B站视频封面类
class TitlePage:
    URL = str
    def __init__(self, user_agent="macOS"):

        self._imageUrl = ""
        self._imgPath = ""

        # 根据当前系统使用不同的 用户代理
        self._user_agent = USER_AGENT.get_user_agent()
        # 代理ip池对象
        self._ip = IPagent()


    # 设置路径
    def setPath(self,path:str):
        if path:
            if not (path[-1] == "/"):
                self._imgPath = path+r"/"
        else:
            # 当前路径
            self._imgPath = os.path.dirname(sys.argv[0])

    # 获取路径
    def getPath(self):
        return self._imgPath

    # 获取网页文本
    def getHtml(self,baseurl)->str:
        head = {  # 模拟浏览器身份头向对方发送消息
            "user-agent": self._user_agent
        }
        # 使用代理ip
        http = self._ip.getIP()
        if http:
            proxies = {
                http["type"]: '{}:{}'.format(http["ip"], http["port"])
            }
        else:
            proxies = {}
        try:
            response = requests.get(url=baseurl, headers=head, verify=False,proxies=proxies)
            # 200表示服务器接受请求，会传回网页源代码，所以把文本内容传回来就行了
            if response.status_code == 200:
                # # print(response.text)
                return response.text
        except:
            pass
            # print("请求失败")

    # 获取图片链接
    def getImageUrl(self,htmlText:str):
        temp = re.findall("itemprop=\"image\" content=\"(http://i.*?.png)\">",htmlText)
        # # print("图片链接:",temp)
        try:
            if temp:
                if len(temp[0]) < 80:
                    self._imageUrl = temp
                else:
                    self._imageUrl = re.findall("itemprop=\"image\" content=\"(http://i.*?.jpg)\">", htmlText)
            else:
                if len(temp[0]) < 80:
                    self._imageUrl = re.findall("itemprop=\"image\" content=\"(http://i.*?.jpg)\">",htmlText)
                else:
                    self._imageUrl = re.findall("itemprop=\"image\" content=\"(http://i.*?.png)\">",htmlText)
            # print(self._imageUrl)
        except Exception:
            pass
            # print("无法获取封面")

    # 下载图片
    def downImage(self,imgaeName="temp"):
        try:

            t = requests.get(self._imageUrl[0])
            # 图片路径
            self._imgPath += (imgaeName+".jpg")
            # print("路径:",self._imgPath)
            with open(self._imgPath, "wb") as f:
                f.write(t.content)
        except Exception as e:
            pass
            # print("[错误_封面获取001]",e)
            # print("封面下载失败!")

    # 简化以上3步
    def down(self, bv:str, p:int = 1,imgaeName="temp"):
        baseurl = "https://www.bilibili.com/video/BV" + str(bv) + "?p=" + str(p)
        html = self.getHtml(baseurl)
        self.getImageUrl(html)
        self.downImage(imgaeName=imgaeName)

if __name__ == '__main__':
    v = TitlePage()
    url = "https://www.bilibili.com/video/BV1oa4y1W7yx?p=2"
    v.down("1bt4y1e7qa")
    # html = v.getHtml(url)
    # v.getImageUrl(html)
    # v.downImage()