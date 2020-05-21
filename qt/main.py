from utils.FramelessDialog import *
from utils.VerificationCode import WidgetCode
from UI.Ui_transfer import Ui_TransferWindow
from UI.Ui_register import Ui_RegisterWindow
from UI.Ui_login import Ui_LoginWindow
from UI.Ui_main_window import Ui_MainWindow
from UI.Ui_rename_file import Ui_RenameWindow
from UI.Ui_share import Ui_ShareWindow
from UI.Ui_share_link import Ui_ShareLinkWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal
from client import *

import threading
import sys
import os
import qtawesome
root_path = os.getcwd()
sys.path.append(f'{root_path}\\qt')


FILE_ROOT_PATH = '../static/'  # 本地登陆的文件根目录
ABSOLUTE_PATH = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
SAVE_PATH = os.path.join('c:\\Users', (os.environ['USERNAME']))
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
    max-width:36px;
    max-height:36px;
    font-size:12px;
    font-family:"Webdings";
    qproperty-text:"r";
    border-radius:10px;
}
#closeButton:hover{
    color:white;
    border:none;
    background:red;
}
#minButton{
    background:%s;
    max-width:36px;
    max-height:36px;
    font-family:"Webdings";
    font-size: 12px;
    qproperty-text:"0";
    border-radius:10px;
}
#minButton:hover{
    color:black;
    border:none;
    background:%s;
}
QTableWidget{
    background:%s;
    border:none;
}
""" % (FUNC_COLOR, GRAY_COLOR, HOVER_COLOR, TITLE_COLOR, TITLE_COLOR, BACKGROUND_COLOR,  BACKGROUND_COLOR)

# 文件类型判断
img_list = ['bmp', 'jpeg', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx',
            'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'ai', 'raw', 'WMF', 'webp']
doc_list = ['txt', 'doc', 'xls', 'ppt', 'docx', 'xlsx', 'pptx', 'pdf']
music_list = ['mp3', 'cd', 'ogg', 'wma', 'mp3pro', 'ape',
              'flac', 'module', 'midi', 'vqf', 'dts', 'm4a', 'aac', 'ac3']
video_list = ['asf', 'wav', 'rm', 'mp4',
              'real', 'avi', 'mkv', 'webm', 'flv', 'mov']


# 经过基本美化的窗体(包括去标题栏，背景透明，淡入淡出，鼠标左键移动窗口，窗口阴影)
class BasicWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BasicWindow, self).__init__(parent)
        self.setupUi(self)
        self.m_flag = False  # 判断是否按下鼠标
        self.setFixedSize(self.width(), self.height())  # 设置窗口大小不能调整
        # self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 去掉窗口标题栏
        self.animation = QPropertyAnimation(self, b'windowOpacity')  # 窗口透明度动画类
        self.animation.setDuration(500)  # 持续时间0.5秒
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

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
            self.m_Position = event.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
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
            self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()


# 主窗口
class Main_window(BasicWindow, Ui_MainWindow):
    def __init__(self, user_name, parent=None):
        super(Main_window, self).__init__(parent)
        self.setupUi(self)
        self.user_name = user_name  # 当前登陆的用户的用户名
        self.is_open_tw = False  # 判断是否打开传输列表窗口
        self.is_file_found = False  # 判断是否找到对应文件

        self.left_column = {'allfile_btn': 0, 'doc_btn': 1, 'img_btn': 2,
                            'music_btn': 3, 'video_btn': 4, 'other_btn': 5}  # 左边栏
        self.file_button = {'删除': 'fa.trash', '重命名': 'fa.pencil-square',
                            '下载': 'fa.cloud-download', '分享': 'fa.share-alt-square'}  # 文件操作及对应图标
        self.logo.setPixmap(QPixmap(
            f'{ABSOLUTE_PATH}/img/logo.png').scaled(self.logo.width(), self.logo.height()))  # 添加logo
        self.label_3.setPixmap(QPixmap(
            f'{ABSOLUTE_PATH}/img/history.png').scaled(self.label_3.width(), self.label_3.height()))
        self.label_4.setPixmap(QPixmap(
            f'{ABSOLUTE_PATH}/img/exclamation.png').scaled(self.label_4.width(), self.label_4.height()))
        self.init_menu()    # 添加用户菜单
        self.doShow()   # 淡入
        self.init_ui()  # 初始化界面
        # index(self.username)
        # widget美化
        Qss = 'QWidget#widget{background-color:%s;}' % TITLE_COLOR
        Qss += 'QWidget#widget_2{background-color:%s;}' % GRAY_COLOR
        Qss += 'QWidget#widget_3{background-color:%s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_4{background-color:%s;}' % FUNC_COLOR
        Qss += 'QPushButton#user_btn{background-color:%s; border:none; border-radius:10px;}' % TITLE_COLOR
        Qss += '#upload_btn:hover{background-color:%s; border-radius:10px; border:1px solid %s;}' % (
            FUNC_COLOR, HOVER_COLOR)
        Qss += '#mkdir_btn:hover{background-color:%s; border-radius:10px; border:1px solid %s;}' % (
            FUNC_COLOR, HOVER_COLOR)
        Qss += '#transfer_btn:hover{background-color:%s; border-radius:10px; border:1px solid %s;}' % (
            FUNC_COLOR, HOVER_COLOR)
        for btn in self.left_column:
            Qss += '#%s{background-color:%s; border-radius:0;}' % (
                btn, GRAY_COLOR)
            Qss += '#%s:hover{background-color:%s; border-radius:0;}' % (
                btn, LIGHT_FUNC_COLOR)
            eval(f'self.{btn}').setCursor(
                QCursor(Qt.PointingHandCursor))  # 鼠标悬停按钮上时变小手
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss)  # 边框部分qss重载

        # 所有按钮的初始化
        self.minButton.clicked.connect(self.showMinimized)
        self.minButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeButton.clicked.connect(self.doClose)
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.user_btn.setText(f'{self.user_name}')   # 用户名按钮
        self.user_btn.setGeometry(QtCore.QRect(970, 10, 100, 31))
        self.user_btn.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/user.png'))
        self.user_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_btn.setIcon(qtawesome.icon('fa.cloud-upload'))  # 上传按钮
        self.upload_btn.setGeometry(QtCore.QRect(190, 8, 91, 37))
        self.upload_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_btn.clicked.connect(self.btn_upload)
        self.uploadselect = QtWidgets.QFileDialog()         # 上传文件选择界面
        self.uploadselect.setGeometry(QtCore.QRect(248, 341, 500, 62))
        self.mkdir_btn.setIcon(qtawesome.icon('fa.plus-square'))  # 新建文件夹按钮
        self.mkdir_btn.setGeometry(QtCore.QRect(290, 8, 141, 37))
        self.mkdir_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mkdir_btn.clicked.connect(self.btn_mkdir)
        self.back_btn.setIcon(qtawesome.icon('fa.chevron-left'))  # 回退按钮
        self.back_btn.setToolTip('回退')
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_btn.clicked.connect(self.btn_back)
        self.forward_btn.setIcon(qtawesome.icon('fa.chevron-right'))  # 前进按钮
        self.forward_btn.setToolTip('前进')
        self.forward_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.forward_btn.clicked.connect(self.btn_forward)
        self.refresh_btn.setIcon(qtawesome.icon('fa.refresh'))  # 刷新按钮
        self.refresh_btn.setToolTip('刷新')
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.btn_refresh)
        self.lineEdit.setPlaceholderText('搜索网盘文件')
        self.search_btn.setIcon(qtawesome.icon('fa.search'))  # 搜索按钮
        self.search_btn.setToolTip('搜索')
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.clicked.connect(self.btn_search)
        self.transfer_btn.setIcon(qtawesome.icon('fa.exchange'))  # 传输列表按钮
        self.transfer_btn.setGeometry(QtCore.QRect(480, 8, 111, 37))
        self.transfer_btn.clicked.connect(self.btn_transfer)
        self.allfile_btn.setIcon(
            QIcon(f'{ABSOLUTE_PATH}/img/file_icon/folder.png'))  # 全部文件按钮
        self.allfile_btn.clicked.connect(lambda: self.btn_left('allfile_btn'))
        self.doc_btn.setIcon(
            QIcon(f'{ABSOLUTE_PATH}/img/file_icon/word.png'))  # 文档按钮
        self.doc_btn.clicked.connect(lambda: self.btn_left('doc_btn'))
        self.music_btn.setIcon(
            QIcon(f'{ABSOLUTE_PATH}/img/file_icon/music.png'))  # 音乐按钮
        self.music_btn.clicked.connect(lambda: self.btn_left('music_btn'))
        self.video_btn.setIcon(
            QIcon(f'{ABSOLUTE_PATH}/img/file_icon/video.png'))  # 视频按钮
        self.video_btn.clicked.connect(lambda: self.btn_left('video_btn'))
        self.other_btn.setIcon(
            QIcon(f'{ABSOLUTE_PATH}/img/file_icon/unknown.png'))  # 其他按钮
        self.other_btn.clicked.connect(lambda: self.btn_left('other_btn'))
        self.img_btn.setIcon(
            QIcon(f'{ABSOLUTE_PATH}/img/file_icon/img.png'))  # 图片按钮
        self.img_btn.clicked.connect(lambda: self.btn_left('img_btn'))

    def init_menu(self):
        """用户菜单栏初始化
        """
        self.menu = QMenu(self.user_btn)
        self.menu.addAction('注销', self.logout)
        self.user_btn.setMenu(self.menu)

    def init_ui(self):
        """初始化界面
        """
        self.is_file_exist = {'allfile_btn': False, 'doc_btn': False, 'img_btn': False,
                              'music_btn': False, 'video_btn': False, 'other_btn': False}  # 判断各类型文件是否存在
        self.allfile_btn.setStyleSheet(
            '#allfile_btn{background-color:%s; color:%s; border-left:6px solid %s}' % (FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))
        for btn in self.left_column:  # 其他按钮全部恢复
            if btn != 'allfile_btn':
                eval(f'self.{btn}').setStyleSheet(
                    '#%s{background-color:%s; border-radius:0;}' % (btn, GRAY_COLOR))
        self.all_file = client.fetch_all_file()
        file_list = self.all_file['file_list']
        folder_list = self.all_file['folder_list']
        # print(self.all_file)
        # 所有文件页面初始化
        if file_list or folder_list:
            self.is_file_exist['allfile_btn'] = True
        if self.is_file_exist['allfile_btn']:
            self.stackedWidget.setCurrentIndex(0)
            self.file_table('allfile', self.all_file)
        else:
            self.stackedWidget.setCurrentIndex(6)
        # 各类文件字典生成
        doc_files = {'file_list': [], 'folder_list': []}
        img_files = {'file_list': [], 'folder_list': []}
        music_files = {'file_list': [], 'folder_list': []}
        video_files = {'file_list': [], 'folder_list': []}
        other_files = {'file_list': [], 'folder_list': []}
        for i, file_ in enumerate(file_list):
            mime = file_['file_name'].split('.')[-1]
            if mime in doc_list:
                self.is_file_exist['doc_btn'] = True
                doc_files['file_list'].append(file_)
            elif mime in img_list:
                self.is_file_exist['img_btn'] = True
                img_files['file_list'].append(file_)
            elif mime in music_list:
                self.is_file_exist['music_btn'] = True
                music_files['file_list'].append(file_)
            elif mime in video_list:
                self.is_file_exist['video_btn'] = True
                video_files['file_list'].append(file_)
            else:
                self.is_file_exist['other_btn'] = True
                other_files['file_list'].append(file_)
        # 各类文件页面初始化
        self.file_table('doc', doc_files)
        self.file_table('img', img_files)
        self.file_table('music', music_files)
        self.file_table('video', video_files)
        self.file_table('other', other_files)

    def file_table(self, file_type, file_dict):
        """文件表初始化

        Arguments:
            file_type {str} -- 文件类型
            file_dict {dict} -- 所有文件的字典
        """
        folder_num = len(file_dict['folder_list'])
        folder_list = file_dict['folder_list']
        file_num = len(file_dict['file_list'])
        file_list = file_dict['file_list']
        eval(f'self.{file_type}_table').setColumnCount(7)
        eval(f'self.{file_type}_table').setRowCount(folder_num + file_num)
        eval(f'self.{file_type}_table').setHorizontalHeaderLabels(
            ['文件', '大小', '修改时间', '', '', '', ''])
        # 设置表格每项大小
        eval(f'self.{file_type}_table').setColumnWidth(0, 429)
        eval(f'self.{file_type}_table').setColumnWidth(1, 120)
        eval(f'self.{file_type}_table').setColumnWidth(2, 180)
        eval(f'self.{file_type}_table').setColumnWidth(3, 50)
        eval(f'self.{file_type}_table').setColumnWidth(4, 50)
        eval(f'self.{file_type}_table').setColumnWidth(5, 50)
        eval(f'self.{file_type}_table').setColumnWidth(6, 50)
        eval(f'self.{file_type}_table').setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # 表格禁止编辑
        eval(f'self.{file_type}_table').verticalHeader(
        ).setVisible(False)  # 隐藏水平头标签
        eval(f'self.{file_type}_table').setSelectionBehavior(
            QAbstractItemView.SelectRows)  # 设置为整行选中
        eval(f'self.{file_type}_table').setSelectionMode(
            QAbstractItemView.NoSelection)
        eval(f'self.{file_type}_table').setShowGrid(False)  # 不显示网格

        for i, folder_ in enumerate(folder_list):
            new = QPushButton(self.stackedWidget)
            objname = f"{folder_['belong_folder']}%^{folder_['folder_name']}"  # 按钮名称设置
            new.setObjectName(objname)
            new.setStyleSheet("""
                QPushButton{
                    background-color:%s;
                    text-align:left
                }
                QPushButton:hover{
                    color:%s;
                }
                """ % (BACKGROUND_COLOR, HOVER_COLOR))
            new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/folder.png'))
            new.setText(folder_['folder_name'])
            new.clicked.connect(
                lambda: self.open_folder(self.sender()))  # 打开文件夹
            eval(f'self.{file_type}_table').setCellWidget(i, 0, new)
            new = QTableWidgetItem(folder_['update_time'].replace('T', ' '))
            eval(f'self.{file_type}_table').setItem(i, 2, new)
            # 操作部分
            for j, btn_name in enumerate(['重命名', '删除']):
                new = QPushButton(self.stackedWidget)
                objname = btn_name + '%^' + folder_['folder_name']  # 按钮名称设置
                new.setObjectName(f'{objname}')
                new.setStyleSheet("""
                    QPushButton{
                        background-color:%s;
                    }
                    QPushButton:hover{
                        color:%s;
                    }
                    """ % (BACKGROUND_COLOR, HOVER_COLOR))
                new.setCursor(QCursor(Qt.PointingHandCursor))
                new.setIcon(qtawesome.icon(self.file_button[btn_name]))
                new.setToolTip(btn_name)
                new.clicked.connect(
                    lambda: self.file_operation(self.sender()))  # 文件夹操作
                eval(f'self.{file_type}_table').setCellWidget(i, j+4, new)

        for i, file_ in enumerate(file_list):
            new = QPushButton(self.stackedWidget)
            objname = f"{file_['file_path']}"  # 按钮名称设置
            new.setObjectName(objname)
            new.setStyleSheet("""
                QPushButton{
                    background-color:%s;
                    text-align:left
                }
                QPushButton:hover{
                    color:%s;
                }
                """ % (BACKGROUND_COLOR, HOVER_COLOR))
            mime = file_['file_name'].split('.')[-1]
            if mime in ['doc', 'docx']:
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/word.png'))
            elif mime == 'txt':
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/txt.png'))
            elif mime in ['ppt', 'pptx']:
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/ppt.png'))
            elif mime in ['xls', 'xlsx']:
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/xls.png'))
            elif mime == 'pdf':
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/pdf.png'))
            elif mime in img_list:
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/img.png'))
            elif mime in music_list:
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/music.png'))
            elif mime in video_list:
                new.setIcon(QIcon(f'{ABSOLUTE_PATH}/img/file_icon/video.png'))
            else:
                new.setIcon(
                    QIcon(f'{ABSOLUTE_PATH}/img/file_icon/unknown.png'))
            new.setText(file_['file_name'])
            new.clicked.connect(
                lambda: self.file_preview(self.sender()))  # 文件预览
            eval(f'self.{file_type}_table').setCellWidget(i+folder_num, 0, new)
            new = QTableWidgetItem(file_['file_size'])
            eval(f'self.{file_type}_table').setItem(i+folder_num, 1, new)
            new = QTableWidgetItem(file_['update_time'].replace('T', ' '))
            eval(f'self.{file_type}_table').setItem(i+folder_num, 2, new)
            # 操作部分
            for j, btn_name in enumerate(['下载', '重命名', '分享', '删除']):
                new = QPushButton(self.stackedWidget)
                objname = btn_name + '%^' + file_['file_path']
                new.setObjectName(objname)  # 文件操作按钮名称
                new.setStyleSheet("""
                    QPushButton{
                        background-color:%s;
                    }
                    QPushButton:hover{
                        color:%s;
                    }
                    """ % (BACKGROUND_COLOR, HOVER_COLOR))
                new.setCursor(QCursor(Qt.PointingHandCursor))
                new.setIcon(qtawesome.icon(self.file_button[btn_name]))
                new.setToolTip(btn_name)
                new.clicked.connect(
                    lambda: self.file_operation(self.sender()))  # 文件操作
                eval(f'self.{file_type}_table').setCellWidget(
                    i+folder_num, j+3, new)

    def open_folder(self, btn):
        """打开文件夹界面

        Arguments:
            btn {QPushButton} -- 打开文件夹的按钮
        """
        belong_folder = btn.objectName().split('%^')[0]
        folder_name = btn.objectName().split('%^')[1]
        print(f'父目录: {belong_folder} 文件夹名: {folder_name}')

    def file_preview(self, btn):
        """预览文件

        Arguments:
            btn {QPushButton} -- 预览文件的按钮
        """
        print(f'预览文件: {btn.objectName()}')

    def file_operation(self, btn):
        """文件操作

        Arguments:
            btn {QPushButton} -- 操作文件的按钮
        """
        operation = btn.objectName().split('%^')[0]
        file_path = btn.objectName().split('%^')[1]
        if operation == '下载':
            func = threading.Thread(target=client.download,
                                    args=(file_path, SAVE_PATH,))
            func.setDaemon(True)
            func.start()
        if operation == '删除':
            self.delete_thread = newThread(
                mode='delete', args=(self.user_name, file_path,))
            self.delete_thread.start()
            self.delete_thread.trigger.connect(self.init_ui)
        elif operation == '重命名':
            self.rename_window = Rename_window(
                file_path=file_path, user_name=self.user_name)
            self.rename_window.show()
            self.upload_thread = newThread(mode='refresh')
            self.upload_thread.start()
            self.upload_thread.trigger.connect(self.init_ui)

        elif operation == '分享':
            self.share_window = Share_window(file_path)
            self.share_window.show()

        print(f'{operation}: {file_path}')

    def btn_left(self, left_btn):
        """左边栏按钮对应事件
        """
        # index(self.username)
        eval(f'self.{left_btn}').setStyleSheet('#%s{background-color:%s; color:%s; border-left:6px solid %s}' %
                                               (left_btn, FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))  # 当前点击按钮高亮
        # print(left_btn)
        if self.is_file_exist[f'{left_btn}']:
            self.stackedWidget.setCurrentIndex(
                self.left_column[left_btn])  # 切换当前页面
        else:
            self.stackedWidget.setCurrentIndex(6)
        for btn in self.left_column:  # 其他按钮全部恢复
            if btn != left_btn:
                eval(f'self.{btn}').setStyleSheet(
                    '#%s{background-color:%s; border-radius:0;}' % (btn, GRAY_COLOR))

    def btn_transfer(self):
        """传输列表界面
        """
        def confirm_close(parameter):
            self.is_open_tw = parameter
        if not self.is_open_tw:
            self.transfer_window = Transfer_window()
            self.is_open_tw = True
            self.transfer_window.show()
        else:
            self.warn_dialog = Warn_Dialog()
            self.warn_dialog.label.setText('请勿同时打开多个传输列表！')
            self.warn_dialog.show()

    def btn_upload(self):
        """文件上传
        """

        self.upload_flag = False
        fileinfo = self.uploadselect.getOpenFileName(
            self, 'OpenFile', "c:/")
        if os.path.exists(fileinfo[0]):
            # func = MyThread(target=client.upload, args=(
            #     self.user_name, fileinfo[0],))
            # func.run()
            self.refresh_thread = newThread(mode='upload', args=(
                self.user_name, fileinfo[0],))
            self.refresh_thread.start()
            self.refresh_thread.trigger.connect(self.init_ui)
            # func.start()

    def btn_mkdir(self):
        """新建文件夹
        """
        print("新建文件夹")

    def btn_back(self):
        """回退
        """
        print("回退")

    def btn_forward(self):
        """前进
        """
        print("前进")

    def btn_refresh(self):
        """刷新
        """
        self.init_ui()
        print("刷新")

    def btn_search(self):
        """搜索网盘文件
        """
        file_search = self.lineEdit.text()
        print(f'搜索: {file_search}')
        # 搜索到文件
        if self.is_file_found:
            pass
        else:
            self.stackedWidget.setCurrentIndex(7)

    def logout(self):
        """注销账户
        """
        self.login_window = Login_window()
        self.login_window.show()
        self.doClose()


class newThread(QThread):
    '''线程类'''
    trigger = pyqtSignal(str)

    def __init__(self, mode, args=()):
        QThread.__init__(self)
        self.mode = mode
        self.args = args

    def run(self):
        if self.mode == 'refresh':
            while True:
                try:
                    if login_window.main_window.rename_window.rename_flag:
                        self.trigger.emit(str(1))
                        login_window.main_window.rename_window.rename_flag = False
                        break
                except:
                    continue
        elif self.mode == 'upload':
            flag = client.upload(username=self.args[0], filepath=self.args[1])
            if flag:
                self.trigger.emit(str(1))
        elif self.mode == 'delete':
            flag = client.delete(username=self.args[0], filepath=self.args[1])
            if flag:
                self.trigger.emit(str(1))


# 文件重命名窗口
class Rename_window(BasicWindow, Ui_RenameWindow):
    def __init__(self, user_name, file_path, parent=None):
        super(Rename_window, self).__init__(parent)
        self.setupUi(self)
        # print(file_path)
        self.user_name = user_name
        self.file_path = file_path
        self.rename_flag = False
        name = file_path.split('/')[-1].split('.')[0]
        try:
            self.mime = '.' + file_path.rsplit('.', 1)[1]
        except:  # 文件夹无后缀
            self.mime = ''
            self.folder = ''
        self.lineEdit.setText(name)
        self.label_2.setText(self.mime)
        self.label.setStyleSheet(
            'QLabel{background-color:%s; border-radius:6px}' % FUNC_COLOR)
        self.label_2.setStyleSheet(
            'QLabel{background-color:%s; border-radius:6px}' % FUNC_COLOR)
        self.pushButton_2.clicked.connect(self.btn_rename)
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeButton.clicked.connect(self.doClose)
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.minButton.clicked.connect(self.showMinimized)
        self.minButton.setCursor(QCursor(Qt.PointingHandCursor))

        # widget美化
        Qss = 'QWidget#widget{background-color:%s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_3{background-color:%s;}' % TITLE_COLOR
        # 重命名按钮
        Qss += 'QPushButton#pushButton_2{background-color:%s; border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color:%s; border-radius:5px; color:black}' % FUNC_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color:%s; border-radius:5px;}' % LIGHT_FUNC_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss)  # 边框部分qss重载

    def btn_rename(self):
        """重命名
        """
        file_path = self.file_path
        new_file_name = self.lineEdit.text()
        self.rename_flag = client.rename(username=self.user_name,
                                         filepath=self.file_path, newfilename=new_file_name)
        print(f'重命名完成： {new_file_name}')


# 文件分享窗口
class Share_window(BasicWindow, Ui_ShareWindow):
    def __init__(self, file_path, parent=None):
        super(Share_window, self).__init__(parent)
        self.setupUi(self)
        # print(file_path)
        self.file_path = file_path  # 文件路径
        self.file_name = file_path.split('/')[-1]  # 文件名
        self.label_5.setText(self.file_name)
        self.closeButton.clicked.connect(self.doClose)
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.minButton.clicked.connect(self.showMinimized)
        self.minButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.clicked.connect(self.btn_share)
        self.radioButton_2.setChecked(True)

        # widget美化
        Qss = 'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_3{background-color: %s;}' % TITLE_COLOR
        Qss += 'QWidget#widget_2{background-color: %s;}' % FUNC_COLOR
        # 生成分享链接按钮
        Qss += 'QPushButton#pushButton_2{background-color: %s; border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color:%s; border-radius:5px; color:black}' % FUNC_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color: %s; border-radius:5px;}' % LIGHT_FUNC_COLOR
        Qss += 'QLabel{background-color:%s;}' % FUNC_COLOR
        Qss += '#label_5{background-color:%s; border-radius:0}' % GRAY_COLOR
        Qss += '#label_6{background-color:%s; border-radius:0}' % GRAY_COLOR
        Qss += '#label_7{background-color:%s; border-radius:0}' % TITLE_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss)  # 边框部分qss重载

    def btn_share(self):
        """生成分享链接
        """
        password = self.lineEdit.text()
        if not password:
            self.warn_dialog = Warn_Dialog()
            self.warn_dialog.label.setText('请输入分享密码！')
            self.warn_dialog.show()
            return
        if self.radioButton_2.isChecked():
            share_time = '7天'
        elif self.radioButton_3.isChecked():
            share_time = '30天'
        elif self.radioButton_4.isChecked():
            share_time = '无期限'
        self.share_link_window = Share_link_window(
            self.file_path, password, share_time)
        self.share_link_window.show()
        self.doClose()


# 分享链接窗口
class Share_link_window(BasicWindow, Ui_ShareLinkWindow):
    def __init__(self, file_path, password, share_time, parent=None):
        super(Share_link_window, self).__init__(parent)
        self.setupUi(self)
        # print(file_path)
        self.file_path = file_path  # 文件路径
        self.file_name = file_path.split('/')[-1]  # 文件名
        self.pwd_label.setText(password)
        self.pwd_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse)  # 设置标签可复制
        self.link_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.closeButton.clicked.connect(self.doClose)
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.minButton.clicked.connect(self.showMinimized)
        self.minButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.clicked.connect(self.btn_copy)

        # widget美化
        Qss = 'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_3{background-color: %s;}' % TITLE_COLOR
        Qss += 'QWidget#widget_2{background-color: %s;}' % FUNC_COLOR
        # 复制分享链接按钮
        Qss += 'QPushButton#pushButton_2{background-color: %s; border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color:%s; border-radius:5px; color:black}' % FUNC_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color: %s; border-radius:5px;}' % LIGHT_FUNC_COLOR
        Qss += 'QLabel{background-color:%s;}' % FUNC_COLOR
        Qss += '#link_label{background-color:%s; border-radius:0}' % GRAY_COLOR
        Qss += '#pwd_label{background-color:%s; border-radius:0}' % GRAY_COLOR
        Qss += '#qr_label{background-color:%s; border-radius:0}' % GRAY_COLOR
        Qss += '#label_7{background-color:%s; border-radius:0}' % TITLE_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss)  # 边框部分qss重载

    def btn_copy(self):
        """复制分享链接
        """
        print(self.link_label.text())


# 登陆窗口
class Login_window(BasicWindow, Ui_LoginWindow):
    def __init__(self, parent=None):
        super(Login_window, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_4.setObjectName('closeButton')
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setObjectName('minButton')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # 密码输入不可见

        # widget美化
        Qss = 'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_2{background-color: %s;}' % TITLE_COLOR
        # 注册按钮
        Qss += 'QPushButton#pushButton_2{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color: %s;border-radius:5px; color:black}' % FUNC_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color: %s;border-radius:5px;}' % LIGHT_FUNC_COLOR
        # 登陆按钮
        Qss += 'QPushButton#pushButton{background-color: %s;border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton:hover{background-color: %s;border-radius:5px; color:black}' % FUNC_COLOR
        Qss += 'QPushButton#pushButton:pressed{background-color: %s;border-radius:5px;}' % LIGHT_FUNC_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss)  # 边框部分qss重载

        self.pushButton.clicked.connect(self.btn_login)
        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.doClose)
        self.code = WidgetCode(
            self.widget_3, minimumHeight=35, minimumWidth=80)  # 添加验证码
        self.doShow()

    # 登陆按钮事件
    def btn_login(self):
        """登陆按钮事件
        """
        user_name = self.lineEdit.text()  # 获取用户输入的用户名
        password = self.lineEdit_2.text()  # 获取用户输入的密码
        code_check = self.code.check(self.lineEdit_3.text())  # 验证码验证
        if not code_check:
            if client.user_login(user_name, password):
                self.main_window = Main_window(user_name)
                self.main_window.show()
                self.close()
            else:
                self.doShakeWindow(self)
                self.warn_dialog = Warn_Dialog()
                self.warn_dialog.label.setText('用户名或密码错误！')
                self.warn_dialog.show()
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


# 注册窗口
class Register_window(BasicWindow, Ui_RegisterWindow):
    def __init__(self, parent=None):
        super(Register_window, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_4.setObjectName('closeButton')
        self.pushButton_3.setObjectName('minButton')
        self.lineEdit_2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_3.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        # widget美化
        Qss = 'QWidget#widget{background-color: %s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_3{background-color: %s;}' % TITLE_COLOR
        # 注册按钮
        Qss += 'QPushButton#pushButton_2{background-color:%s; border-radius:5px;}' % TITLE_COLOR
        Qss += 'QPushButton#pushButton_2:hover{background-color:%s; border-radius:5px; color:black}' % FUNC_COLOR
        Qss += 'QPushButton#pushButton_2:pressed{background-color:%s; border-radius:5px;}' % LIGHT_FUNC_COLOR
        Qss += GLOBAL_BUTTON
        self.setStyleSheet(Qss)  # 边框部分qss重载

        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.showMinimized)
        self.pushButton_4.clicked.connect(self.doClose)
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.doShow()

    def btn_register(self):
        """注册按钮事件
        """
        user_name = self.lineEdit.text()  # 获取用户输入的用户名
        password = self.lineEdit_2.text()  # 获取用户输入的密码
        repassword = self.lineEdit_3.text()  # 获取用户重复输入的密码
        if client.user_register(user_name, password, repassword):
            self.login_window = Login_window()
            self.login_window.show()
            self.close()


# 传输列表界面
class Transfer_window(BasicWindow, Ui_TransferWindow):
    signal = QtCore.pyqtSignal(bool)  # 传递是否有窗口打开的布尔值

    def __init__(self, parent=None):
        super(Transfer_window, self).__init__(parent)
        self.setupUi(self)
        self.is_download = False  # 是否正在下载
        self.is_upload = False  # 是否正在上传
        self.is_complete = False  # 是否有传输完成的任务
        self.top_column = {'upload': 1, 'download': 0, 'complete': 2}  # 顶部栏
        self.init_ui()  # 界面初始化

        Qss = GLOBAL_BUTTON
        Qss += 'QWidget#widget{background-color:%s;}' % BACKGROUND_COLOR
        Qss += 'QWidget#widget_2{background-color:%s;}' % TITLE_COLOR
        for btn in self.top_column:
            Qss += '#%s_btn{background-color:%s; border-radius:0;}' % (
                btn, TITLE_COLOR)
            Qss += '#%s_btn:hover{background-color:%s; border-radius:0;}' % (
                btn, LIGHT_FUNC_COLOR)
            eval(f'self.{btn}_btn').setCursor(
                QCursor(Qt.PointingHandCursor))  # 鼠标悬停按钮上时变小手
        self.setStyleSheet(Qss)  # 边框部分qss重载

        # 静态页面设置
        self.label.setPixmap(QPixmap(f'{ABSOLUTE_PATH}/img/download.png').scaled(
            self.label.width(), self.label.height()))  # 添加logo
        self.label_4.setPixmap(QPixmap(
            f'{ABSOLUTE_PATH}/img/upload.png').scaled(self.label_4.width(), self.label_4.height()))
        self.label_3.setPixmap(QPixmap(
            f'{ABSOLUTE_PATH}/img/history.png').scaled(self.label_3.width(), self.label_3.height()))

        # 按钮功能实现
        self.closeButton.clicked.connect(self.signalClose)
        self.minButton.clicked.connect(self.showMinimized)
        self.upload_btn.clicked.connect(
            lambda: self.btn_top('upload'))  # 上传列表按钮
        self.upload_btn.setIcon(qtawesome.icon('fa.upload'))
        self.download_btn.clicked.connect(
            lambda: self.btn_top('download'))  # 下载列表按钮
        self.download_btn.setIcon(qtawesome.icon('fa.download'))
        self.complete_btn.clicked.connect(
            lambda: self.btn_top('complete'))  # 传输完成按钮
        self.complete_btn.setIcon(qtawesome.icon('fa.check-square-o'))

    def init_ui(self):
        """界面初始化
        """
        self.download_btn.setStyleSheet(
            '#download_btn{background-color:%s; color:%s; border-bottom:5px solid %s}' % (FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))
        if self.is_download:
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.stackedWidget.setCurrentIndex(3)

    def btn_top(self, btn_name):
        """顶部栏栏按钮对应事件
        """
        top_btn = btn_name + '_btn'
        eval(f'self.{top_btn}').setStyleSheet('#%s{background-color:%s; color:%s; border-bottom:5px solid %s}' %
                                              (top_btn, FUNC_COLOR, HOVER_COLOR, HOVER_COLOR))  # 当前点击按钮高亮
        if eval(f'self.is_{btn_name}'):
            self.stackedWidget.setCurrentIndex(self.top_column[btn_name])
        else:
            self.stackedWidget.setCurrentIndex(self.top_column[btn_name]+3)
        for btn in self.top_column:  # 其他按钮全部恢复
            if btn != btn_name:
                eval(f'self.{btn}_btn').setStyleSheet(
                    '#%s{background-color:%s; border-radius:0;}' % (f'{btn}_btn', TITLE_COLOR))

    def signalClose(self):
        """淡出关闭窗口并向父窗口发送已关闭的信息
        """
        self.signal.emit(False)
        self.doClose()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    login_window = Login_window()
    login_window.show()

    sys.exit(app.exec_())
