'''

    控件的样式类

'''

import os
import sys

# path = os.path.dirname(os.path.dirname(os.path.realpath(sys.executable)))
# 绝对路径
absolutePath = os.path.dirname(sys.argv[0])
# 样式类
class QSS:
    '''
        主页上的控件方法都以 [home] 打头

    '''
    def __init__(self):
        pass

    # 主页默认背景
    def homeBackDropDefault(self):
        return "QMainWindow{border-image:url(%s/image/home_Backdrop/home_back1.png);}"%absolutePath
    # 主页加载视频时的背景
    def homeBackDropIng(self):
        return "QMainWindow{border-image:url(%s/image/home_Backdrop/home_backing.png);}"%absolutePath

    # 主页关闭按钮
    def homeCloseButton(self):
        c = '''
        QPushButton{
            background-color: rgb(223, 104, 104);
            border-radius: 7px;
        }
        QPushButton:hover{
            background-color: rgb(223, 104, 104);
            border-radius: 7px;
            border-image:url(%s/image/home_close_btn/home_close_btn.png);
        }
        '''%absolutePath
        return c

    # 主页最小化按钮
    def homeMinButton(self):
        c = '''
                QPushButton{
                    background-color: #efe466;
                    border-radius: 7px;
                }
                QPushButton:hover{
                    background-color: #efe466;
                    border-radius: 7px;
                    border-image:url(%s/image/home_min_btn/homeminbtn.png);
                }
                '''%absolutePath
        return c


    # 主页下载视频位置按钮
    def homedownPos(self):
        c = '''
                QPushButton{
                    border:none;
                    border-image:url(%s/image/home_downPos/downPos.png);

                }
                '''%absolutePath
        return c

    def homeScrollAreaStyle(self):
        c = '''
        QScrollBar:vertical{
            border-radius:7px;
            background:#b0f0f2;
            width:8px;
        }
        QScrollBar::handle:vertical:hover{
            border-radius:1px;
            background:#85cae4;
            width:8px;
        }
        
        '''
        return c

    # 小视频关闭按钮
    def videoCloseButton(self):
        c = '''
        QPushButton{
            background-color: rgb(0, 0, 0);
            border:1px solid #fff;
            border-radius: 7px;
        }
        QPushButton:hover{
            background-color: rgb(255, 255, 255);
            border:2px solid red;
            border-radius: 7px;
            border-image:url(%s/image/home_close_btn/home_close_btn.png);
        }'''%absolutePath
        return c

    # 小视频设置按钮
    def videoSetingButton(self):
        c = '''
        QPushButton{
            border-image:url(%s/image/videoSeting/videoSeting2.png);
        }
        '''%absolutePath
        return c

    # 小视频开始按钮
    def videoStartButton(self):
        return "QPushButton{border-image:url(%s/image/videoPlayBtn/videoStartBtn.png);}"%absolutePath
    # 小视频暂停按钮
    def videoStopButton(self):
        return "QPushButton{border-image:url(%s/image/videoPlayBtn/videoStopBtn.png);}"%absolutePath

    # 小视频comboBox(下拉框)
    def videoComboBox(self):
        c = '''QComboBox {
        border:none;
        color:black;
        padding-left:30px;
        font-size:11px "SimHei";
        }  
        QComboBox QAbstractItemView {
        background:#fff;
        color:#ffffff;
        } 
        '''
        return c

if __name__ == '__main__':
    c=QSS()
    print(c.homeBackDropDefault())