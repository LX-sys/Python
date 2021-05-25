'''

    B站视频下载实现
'''

import requests
from pyquery import PyQuery as pq
import re
import json
import subprocess
import traceback
import tempfile
import os
from sys import path
import urllib3
import USER_AGENT
import time
from IPAgent import IPagent
# 消除 已经关闭认证（verify=False）情况下，控制台会输出以下错误
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# # print(os.getcwd())



class BliVideoDownlod:
    
    def __init__(self, user_agent="macOS"):
        '''

        :param user_agent: 根据当前系统使用不同的 用户代理
        '''
        # 视频标题
        self._videoTile = ""
        # 视频大小
        self._videSize = 0
        # 音频大小
        self._baseSize = 0
        # 总大小
        self._Szie = 0
        # 下载路径
        self._path = os.getcwd()
        # 音频视频路径
        self._bvPath = {"base": "", "video": ""}
        # 输出视频名称
        self._outVideName = ""
        # 视频音频合成后的路径
        self._outVidePath = ""
        # 视频大小换算成MB
        self._mb = 0
        # 百分比
        self._percentage = 0
        # 暂停
        self._stop = True
        # 关闭下载
        self._closeDown = False
        # 是否需要音频
        self._isBase = False

        # 根据当前系统使用不同的 用户代理
        self._user_agent = USER_AGENT.get_user_agent()
        # 代理ip池对象
        self._ip = IPagent()
        # # print("obj:",id(self))


    # 设置是否需要音频
    def setIsBase(self,b:bool=False):
        self._isBase = b

    # 音频视频融合
    def baseVideo(self,file_name="",mp3_file=""):
        """
             视频添加音频
            :param file_name: 传入视频文件的路径
            :param mp3_file: 传入音频文件的路径
            :return:
            """
        # 提取后缀
        # print("F:",file_name,"mp3:",mp3_file)
        outfile_name = "out_"+file_name.split('/')[-1]
        # # print("out:",outfile_name)
        # 输出视频名称
        self._outVideName = outfile_name
        self._outVideName = self._outVideName.replace(" ","")
        # self._outVideName = "test.flv"
        # 视频音频合成后的路径
        self._outVidePath = self._path + "/" +outfile_name

        cmd = 'ffmpeg -i ' + self._bvPath["video"] \
              + ' -i ' + self._bvPath["base"] + ' -acodec copy -vcodec copy ' \
              + self._outVidePath

        # 视频大，输出卡死问题未解决
        # subprocess.call(cmd, shell=True)

        # 最大 大小为视频大小的3倍
        # 自定义输出流的大小
        # max_size = self._Szie * 3
        max_size = 64 * 1024
        out_temp = tempfile.SpooledTemporaryFile(max_size=max_size)
        try:

            fileno = out_temp.fileno()
            obj = subprocess.Popen(cmd,stdout=fileno,stderr=fileno,shell=True,close_fds=True)
            # obj.wait()
            obj.communicate()
            out_temp.seek(0)
            # lines = out_temp.readlines()
            # # # print(lines)
        except Exception as e:
            # # print("e",e)
            pass
            # # # print(traceback.format_exc())
        finally:
            if out_temp:
                out_temp.close()


    def getVideoTile(self):
        '''
        视频标题
        :return:
        '''
        return self._videoTile
    def getVideoSize(self):
        '''
        视频大小(不含音频)
        :return:
        '''
        return self._videSize
    def getBaseSize(self):
        '''
        音频大小
        :return:
        '''
        return self._baseSize
    def setDownloadPath(self, path:str):
        '''
        设置下载路径
        :param path: 路径
        :return:
        '''
        self._path = path
    def DownloadPath(self):
        return self._path


    def getSize(self):
        '''
        视频大小(视频+音频) 字节数
        :return:
        '''
        return self._Szie
    def getMB(self):
        '''
        视频大小(视频+音频)  字节转换成MB 后结果保留两位
        :return:
        '''
        self._mb = self._Szie/(1024*1024)
        self._mb = round(self._mb, 2)   # 结果保留两位小数
        return self._mb

    def percentage(self):
        '''
            获取当前下载的百分比
        :return:
        '''
        return self._percentage

    def _getHtml(self,baseurl):
        head = {  # 模拟浏览器身份头向对方发送消息
            "user-agent": self._user_agent
        }
        http = self._ip.getIP()
        if http:
            proxies = {
                http["type"]: '{}:{}'.format(http["ip"], http["port"])
            }
        else:
            proxies={}
        try:
            response = requests.get(url=baseurl, headers=head)
            # 200表示服务器接受请求，会传回网页源代码，所以把文本内容传回来就行了
            if response.status_code == 200:
                return response.text
        except:
            pass
            # # print("请求失败")
    
    def _getVideo(self,baseurl,p):
        global audio_url
        html = self._getHtml(baseurl)
        # # print(html)
        doc = pq(html)		# pyquery库语法简洁些，所以先采用pyquery库
        title = doc('#viewbox_report > h1 > span').text()	# 设置普通视频标题获取规则
        # 获取番剧的标题
        if not title:
            title=doc(".media-wrapper > h1").text()
        # 获取小标题
        subTitle = re.findall('part\":\"(.*?)\",',html)
        if p != 1:
            title = subTitle[int(p) - 1]

        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'	# 设置类的获取规则
        # # print("y:",re.findall(pattern, html))
        try:
            result = re.findall(pattern, html)[0]
        except Exception:
            result = re.findall(r"readyVideoUrl: '(.*)',",html)[0]
            # # print("报错",result)


            # result = re.findall(pattern, html)[0]
        # # # print("yy:", result)
        temp = json.loads(result)
        # # # print("temp:",temp)
        # # # print(("开始下载--->")+title)
        # 去除视频名称的特殊符号,只保留汉字,字母,数字
        # 无法获取系统视频中的子标题名称(BUG)
        title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",title)
        self._videoTile = title
        # # print("标签:",self._videoTile)
        # title = str(p)
        try:
            video_url = temp['data']['dash']['video'][0]['baseUrl']
            # # print("vudlc:", video_url)
            audio_url = temp['data']['dash']['audio'][0]['baseUrl']
            headers = {
                "user-agent": self._user_agent
            }
            headers.update({'Referer': baseurl})
            http = self._ip.getIP()
            if http:
                proxies = {
                    http["type"]: '{}:{}'.format(http["ip"], http["port"])
                }
            else:
                proxies = dict()
            b = requests.get(url=audio_url, headers=headers, verify=False, timeout=(3, 7), proxies=proxies)
            # print("<>")
            v = requests.get(url=video_url, headers=headers, verify=False, timeout=(3, 7), proxies=proxies)
            # # print("<------>")
            self._videSize = len(v.content)   # 视频大小
            self._baseSize = len(b.content)   # 音频大小
            self._Szie = self._videSize + self._baseSize
            # # print("视频总大小:", self._Szie)

            self._fileDownload(homeurl=baseurl, url=video_url, title=self._videoTile, typ=0)
            # print("0")
            self._fileDownload(homeurl=baseurl, url=audio_url, title=self._videoTile, typ=1)
            # print("1")
        except Exception as e:
            # print("报错编号 002")
            # print(e)
            try:
                # 一秒后再次尝试
                time.sleep(1)
                self._fileDownload(homeurl=baseurl, url=audio_url, title=self._videoTile, typ=1)
                # print("111")
            except Exception:
                pass
            # # print("vudl:",video_url)
            # video_url = temp['data']['durl'][0]['url']
            # self._fileDownload(homeurl=baseurl, url=video_url, title=self._videoTile, typ=0)
            pass


    # 暂停/开始
    def setStop(self,b:bool=True):
        self._stop = b

    # 关闭下载
    def setCloseDown(self,down:bool=False):
        self._closeDown = down

    def _fileDownload(self,homeurl, url, title, typ):
        # print("typ:",typ)
        # 添加请求头键值对,写上 refered:请求来源
        headers = {
            "user-agent": self._user_agent
        }
        headers.update({'Referer': homeurl})
        if not title:
            title = "temp"
        if typ == 0:
            filename = self._path + "/" + title + ".flv"
            self._bvPath["video"] = filename
            # self._bvPath["base"] = self._path + "/" + title + ".mp3"
            # print("v:",filename)
        else:
            filename = self._path + "/" + title + ".mp3"
            self._bvPath["base"] = filename
            # print("b:",filename)
        requests_ = requests.Session()
        # 指定每次下载1M的数据
        begin = 0
        end = 1024 * 1024 - 1
        # # # print(end)
        flag = 0
        temp = 0
        btemp = 0
        while True:

            if self._closeDown:
                # # print("关闭下载")
                break
            if self._stop:
                # 添加请求头键值对,写上 range:请求字节范围
                headers.update({'Range': 'bytes=' + str(begin) + '-' + str(end)})
                http = self._ip.getIP()
                if http:
                    proxies = {
                        http["type"]: '{}:{}'.format(http["ip"], http["port"])
                    }
                else:
                    proxies=dict()
                # 获取视频分片
                res = requests_.get(url=url, headers=headers, verify=False,proxies=proxies)
                if not typ:
                    temp += len(res.content)
                else:
                    # 获取音频大小时，还要加上视频大小
                    btemp += len(res.content)
                    temp = btemp + self._videSize
                if res.status_code != 416:
                    # 响应码不为416时有数据，由于我们不是b站服务器，最终那个数据包的请求range肯定会超出限度，所以传回来的http状态码是416而不是206
                    begin = end + 1
                    end = end + (1024 * 1024)
                else:
                    headers.update({'Range': str(end + 1) + '-'})
                    res = requests_.get(url=url, headers=headers, verify=False,proxies=proxies)
                    flag = 1
                # 存文件
                with open(filename, 'ab') as fp:
                    fp.write(res.content)
                    fp.flush()
                    # # # print("下载:",round(temp/self._Szie, 2)*100)
                    self._percentage = round(temp/self._Szie, 2)*100

                if flag == 1:
                    fp.close()
                    break

    def main(self,bv:str,judge:bool=False,vNumber:int=1):
        '''

        :param bv: B站视频号 不加BV
        :param judge: [True]下载一个系统视频  [False]下载单一视频
        :param vNumber: 下载视频数量, 默认是1
        :return:
        '''
        # # print("B站视频下载器\n")
        if judge:
            for p in range(vNumber):
                baseurl = "https://www.bilibili.com/video/BV" + str(bv) + "?p=" + str(p)
                self._getVideo(baseurl, p)
        else:
            # p = input("如果是系列视频，请任选一集输入视频p号<------>如果不是系列视频，请输入'1'\n")
            baseurl = "https://www.bilibili.com/video/BV" + str(bv) + "?p=" + str(vNumber)
            self._getVideo(baseurl, vNumber)
        # # print("下载完毕")
        # # print("音频视频融合开始")
        self.baseVideo(file_name=self._bvPath["video"],mp3_file=self._bvPath["base"])
        # print("融合完成")
        # print("base:",self._bvPath)
        # 重命名输出视频
        # # print("self._outVidePath:", self._outVidePath)
        # # print("p_:", self._path + "/" + self._outVideName.split("out_")[-1])
        try:

            if not self._isBase:
                # 不需要音频
                # # print("c>",self._bvPath["base"])
                os.unlink(self._bvPath["base"])
            os.rename(self._outVidePath, self._path + "/" + self._outVideName.split("out_")[-1])
        except Exception as e:
            # 删除文件(正在使用会报错)
            os.unlink(self._bvPath["video"])
            # # print("ee:",e)
            return False
        # self.info()
        return True

    def info(self):
        pass
        # # print("视频标题:",self.getVideoTile())
        # # print("视频大小:",self.getVideoSize())
        # # print("音频大小:",self.getBaseSize())
        # # print("总大小:",self.getSize())
        # # print("下载路径:",self._path)
        # # print("音频视频路径:",self._bvPath)
        # # print("视频MB(总的):",self.getMB())
        

if __name__ == '__main__':
    v = BliVideoDownlod()
    # 1rV411y7UL   1Bt4y1q7ch  1e7411s79p  1Wa4y1J7tV
    v.main("1YD4y1d7h4")
    v.info()