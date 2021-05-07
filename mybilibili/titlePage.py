'''

    B站视频 封面获取
'''

import requests
import re


# 获取B站视频封面类
class TitlePage:
    URL = str
    def __init__(self, user_agent="macOS"):

        self.imageUrl = ""
        self.path = ""
        self.imgPath = ""

        # 根据当前系统使用不同的 用户代理
        self._user_agent: str
        if user_agent == "macOS":
            self._user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"
        elif user_agent == "windows":
            self._user_agent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"

    # 获取网页文本
    def getHtml(self,baseurl)->str:
        head = {  # 模拟浏览器身份头向对方发送消息
            "user-agent": self._user_agent
        }
        try:
            response = requests.get(url=baseurl, headers=head)
            # 200表示服务器接受请求，会传回网页源代码，所以把文本内容传回来就行了
            if response.status_code == 200:
                # print(response.text)
                return response.text
        except:
            print("请求失败")

    # 获取图片链接
    def getImageUrl(self,htmlText:str):
        temp = re.findall("itemprop=\"image\" content=\"(http://i.*?.png)\">",htmlText)
        if temp:
            if len(temp[0]) < 80:
                self.imageUrl = temp
            else:
                self.imageUrl = re.findall("itemprop=\"image\" content=\"(http://i.*?.jpg)\">", htmlText)
        else:
            if len(temp[0]) < 80:
                self.imageUrl = re.findall("itemprop=\"image\" content=\"(http://i.*?.jpg)\">",htmlText)
            else:
                self.imageUrl = re.findall("itemprop=\"image\" content=\"(http://i.*?.png)\">",htmlText)
        print(self.imageUrl)

    # 下载图片
    def downImage(self,path:str="./",imgaeName="temp"):
        try:
            self.path = path
            t = requests.get(self.imageUrl[0])
            # 图片路径
            self.imgPath = path+imgaeName+".jpg"
            with open(self.imgPath, "wb") as f:
                f.write(t.content)
        except Exception as e:
            print("[错误_封面获取001]",e)
            print("下载失败!")

    # 简化以上3步
    def down(self, bv:str, p:int = 1, path:str = "./",imgaeName="temp"):
        self.path = path
        baseurl = "https://www.bilibili.com/video/BV" + str(bv) + "?p=" + str(p)
        html = self.getHtml(baseurl)
        self.getImageUrl(html)
        self.downImage(path=path,imgaeName=imgaeName)

if __name__ == '__main__':
    v = TitlePage()
    url = "https://www.bilibili.com/video/BV1oa4y1W7yx?p=2"
    v.down("1bt4y1e7qa")
    # html = v.getHtml(url)
    # v.getImageUrl(html)
    # v.downImage()