# import sys
# import os
# __path="\\".join(os.getcwd().split("\\"))
# __path+="\\"+"run"+"\\"+"Keyword"
# print(__path)
# sys.path.append(__path)
# from Keyword import *
# # vscode下导入其它文件夹下的模块的方法
# print(Keyword.DEFAUKT_SIZE)
# print("=====================================")
# from AdminFilePath.AdminFilePath import adp
# from AdminCommand.AdminCommand import ac
# from AdminCommand.AdminCommand import adp

from AdminFilePath.AdminFilePath import adp
from AdminCommand.AdminCommand import ac
from Keyword.Keyword import Keyword

# 控制器类
class Controller:
    def __init__(self):
        # 关键字列表
        self.Keyword_list = Keyword.KEYWORDS_LIST
        # 关键字字典
        self.keywork_dict = Keyword.KEYWORDS_DICT
        self.adp = adp  # 管理文件路径类对象
        self.ac = ac     # 管理命令类对象

    def run(self):
        while True:
            print("ErrorConfigurator 3.0 version")
            t = input(">>>")
            if ac.isSyntax(t):
                # 加入历史语句
                self.ac.appHis(t)
                if len(t.split(" ")) == 1:
                    keywork=self.ac.removeEndSemicolon(t)
                else:
                    # 获取出关键字
                    keywork = t.split(" ")[0].lower()
                print(keywork)
                # 退出程序
                if keywork == Keyword.EXIT:
                    break
                elif keywork == Keyword.CONNECT:    # 文件链接
                    try:
                        self.adp.setpathAndfileName(self.ac.connectAnalysis(t))
                    except Exception as e:
                        print(e)
                        pass
                elif keywork == Keyword.SHOW:    # 显示当前连接的文件
                    # 判断文件路径是否连接
                    if self.adp.isPathNone():
                        continue
                    if self.ac.showAnalysis(t) == "file":
                        self.adp.getfileName()
                    elif self.ac.showAnalysis(t) == "config":
                        self.adp.getconfig()
                elif keywork == Keyword.CHANGE:    #  改变文件路径
                        self.adp.resetPath(self.ac.changeAnalysis(t))
                elif keywork in Keyword.ERRORLEVEL_LIST:     # 错误级别配置
                    # 判断文件路径是否连接
                    if self.adp.isPathNone():
                        continue
                    # 去除结尾分号
                    t=self.ac.removeEndSemicolon(t)
                    # 更新头信息
                    self.adp.up_headinfo()
                    if t.split(" ")[1].lower() in Keyword.ATTRIBUTE_LIST:
                        if len(t.split(" "))==2:   # 没有给出自定义颜色/大小
                            cs=self.ac.errorlevelAnalysis( t,t.split(" ")[-1].lower()) # 去除结尾分号转小写
                        else:
                            cs=self.ac.errorlevelAnalysis(t,t.split(" ")[1].lower())
                        self.adp.opens(errorKeyword=keywork, colorsize=t.split(" ")[1].lower(), cs=cs)
                elif keywork == Keyword.SET:  # 级别配置
                     # 判断文件路径是否连接
                    if self.adp.isPathNone():
                        continue
                    self.adp.setColor(self.ac.setAnalysis(t))
                elif keywork in Keyword.ATTRIBUTE_LIST:  # 级别设置后,快捷使用(size暂时不用)
                     # 判断文件路径是否连接
                    if self.adp.isPathNone():
                        continue
                    # 更新头信息
                    self.adp.up_headinfo()
                    # 首先取出两个判断是否执行过set
                    temp_color_dict=self.adp.getColor()
                    cs=temp_color_dict["info"]
                    if cs == temp_color_dict["error"]:
                        # 得到颜色对应的级别
                        colorlevel=self.adp.colorTotype(cs)
                        self.adp.opens(errorKeyword=colorlevel,colorsize=keywork,cs=cs)
                    else:
                        # C:\Users\刘璇\Desktop\ErrorConfigurator\aa.md
                        # ‪C:\Users\刘璇\Desktop\ErrorConfigurator\error1.md
                        # connect C:\Users\刘璇\Desktop\ErrorConfigurator\lx.docx
                        # out info C:\Users\刘璇\Desktop\ErrorConfigurator\run docx
                        # 没有执行过set,默认级别为info
                        # connect C:\Users\刘璇\Desktop\ErrorConfigurator\aa.md,‪C:\Users\刘璇\Desktop\ErrorConfigurator\error1.md;
                        self.adp.opens(errorKeyword="info",colorsize=keywork,cs=cs)
                elif keywork in Keyword.HISTORY:    # 显示历史
                    t=self.ac.removeEndSemicolon(t)  # 去除;
                    if len(t.split(" ")) == 1:
                        self.ac.showHistory()
                    elif len(t.split(" ")) == 2:
                        try:
                            number = int(t.split(" ")[-1])
                        except Exception:
                            print("请输入数字类型")
                            continue
                        self.ac.showHistory(number)
                elif keywork == Keyword.OUT:  # 导出错误文件
                    # 判断文件路径是否连接
                    if self.adp.isPathNone():
                        continue
                    # 更新头信息
                    self.adp.up_headinfo()
                    if self.ac.outAnalysi(t):
                        temp=self.ac.outAnalysi(t)
                        self.adp.out(level=temp["level"], path=temp["path"],format=temp["format"])
                elif keywork == Keyword.CONFIG: # 配置重启(针对配置文件)
                    if self.ac.configAnalysi(t) == Keyword.CONFIG:
                        self.adp.init_config()
                    elif self.ac.configAnalysi(t) == "default":  # 暂不实现
                        self.adp.config_default()
                elif keywork == Keyword.HEADINFO: # 头信息
                    # 判断文件路径是否连接
                    if self.adp.isPathNone():
                        continue
                    # 设置头部信息
                    self.adp.setheadinfo(self.ac.headinfoAnalysi(t))
                elif keywork == Keyword.HELP: # 帮助help
                    self.ac.helpAnalysi(t)