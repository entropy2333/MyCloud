import sys
import os
root_path = os.getcwd()
sys.path.append(f'{root_path}\\qt')
sys.path.append('..')
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget,\
    QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem,\
    QSizePolicy
from UI.Ui_warn_dialog import Ui_Warn_Dialog
from UI.Ui_info_dialog import Ui_Info_Dialog


Stylesheet = """
#Custom_Widget {
    background: white;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
#Warn_Widget{
    background: red;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
#Info_Widget{
    background: #4DBCFF;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: white;
    background: red;
}
#pushButton {
    border-radius: 10px;
}
#pushButton:hover {
    background: #D3D3D3;
}
"""

class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)
        self.initUi()
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def initUi(self):
        layout = QVBoxLayout(self)
        # 重点： 这个widget作为背景和圆角
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout.addWidget(self.widget)


        # 在widget中添加ui
        layout = QGridLayout(self.widget)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
        layout.addWidget(QPushButton(
            'r', self, clicked=self.accept, objectName='closeButton'), 0, 1)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum,
                                   QSizePolicy.Expanding), 1, 0)

    def sizeHint(self):
        return QSize(400, 200)


class Warn_Dialog(QDialog, Ui_Warn_Dialog):
    def __init__(self, *args, **kwargs):
        super(Warn_Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.widget.setObjectName('Custom_Widget')
        self.widget_2.setObjectName('Warn_Widget')
        self.setStyleSheet(Stylesheet)
        self.label_2.setStyleSheet('color:white')
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        self.pushButton.clicked.connect(self.close)

    def sizeHint(self):
        return QSize(400, 200)


class Info_Dialog(QDialog, Ui_Info_Dialog):
    def __init__(self, *args, **kwargs):
        super(Info_Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.widget.setObjectName('Custom_Widget')
        self.widget_2.setObjectName('Info_Widget')
        self.setStyleSheet(Stylesheet)
        self.label_2.setStyleSheet('color:white')
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        self.pushButton.clicked.connect(self.close)

    def sizeHint(self):
        return QSize(400, 200)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # w = Warn_Dialog()
    w = Info_Dialog()
    w.exec_()
    QTimer.singleShot(200, app.quit)
    sys.exit(app.exec_())
