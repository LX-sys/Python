


#  关键字类
class Keyword:
    # 文件连接关键字
    CONNECT = "connect"
    # 切换文件连接关键字
    CHANGE = "change"
    # 级别配置关键字
    SET = "set"
    # 导出关键字
    OUT = "out"
    # 显示信息关键字
    SHOW = "show"
    # help关键字
    HELP = "help"
    # 退出关键字
    EXIT = "exit"
    # 颜色
    COLOR = "color"
    # 大小
    SIZE = "size"
    # 历史
    HISTORY = "history"
    # 属性列表
    ATTRIBUTE_LIST = ["color","size"]
    # 错误级别
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    # 配置重启(针对配置文件)
    CONFIG = "config"
    # 头信息
    HEADINFO = "headinfo"
    # 错误级别列表(可自定义扩展)
    ERRORLEVEL_LIST = [
            "debug", "info", "warning", "error", "critical"] 
    # 关键字列表
    KEYWORDS_LIST = ["connect", "change","set", "out", "show", "help", "exit",
                     "color","size","history","config","headinfo"]+ERRORLEVEL_LIST
    # 关键字字典
    KEYWORDS_DICT = {i:i for i in KEYWORDS_LIST}
    # 每个级别错误的默认颜色
    DEFAUKT_COLOR = {"debug":"#7D9EC0",
                    "info":"#698B22",
                    "warning":"#CDCD00",
                    "error":"#CD2626"}
    # 每个级别错误的默认颜色(备份)
    DEFAUKT_COLOR_={"debug":"#7D9EC0",
                            "info":"#698B22",
                            "warning":"#CDCD00",
                            "error":"#CD2626"}
    # 每个级别错误的默认字体大小
    DEFAUKT_SIZE={"debug":"4",
                            "info":"4",
                            "warning":"4",
                            "error":"4"}
    # 每个级别错误的默认字体大小(备份)
    DEFAUKT_SIZE_={"debug":"4",
                            "info":"4",
                            "warning":"4",
                            "error":"4"}
    # 支持导出的文件后缀列表
    FORMAT_LIST=["md","doc","docx"]
    # 二进制映射字典(用于#开头的颜色与RGB颜色的转换)
    BIN_DICT={"0":"0000",
              "1":"0001",
              "2":"0010",
              "3":"0011",
              "4":"0100",
              "5":"0101",
              "6":"0110",
              "7":"0111",
              "8":"1000",
              "9":"1001",
              "A":"1010",
              "B":"1011",
              "C":"1100",
              "D":"1101",
              "E":"1110",
              "F":"1111"}

