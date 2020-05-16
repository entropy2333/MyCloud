from UI.Ui_login import Ui_LoginWindow
import sys
import os
import qtawesome
root_path = os.getcwd()
sys.path.append(f'{root_path}\\qt')
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui, QtWidgets
from utils.VerificationCode import WidgetCode
from utils.FramelessDialog import *
from utils.FramelessWindow import FramelessWindow
ABSOLUTE_PATH = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
BACKGROUND_COLOR = '#F8F8FF'  # 主界面底色
TITLE_COLOR = '#F0E68C'  # 标题栏颜色
FUNC_COLOR = '#FFFFE0'  # 功能栏颜色
LIGHT_FUNC_COLOR = '#FFFFF0'  # 到功能栏颜色的过渡色
HOVER_COLOR = '#00BFFF'  # 按钮点击时的文字颜色
GRAY_COLOR = '#EEF0F6'  # 万能的灰色
GLOBAL_BUTTON = """
QPushButton{
    border:none;
    background:%s
}
QPushButton:hover{
    background:%s;
    border-radius:10px;
    color:%s;
}
#closeButton{
    background:%s;
    max-width: 36px;
    max-height: 36px;
    font-size: 12px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover{
    color: white;
    border:none;
    background: red;
}
#minButton{
    background:%s;
    max-width: 36px;
    max-height: 36px;
    font-family: "Webdings";
    font-size: 12px;
    qproperty-text: "0";
    border-radius: 10px;
}
#minButton:hover{
    color:black;
    border:none;
    background: %s;
}
""" % (FUNC_COLOR, GRAY_COLOR, HOVER_COLOR, TITLE_COLOR, TITLE_COLOR, BACKGROUND_COLOR)


class Login_window(QMainWindow, Ui_LoginWindow):
    def __init__(self, parent=None):
        super(Login_window, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏
        self.pushButton_4.setObjectName('closeButton')
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setObjectName('minButton')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # 密码输入不可见

        # widget美化
        Qss =  'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_2{background-color: %s;}' % TITLE_COLOR
        # 注册按钮
        Qss += 'QPushButton#pushButton_2{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        # 登陆按钮
        Qss += 'QPushButton#pushButton{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton:hover{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton:pressed{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss) # 边框部分qss重载

        self.pushButton.clicked.connect(self.btn_login)
        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.doClose)
        self.code = WidgetCode(self.widget_3, minimumHeight=35, minimumWidth=80)  # 添加验证码
        self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
        self.animation.setDuration(500)  # 持续时间0.5秒
        self.doShow()

    # 登陆按钮事件
    def btn_login(self):
        """登陆按钮事件
        """
        user_name = self.lineEdit.text()  # 获取用户输入的用户名
        password = self.lineEdit_2.text()  # 获取用户输入的密码
        code_check = self.code.check(self.lineEdit_3.text())  # 验证码验证
        if not code_check:
            self.main_window = Main_window()
            self.main_window.show()
            self.close()
        else:
            self.doShakeWindow(self)
            self.warn_dialog = Warn_Dialog()
            self.warn_dialog.label.setText('验证码错误！')
            self.warn_dialog.show()

    def btn_register(self):
        """注册按钮事件
        """
        self.register_window = Register_window()
        self.register_window.show()
        self.close()

    def doShakeWindow(self, target):
        """窗口抖动动画

        Arguments:
            target {窗口对象} -- 目标控件
        """
        if hasattr(target, '_shake_animation'):
            # 如果已经有该对象则跳过
            return

        animation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = animation
        animation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()

        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))
        animation.start(animation.DeleteWhenStopped)

    def doShow(self):
        """淡入
        """
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        """淡出
        """
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def mousePressEvent(self, event):
        """鼠标左键按下变小手

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
      
    def mouseReleaseEvent(self, event):
        """鼠标左键放开变回箭头

        Arguments:
            event -- 事件
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = False
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        """鼠标拖动窗口

        Arguments:
            event -- 事件
        """
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position) #更改窗口位置
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # login_window = Login_window()
    # login_window.show()
    w = FramelessWindow()
    # w.setWindowTitle('测试标题栏')
    # w.setWindowIcon(QIcon('Data/Qt.ico'))
    w.setWidget(Login_window(w))  # 把自己的窗口添加进来

    sys.exit(app.exec_())