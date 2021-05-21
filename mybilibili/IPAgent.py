'''

    IP代理池
    当可用代理ip小于2个时,启动软件时会自行更新,
    只要源始网站还在,就不用管这个代码,全自动管理
    编写时间:2021 5 19
'''

import requests
import USER_AGENT
import telnetlib
import abc
import re
import time
import json
import random
import threading



# 检测ip是否可用
# def test_ip(ip,port):
#     try:
#         telnetlib.Telnet(ip,port,timeout=2)
#         # print("ip "+ip+":"+port+"            可用")
#     except:
#         # print("ip "+ip+":"+port+"            不可用")
# 
# 
# ip_list = [
#     "222.74.202.227:9999",
#     "61.135.185.152:80",
#     "118.25.187.125:8080",
#     "59.60.209.168:9999",
#     "209.97.153.244:8080"
# ]


# for ip_str in ip_list:
#     ip_arr = ip_str.split(":")
#     test_ip(ip_arr[0], ip_arr[1])
#     pass



# 随机获取请求头
headers = {
    'user-agent':USER_AGENT.get_user_agent()
}


# ip代理抽象类
class IPAgentABC(metaclass=abc.ABCMeta):

    # 获取ip的原始网站(ip代理网站)
    def sourceHtml(self,url:str):
        pass

    # 从本地读取IP池
    @abc.abstractmethod
    def readIPS(self,ip:list=None):
        pass

    # 将可用IP写入文件
    @abc.abstractmethod
    def writeIPs(self,ip:[list,dict]=None):
        '''
        :param ip: 参数=None,表示不传参数则调用类自己的
        :return:
        '''
        pass

    # 检测单个ip是否可用
    @abc.abstractmethod
    def isIP(self,ip:str,port:str):
        pass

    # 检测ip群是否可用
    @abc.abstractmethod
    def IPs(self, ips:dict=None):
        '''
        :param ips: 参数=None,表示不传参数则调用类自己的
        :return:
        '''
        pass

    # 检测源始网站是否可用
    @abc.abstractmethod
    def isSHtml(self):
        pass

    # ip总个数
    @abc.abstractmethod
    def getIpNumber(self):
        pass

    # 获取可用ip
    @abc.abstractmethod
    def getIP(self):
        pass

