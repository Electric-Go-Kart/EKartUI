# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFrame, QLCDNumber,
    QLabel, QPlainTextEdit, QProgressBar, QPushButton,
    QSizePolicy, QSlider, QTabWidget, QTimeEdit,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 480)
        palette = QPalette()
        brush = QBrush(QColor(0, 153, 102, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush1 = QBrush(QColor(0, 61, 61, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(255, 51, 51, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush2)
        brush3 = QBrush(QColor(0, 153, 255, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
#endif
        Widget.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Impact"])
        font.setBold(True)
        Widget.setFont(font)
        Widget.setAutoFillBackground(True)
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 781, 401))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        palette1 = QPalette()
        brush4 = QBrush(QColor(51, 51, 51, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush4)
        brush5 = QBrush(QColor(255, 51, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Highlight, brush5)
        palette1.setBrush(QPalette.Active, QPalette.Accent, brush5)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        palette1.setBrush(QPalette.Inactive, QPalette.Highlight, brush5)
        palette1.setBrush(QPalette.Inactive, QPalette.Accent, brush5)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Accent, brush5)
        self.tabWidget.setPalette(palette1)
        font1 = QFont()
        font1.setFamilies([u"Impact"])
        font1.setPointSize(18)
        font1.setBold(True)
        self.tabWidget.setFont(font1)
        self.tabWidget.setCursor(QCursor(Qt.OpenHandCursor))
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setIconSize(QSize(44, 26))
        self.tabWidget.setElideMode(Qt.ElideMiddle)
        self.dash = QWidget()
        self.dash.setObjectName(u"dash")
        palette2 = QPalette()
        brush6 = QBrush(QColor(0, 0, 0, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush6)
        brush7 = QBrush(QColor(102, 102, 102, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Dark, brush7)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush4)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush6)
        palette2.setBrush(QPalette.Inactive, QPalette.Dark, brush7)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush7)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush6)
        palette2.setBrush(QPalette.Disabled, QPalette.Dark, brush7)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush7)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush7)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        self.dash.setPalette(palette2)
        self.Drive_Reverse = QSlider(self.dash)
        self.Drive_Reverse.setObjectName(u"Drive_Reverse")
        self.Drive_Reverse.setGeometry(QRect(40, 60, 101, 261))
        self.Drive_Reverse.setAutoFillBackground(True)
        self.Drive_Reverse.setMinimum(1)
        self.Drive_Reverse.setMaximum(3)
        self.Drive_Reverse.setPageStep(10)
        self.Drive_Reverse.setSliderPosition(2)
        self.Drive_Reverse.setTracking(False)
        self.Drive_Reverse.setOrientation(Qt.Vertical)
        self.Drive_Reverse.setInvertedAppearance(False)
        self.Drive_Reverse.setInvertedControls(True)
        self.Drive_Reverse.setTickPosition(QSlider.TicksBothSides)
        self.GaugeSpeed = QLCDNumber(self.dash)
        self.GaugeSpeed.setObjectName(u"GaugeSpeed")
        self.GaugeSpeed.setEnabled(True)
        self.GaugeSpeed.setGeometry(QRect(320, 260, 121, 81))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        self.GaugeSpeed.setPalette(palette3)
        self.GaugeSpeed.setFocusPolicy(Qt.TabFocus)
        self.GaugeSpeed.setAcceptDrops(False)
        self.GaugeSpeed.setLayoutDirection(Qt.LeftToRight)
        self.GaugeSpeed.setAutoFillBackground(True)
        self.GaugeSpeed.setFrameShape(QFrame.Panel)
        self.GaugeSpeed.setFrameShadow(QFrame.Raised)
        self.GaugeSpeed.setLineWidth(2)
        self.GaugeSpeed.setSmallDecimalPoint(False)
        self.GaugeSpeed.setDigitCount(3)
        self.GaugeSpeed.setSegmentStyle(QLCDNumber.Flat)
        self.plainTextEdit = QPlainTextEdit(self.dash)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(40, 30, 101, 31))
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.Button, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Light, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Midlight, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Dark, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette4.setBrush(QPalette.Active, QPalette.BrightText, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Shadow, brush5)
        palette4.setBrush(QPalette.Active, QPalette.ToolTipText, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Light, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Midlight, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Dark, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.BrightText, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Shadow, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Light, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Midlight, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Dark, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.BrightText, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Shadow, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush5)
        self.plainTextEdit.setPalette(palette4)
        font2 = QFont()
        font2.setFamilies([u"Impact"])
        font2.setPointSize(20)
        font2.setBold(True)
        self.plainTextEdit.setFont(font2)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit_2 = QPlainTextEdit(self.dash)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setGeometry(QRect(40, 320, 101, 31))
        palette5 = QPalette()
        brush8 = QBrush(QColor(255, 255, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette5.setBrush(QPalette.Active, QPalette.WindowText, brush8)
        palette5.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Inactive, QPalette.WindowText, brush8)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        self.plainTextEdit_2.setPalette(palette5)
        self.plainTextEdit_2.setFont(font2)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setTextInteractionFlags(Qt.NoTextInteraction)
        self.pushButton = QPushButton(self.dash)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(610, 20, 150, 75))
        palette6 = QPalette()
        palette6.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette6.setBrush(QPalette.Active, QPalette.Base, brush5)
        palette6.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette6.setBrush(QPalette.Active, QPalette.HighlightedText, brush5)
        palette6.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette6.setBrush(QPalette.Inactive, QPalette.Base, brush5)
        palette6.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette6.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush5)
        palette6.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette6.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette6.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette6.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush5)
        self.pushButton.setPalette(palette6)
        self.pushButton.setFont(font2)
        self.pushButton.setAutoFillBackground(True)
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)
        self.label = QLabel(self.dash)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 0, 321, 311))
        self.label.setPixmap(QPixmap(u"NewUI_sized_DashRam.png"))
        self.label.setScaledContents(True)
        self.BatteryBar = QProgressBar(self.dash)
        self.BatteryBar.setObjectName(u"BatteryBar")
        self.BatteryBar.setGeometry(QRect(610, 270, 150, 50))
        palette7 = QPalette()
        palette7.setBrush(QPalette.Active, QPalette.Window, brush4)
        palette7.setBrush(QPalette.Active, QPalette.Shadow, brush1)
        palette7.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        palette7.setBrush(QPalette.Inactive, QPalette.Shadow, brush1)
        palette7.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette7.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        palette7.setBrush(QPalette.Disabled, QPalette.Shadow, brush1)
        self.BatteryBar.setPalette(palette7)
        self.BatteryBar.setAutoFillBackground(True)
        self.BatteryBar.setValue(24)
        self.plainTextEdit_3 = QPlainTextEdit(self.dash)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")
        self.plainTextEdit_3.setGeometry(QRect(320, 340, 121, 31))
        palette8 = QPalette()
        palette8.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette8.setBrush(QPalette.Active, QPalette.Text, brush8)
        palette8.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette8.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.Text, brush8)
        palette8.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        self.plainTextEdit_3.setPalette(palette8)
        self.plainTextEdit_3.setFont(font2)
        self.plainTextEdit_3.setLayoutDirection(Qt.LeftToRight)
        self.plainTextEdit_3.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setTextInteractionFlags(Qt.NoTextInteraction)
        self.plainTextEdit_3.setBackgroundVisible(False)
        self.TempGauge = QLCDNumber(self.dash)
        self.TempGauge.setObjectName(u"TempGauge")
        self.TempGauge.setGeometry(QRect(610, 130, 150, 75))
        palette9 = QPalette()
        palette9.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        self.TempGauge.setPalette(palette9)
        self.TempGauge.setAutoFillBackground(True)
        self.TempGauge.setLineWidth(5)
        self.TempGauge.setSmallDecimalPoint(True)
        self.TempGauge.setSegmentStyle(QLCDNumber.Flat)
        self.TempGauge.setProperty("value", 66.876000000000005)
        self.TempGauge.setProperty("intValue", 67)
        self.plainTextEdit_4 = QPlainTextEdit(self.dash)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")
        self.plainTextEdit_4.setGeometry(QRect(610, 200, 150, 31))
        palette10 = QPalette()
        palette10.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette10.setBrush(QPalette.Active, QPalette.Text, brush8)
        palette10.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette10.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.Text, brush8)
        palette10.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        self.plainTextEdit_4.setPalette(palette10)
        self.plainTextEdit_4.setFont(font2)
        self.plainTextEdit_4.setLayoutDirection(Qt.LeftToRight)
        self.plainTextEdit_4.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.plainTextEdit_4.setReadOnly(True)
        self.plainTextEdit_4.setTextInteractionFlags(Qt.NoTextInteraction)
        self.plainTextEdit_4.setBackgroundVisible(False)
        self.plainTextEdit_5 = QPlainTextEdit(self.dash)
        self.plainTextEdit_5.setObjectName(u"plainTextEdit_5")
        self.plainTextEdit_5.setGeometry(QRect(610, 320, 150, 31))
        palette11 = QPalette()
        palette11.setBrush(QPalette.Active, QPalette.Button, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Light, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Midlight, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Dark, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette11.setBrush(QPalette.Active, QPalette.BrightText, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette11.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Shadow, brush5)
        palette11.setBrush(QPalette.Active, QPalette.ToolTipText, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Button, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Light, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Midlight, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Dark, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.BrightText, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette11.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Shadow, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Button, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Light, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Midlight, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Dark, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.BrightText, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Shadow, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush5)
        self.plainTextEdit_5.setPalette(palette11)
        self.plainTextEdit_5.setFont(font2)
        self.plainTextEdit_5.setReadOnly(True)
        self.tabWidget.addTab(self.dash, "")
        self.Drive_Reverse.raise_()
        self.plainTextEdit.raise_()
        self.plainTextEdit_2.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.BatteryBar.raise_()
        self.plainTextEdit_3.raise_()
        self.TempGauge.raise_()
        self.plainTextEdit_4.raise_()
        self.plainTextEdit_5.raise_()
        self.GaugeSpeed.raise_()
        self.oakd = QWidget()
        self.oakd.setObjectName(u"oakd")
        self.tabWidget.addTab(self.oakd, "")
        self.timeEdit = QTimeEdit(Widget)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(300, 420, 181, 51))
        palette12 = QPalette()
        palette12.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette12.setBrush(QPalette.Active, QPalette.Text, brush8)
        palette12.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette12.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette12.setBrush(QPalette.Active, QPalette.Accent, brush5)
        palette12.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette12.setBrush(QPalette.Inactive, QPalette.Text, brush8)
        palette12.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette12.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette12.setBrush(QPalette.Inactive, QPalette.Accent, brush5)
        palette12.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette12.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette12.setBrush(QPalette.Disabled, QPalette.Accent, brush5)
        self.timeEdit.setPalette(palette12)
        font3 = QFont()
        font3.setFamilies([u"Impact"])
        font3.setPointSize(40)
        font3.setBold(True)
        self.timeEdit.setFont(font3)
        self.timeEdit.setAutoFillBackground(True)
        self.timeEdit.setAlignment(Qt.AlignCenter)
        self.timeEdit.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.timeEdit.setDateTime(QDateTime(QDate(1999, 1, 29), QTime(21, 0, 0)))

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("Widget", u"  Forwards", None))
        self.plainTextEdit_2.setPlainText(QCoreApplication.translate("Widget", u"Backwards", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Power OFF", None))
        self.label.setText("")
        self.plainTextEdit_3.setPlainText(QCoreApplication.translate("Widget", u"          MPH", None))
        self.plainTextEdit_4.setPlainText(QCoreApplication.translate("Widget", u"  Motor Temp (\u00b0F)", None))
        self.plainTextEdit_5.setPlainText(QCoreApplication.translate("Widget", u"       Battery (%)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dash), QCoreApplication.translate("Widget", u"Dashboard", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.oakd), QCoreApplication.translate("Widget", u"Camera", None))
    # retranslateUi

