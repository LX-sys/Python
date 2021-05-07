from colorama import init
from termcolor import colored

init(autoreset=True)


# 打印错误(带颜色)
class PErrorcolor:
    def __init__(self):
        # 错误id
        self.__pe_id = []

    def addtext(self,text: dict):
        if type(text) == dict:
            self.__pe_id.append(text["err"][0]) # 存ID
            print(text["err"][0],":",colored(text=text["err"][1], color="red"))
        else:
            print("addtext()")

    # 错误写入文件
    def errorwrite(self):
        pass

pec = PErrorcolor()