# ip代理类
class IPagent(IPAgentABC):


    def __init__(self):
        # 存放ip,端口,类型,响应时间
        self._ipList = []
        self._ipDict = dict()
        # 访问失败的网页集合
        self._accessFH = {}
        # 可用ip
        self._yesIPList = dict()
        # 当可用代理ip小于这个参数时自动更新
        self._ipMin = 0
        # 检测ip可用性时间间隔
        self._timeInterval = 0.1
        try:
            self.readIPS()
        except Exception:
            pass
            # print("还未创建ip.json")
        # 可用ip数量
        self._yesIPNumber = 4
        # 匹配ip结构的正则表达式
        self._ipMatch = {"ip":'IP">(.*)</td>',
                         "port":'"PORT">(.*)</td>',
                         "type":'"类型">(.*)</td>',    # http或者https
                         "time":'响应速度">(.*)秒</td>'}
        # 爬取ip的源网站,如果要替换该网站,需要将新的网站的页数部分换成%s
        self._url = "https://www.kuaidaili.com/free/inha/%s/"
        # 是否源网站爬取失败,那么isSHtml()将返回False
        self._isShtml = True

    @staticmethod
    def _sourceHtml(self, url: str = "https://www.kuaidaili.com/free/inha/%s/", pageStart=1, pageEnd=4):
        try:
            if "kuaidaili" in url:
                url = url % pageStart
            else:
                url = self._url % pageStart
            # print(url)
            r = requests.get(url=url, headers=headers)
            status_code = r.status_code
            if status_code != 200:
                self._accessFH.get(url)

            htmltext = r.text
            ip_list = re.findall(self._ipMatch["ip"], htmltext)
            port_list = re.findall(self._ipMatch["port"], htmltext)
            type_list = re.findall(self._ipMatch["type"], htmltext)
            time_list = re.findall(self._ipMatch["time"], htmltext)
            for i in range(len(ip_list)):
                combination = {
                    "ip": ip_list[i],
                    "port": port_list[i],
                    "type": type_list[i].lower(),
                    "time": time_list[i]
                }
                self._ipList.append(combination)
                self._ipDict[ip_list[i]] = combination

            # 终止递归条件
            if pageStart < pageEnd:
                # print("p:",pageStart)
                pageStart += 1
                time.sleep(0.5)
                self._sourceHtml(self=self,pageStart=pageStart)
        except Exception as e:
            # print("e:", e)
            self._isShtml = False
        # 失败的网页
        if self._accessFH:
            '''
                这里不要使用递归,防止死递归
            '''
            # print("失败后,再一次尝试访问")
            # print(self._accessFH)
            for url in self._accessFH:
                r = requests.get(url=url, headers=headers)
                htmltext = r.text
                ip_list = re.findall(self._ipMatch["ip"], htmltext)
                port_list = re.findall(self._ipMatch["port"], htmltext)
                type_list = re.findall(self._ipMatch["type"], htmltext)
                time_list = re.findall(self._ipMatch["time"], htmltext)
                for i in range(len(ip_list)):
                    combination = {
                        "ip": ip_list[i],
                        "port": port_list[i],
                        "type": type_list[i].lower(),
                        "time": time_list[i]
                    }
                    self._ipList.append(combination)
                    self._ipDict[ip_list[i]] = combination
                time.sleep(0.5)

        self.IPs()
        self.writeIPs()

    def sourceHtml(self,url:str="https://www.kuaidaili.com/free/inha/%s/",pageStart=50,pageEnd=53):
        # 这部分代码记录当前访问的页数,自行循环
        try:
            with open("numpage.json","r") as f:
                page_=json.load(f)
            if page_["e"] + 51 > 4000:
                page = {"s": 1, "e": 51}
                with open("numpage.json", "w") as f:
                    json.dump(page, f)
            else:
                page = {"s": page_["e"], "e": page_["e"]+20}
                with open("numpage.json", "w") as f:
                    json.dump(page, f)
        except Exception:
            page = {"s": pageStart, "e": pageEnd}
            if pageEnd +50 > 4000:
                page = {"s": 1, "e": 51}
            with open("numpage.json","w") as f:
                json.dump(page,f)

        pageStart,pageEnd = page_["s"],page_["e"]
        t = threading.Thread(target=self._sourceHtml,args=(self,url,pageStart,pageEnd))
        # print("线程开始")
        t.start()
        # t.join()
        # print("其他程序")
        # self._sourceHtml(self,url=url,pageStart=pageStart,pageEnd=pageEnd)

    @staticmethod
    def test(self):
        pass

    # 显示信息
    def info(self):
        pass
        # print(self._ipDict)
        # print(self.getIpNumber())


    def readIPS(self,ip:list=None):
        try:
            with open("ip.json", "r") as f:
                self._yesIPList = json.load(f)
        except Exception:
            # print("创建")
            with open("ip.json","w") as f:
                pass
        # 检测ip
        # # print("ppp->",self._yesIPList)
        self.IPs(self._yesIPList)
        # 可用代理ip小于2自动增加代理ip
        if self._yesIPNumber < self._ipMin:
            self.sourceHtml()

    def writeIPs(self,ip:[list,dict]=None):
        # # print("writeIPs->")
        if not ip:
            with open("ip.json", "r") as f:
                try:
                    tempdict = json.load(f)
                except Exception as e:
                    tempdict = {}
                    # print("e:",e)
            # if tempdict:
            # 字典合并
            self._yesIPList.update(tempdict)
            # # print("-------------")
        with open("ip.json", "w") as f:
            # print("ip.json")
            json.dump(self._yesIPList,f)
        # # print("<-writeIPs")


    def isIP(self,ip:str,port:str):
        try:
            telnetlib.Telnet(ip, port, timeout=self._timeInterval)
            return True
        except:
            return False

    def IPs(self, ips:dict=None):
        index = 0
        # 需要删除的ip
        delip = []
        # self._lock.acquire()
        if not ips: # 主动调用 sourceHtml()时执行
            for ip,port in self._ipDict.items():
                if self.isIP(ip,port["port"]):
                    combination={"ip":ip,
                                 "port":port["port"],
                                 "type":port["type"]}
                    self._yesIPList[ip]=combination
                # elif ips:
                #     delip.append(ips[ip])
                index+=1
            # print(index)
        else:
            for ip,port in ips.items():
                if not self.isIP(ip,port["port"]):
                    delip.append(ip)
        # self._lock.release()
        # 删除
        if ips:
            for k in ips.keys():
                if k in delip:
                    del self._yesIPList[k]
            # print("剩余:",len(self._yesIPList))

        self._yesIPNumber = len(self._yesIPList)
        if self._yesIPList:

            self.writeIPs(self._yesIPList)


    def getIpNumber(self):
        return len(self._ipList)
    def isSHtml(self):
        return self._isShtml

    def getIP(self):
        num = [ip for ip in self._yesIPList]
        # print("可用",len(num))
        if num:
            ip = random.choice(num)
            return {"ip":ip,
                    "port":self._yesIPList[ip]["port"],
                    "type":self._yesIPList[ip]["type"]
                    }
        else:
            return None

if __name__ == '__main__':
    # p = IPagent()
    # p.sourceHtml()
    # p.readIPS()
    # # print(p.getIP())

    pass