import re
import os
from Keyword.Keyword import Keyword
from PErrorcolor.PErrorcolor import pec
# 管理命令类
class AdminCommand:
    def __init__(self):
        # 关键字列表
        self.Keyword_list = Keyword.KEYWORDS_LIST
         # 每个级别错误的默认颜色
        self.__color=Keyword.DEFAUKT_COLOR
        # 每个级别错误的默认字体大小
        self.__size=Keyword.DEFAUKT_SIZE
        # 历史语句(语法没有错误的语句)
        self.History=[]
        # help
        self.__help={"connect":'''
        connect语法:
            connect  文件路径;
            connect  文件路径1,文件路径2,..;
            connect  文件夹路径;
            connect  文件夹路径1,文件夹路径2,..;
            支持文件夹路径
                可同时对一个文件夹下所有文档进行配置
            如果连续使用 connect 进行连接,路径会追加
        ''',
                     "change":'''
        change语法:
            change 文件路径;
            change 文件夹路径;
            使用 change 路径不会追加，而会改变为当前的路径
        ''',
                     "set":'''
        set语法:
            配置
            set 级别;   # 级别 ["debug", "info", "warning", "error", "critical"]内置5种
            set change 级别;  # 更改级别配置
            set change;  # 恢复默认
            通过set配置过后,可以直接使用color;语法
            使用set change 级别这个语法和set 级别效果一样,大多数时候,都使用set 级别;
            但set change;一般用做恢复默认,不用来设置级别.
        ''',
                     "debug":'''
        debug语法:
            debug color [颜色];  # 颜色为可选项
            debug color;
            debug size 字体大小;
            颜色和颜色可以共存
            字体大小和字体大小可以共存
            但,颜色和字体大小无法共存
        ''',
                     "info":'''
        info语法:
            info color [颜色];  # 颜色为可选项
            info color;
            info size 字体大小;
            颜色和颜色可以共存
            字体大小和字体大小可以共存
            但,颜色和字体大小无法共存
        ''',
                     "warning":'''
        warning语法:
            warning color [颜色];  # 颜色为可选项
            warning color;
            warning size 字体大小;
            颜色和颜色可以共存
            字体大小和字体大小可以共存
            但,颜色和字体大小无法共存
        ''',
                     "error":'''
        error语法:
            error color [颜色];  # 颜色为可选项
            error color;
            error size 字体大小;
            颜色和颜色可以共存
            字体大小和字体大小可以共存
            但,颜色和字体大小无法共存
        ''',
                     "critical":'''
        critical语法:
            critical color [颜色];  # 颜色为可选项
            critical color;
            critical size 字体大小;
            颜色和颜色可以共存
            字体大小和字体大小可以共存
            但,颜色和字体大小无法共存
        ''',
                     "color":'''
        color语法:
            color;
            一般都是与set 级别;一起使用 # 级别 ["debug", "info", "warning", "error", "critical"]内置5种
        ''',
                     "config":'''
        config语法:
            config;  # 用于某些配置的激化,关闭(针对配置文件)
            config default; # 恢复默认配置文件
            如果执行了config; 之后没有效果,请先保存配置文件,在执行,如果还是没有效果,
            请重启软件
            config default; 不要随意执行此语句,可能会覆盖掉你自己的自定义配置
        ''',
                     "history":'''
        history语法:
            显示过去输入语法正确的指令
            history 数字;
            history;  # 不写数字,默认是10
        ''',
                     "out":'''
        out语法:
            out 错误级别 导出路径 导出格式;  # 导出格式为可选项
            out 错误级别 导出路径;  # 默认为md
            所导出新的文档名=原文档名_错误级别
            如果再次导出则生成的文档名=原文档名_错误级别_副本
            还导出,则覆盖副本
            注意: 现在仅支持导出 .md, .doc/.docx 后缀
        ''',
                     "show":'''
        show语法:
            show file;     # 显示当前所连接的文件 
            show config;  # 显示当前的基本配置信息
        ''',
                     "headinfo":'''
        headinfo语法:
            设置文档头信息
            headinfo name,自定义信息1,自定义信息2;  
            这一条命令 表示 在导出的新文档的开头是否生成时间,姓名信息,等其它信息
            需要通过config.ini进行设置
        ''',
                     "help":'''
        help语法:
            显示命令的帮助信息
            help all;  # 显示全部信息
            显示单个帮助信息
            help connect;
            help change;
            help set;
            help out;
            help headinfo;
            help show;
            help history;
            ...
        ''',
                     "exit":'''
        exit语法:
            exit;   # 退出程序
        '''}

    # 加入历史语句
    def appHis(self,sentence:str):
        self.History.append(sentence)
    # 显示厉害语句
    def showHistory(self,number=10):
        if not self.History:
            print("Empty")
            return False
        print("---最近历史---")
        if len(self.History) <=number:
            for sen in self.History:
                print(">>>",sen)
        else:
            # 输出最后number条
            for sen in self.History[len(self.History)-number:]:
                print(">>>",sen)
        print("--------------")

    # 重置颜色
    def ResetColorrSize(self):
        self.__color = Keyword.DEFAUKT_COLOR_
        self.__size = Keyword.DEFAUKT_SIZE_
                        
    # 语法判断
    def isSyntax(self, key: str):
        if key:
            try:
                # 分离出关键字
                keywork = key.split(" ")[0]
                if key[-1] == ";" and len(key.split(" "))==1:     # 针对像exit 这个关键字，只有一个的
                    keywork=self.removeEndSemicolon(key)
                    # 判断关键字是否存在, 是否以关键字开头,以分号结尾
                    if keywork in self.Keyword_list and re.findall(r"^"+keywork, key):
                        print("OK Perfect")
                        return True
                    else:
                        pec.addtext({"err": ["1007", "语法存在问题"]})
                elif keywork in self.Keyword_list and re.findall(r"^"+keywork, key) and key[-1] == ";":
                     # 判断关键字是否存在, 是否以关键字开头,以分号结尾
                        print("OK Perfect")
                        return True
                else:
                        pec.addtext({"err": ["1007", "语法存在问题"]})
            except Exception:
                print("语法存在问题[异常]")

            return False
    
    # 去除结尾分号
    def removeEndSemicolon(self,key:str):
        return key[:-1]
    
    # connect解析
    def connectAnalysis(self, key: str):
        # 去除关键字和结尾分号,只留中间,得到包含所有路径的字符串
        path_str = self.removeEndSemicolon(key).split(" ")[1]
        # 得到所有路径的列表
        paths_list = path_str.split(",")
        return paths_list

    # show解析
    def showAnalysis(self, key: str):
        if key == "show file;":
            return  "file"
        elif key == "show config;":
            return "config"

    #  change解析
    def  changeAnalysis(self, key:str):
        return self.connectAnalysis(key)

    # 错误级别解析
    def errorlevelAnalysis(self, key:str, what="color"):
        # 错误级别关键字
        keywork=key.split(" ")[0].lower()
        # 自定义颜色/大小
        if len(key.split(" "))>2:
            customColorSize=key.split(" ")[-1]   # 去除分号，获取颜色/大小
            if what=="color":
                for i in self.__color:
                    self.__color[i]=customColorSize
            elif what == "size":
                for i in self.__size:
                    self.__size[i]=customColorSize

        else:
                self.ResetColorrSize()   # 重置

        # 轻微错误 ,且对颜色设置
        if keywork.lower() == "debug" and what == "color":
            return self.__color["debug"]
        elif keywork.lower() == "info" and what == "color":
            return self.__color["info"]
        elif keywork.lower() == "warning" and what == "color":
            return self.__color["warning"]
        elif keywork.lower() == "error" and what == "color":
            return self.__color["error"]
        elif keywork.lower() not in self.__color and what == "color":  # 不在
            # 此时是自定义关键字
            self.__color[keywork.lower()]="#71C671"
            return self.__color[keywork.lower()]
        elif keywork.lower() in self.__color and what == "color":  # 在
            return self.__color[keywork.lower()]
        # 对字体大小进行设置
        elif keywork.lower() == "debug" and what == "size":
            return self.__size["debug"]
        elif keywork.lower() == "info" and what == "size":
            return self.__size["info"]
        elif keywork.lower() == "warning" and what == "size":
            return self.__size["warning"]
        elif keywork.lower() == "error" and what == "size":
            return self.__size["error"]
        elif keywork.lower() not in self.__color and what == "size":  # 不在
            # 此时是自定义关键字
            self.__color[keywork.lower()]="#71C671"
            return self.__color[keywork.lower()]
        elif keywork.lower() in self.__color and what == "size":  # 在
            return self.__color[keywork.lower()]
    # set解析
    def setAnalysis(self, key:str):
        try:
            key=self.removeEndSemicolon(key) # 去除结尾分号
            err=key.split(" ")[-1].lower()  # 去除错误级别
        except Exception:
            pec.addtext({"err": ["1008", '语法错误or级别不存在{}'.format(Keyword.ERRORLEVEL_LIST)]})
            return None
        if key.split(" ")[-1] == "change":   # key change; 这条命令相当于恢复默认
            self.__color=Keyword.DEFAUKT_COLOR_
        elif key.split(" ")[1] == "change":  # 切换级别配置
            errcolor=Keyword.DEFAUKT_COLOR_[err]
            for e in Keyword.DEFAUKT_COLOR_:
                self.__color[e]=errcolor
        elif key.split(" ")[-1] in Keyword.ERRORLEVEL_LIST:  # 设置级别
            errcolor=Keyword.DEFAUKT_COLOR_[err]
            for e in Keyword.DEFAUKT_COLOR_:
                self.__color[e]=errcolor
        else:
            pec.addtext({"err": ["1008", '语法错误or级别不存在{}'.format(Keyword.ERRORLEVEL_LIST)]})
            return None
        return self.__color
    
    # color解析
    def colorAnalysi(self, key:str):
        key=self.removeEndSemicolon(key) # 去除结尾分号
        if key.split(" ")[0]=="color":
            return True

    # out解析
    def outAnalysi(self,key:str):
        key = self.removeEndSemicolon(key)  # 去除结尾分号
        t=key.split(" ")
        if len(t) == 3:  # 没有导出格式
            if t[1] in Keyword.KEYWORDS_LIST: # 判断关键字
                if os.path.isdir(t[-1]):  # 判断是否为文件夹
                    return {"level":t[1],"path":t[-1],"format":"md"}
        elif len(t) == 4:  #  有导出格式(暂时不写)
            f=t[-1]
            if f in Keyword.FORMAT_LIST:
                if t[1] in Keyword.KEYWORDS_LIST:  # 判断关键字
                    if os.path.isdir(t[-2]):  # 判断是否为文件夹
                        return {"level":t[1], "path":t[-2], "format":f}
            else:
                pec.addtext({"err",["1012","不支持{}此格式导出,支持 {}".format(f,Keyword.FORMAT_LIST)]})

    # config解析
    def configAnalysi(self,key:str):
        key = self.removeEndSemicolon(key)
        if key == Keyword.CONFIG:
            return "config"
        elif key.split(" ")[-1] == "default":
            return "default"

    # headinfo解析
    def headinfoAnalysi(self,key:str):
        key = self.removeEndSemicolon(key)
        key_str = key.split(" ")[-1] # 去除关键字
        key_list = key_str.split(",")
        name="**"+"姓名/name: "+key_list[0]+"**"+"\n"
        # 其它信息
        it_info=""
        for info_index in range(1,len(key_list)):
            it_info+=key_list[info_index]+"\n"

        temp=name+it_info+"\n-----------------------------------\n"
        return temp

    def helpAnalysi(self,key:str):
        key = self.removeEndSemicolon(key)
        last = key.split(" ")[-1].lower()
        if last == "all":
            for info in self.__help.values():
                print(info)
        elif last in Keyword.KEYWORDS_LIST:
            print(self.__help[last])
        else:
            pec.addtext({"err": ["1008","语法有误,建议使用 help all或者help help;"]})

ac = AdminCommand()
