# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QTabWidget, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 0, 791, 521))
        self.Oak_D = QWidget()
        self.Oak_D.setObjectName(u"Oak_D")
        self.tabWidget.addTab(self.Oak_D, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.pushButton = QPushButton(self.tab_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(620, 20, 131, 91))
        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 300, 111, 81))
        self.pushButton_3 = QPushButton(self.tab_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(20, 200, 111, 81))
        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 100, 111, 81))
        self.plainTextEdit = QPlainTextEdit(self.tab_2)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(40, 60, 71, 31))
        self.tabWidget.addTab(self.tab_2, "")
        self.dateTimeEdit = QDateTimeEdit(Widget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(250, 530, 291, 31))

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Oak_D), QCoreApplication.translate("Widget", u"Camera", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Shut Down", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"Drive", None))
        self.pushButton_3.setText(QCoreApplication.translate("Widget", u"Reverse", None))
        self.pushButton_4.setText(QCoreApplication.translate("Widget", u"Idle", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("Widget", u"   MODE", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Widget", u"Dashboard ", None))
    # retranslateUi

