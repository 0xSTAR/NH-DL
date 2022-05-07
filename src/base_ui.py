from PyQt6 import QtCore, QtGui, QtWidgets
from lang_db import (
        SELECTED_LANG,
        LANGS,
        LANG_DB
)
#from copy import deepcopy


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(440, 679)

        ### UNIVERSAL APP FONT ###

        QtGui.QFontDatabase.addApplicationFont("content/FiraCode-Bold.ttf")
        UNIVERSAL_FONT = QtGui.QFont("Fira Code")

        ##########################

        self.sauceBox = QtWidgets.QLineEdit(Form)
        self.sauceBox.setGeometry(QtCore.QRect(40, 239, 251, 41))
        font = UNIVERSAL_FONT#QtGui.QFont()
        font.setPointSize(20)
        self.sauceBox.setFont(font)
        self.sauceBox.setStyleSheet("background: rgba(255, 255, 255,195);")
        self.sauceBox.setMaxLength(6)
        self.sauceBox.setFrame(True)
        self.sauceBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sauceBox.setObjectName("sauceBox")

        self.saveDirectory = QtWidgets.QLineEdit(Form)
        self.saveDirectory.setGeometry(QtCore.QRect(40, 350, 351, 41))
        font = UNIVERSAL_FONT#deepcopy(UNIVERSAL_FONT)#QtGui.QFont()
        font.setPointSize(20)
        self.saveDirectory.setFont(font)
        self.saveDirectory.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.saveDirectory.setStyleSheet("background: rgba(255, 255, 255,195);")
        self.saveDirectory.setInputMask("")
        self.saveDirectory.setText("")
        self.saveDirectory.setFrame(True)
        self.saveDirectory.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.saveDirectory.setCursorPosition(0)
        self.saveDirectory.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.saveDirectory.setReadOnly(True)
        self.saveDirectory.setObjectName("saveDirectory")

        self.labelSauce = QtWidgets.QLabel(Form)
        self.labelSauce.setGeometry(QtCore.QRect(40, 190, 200, 35))
        font = UNIVERSAL_FONT#deepcopy(UNIVERSAL_FONT)#QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.labelSauce.setFont(font)
        self.labelSauce.setAutoFillBackground(False)
        self.labelSauce.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelSauce.setLineWidth(0)
        self.labelSauce.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.labelSauce.setObjectName("labelSauce")
        self.saveDirLabel = QtWidgets.QLabel(Form)
        self.saveDirLabel.setGeometry(QtCore.QRect(40, 310, 200, 35))

        font = UNIVERSAL_FONT#deepcopy(UNIVERSAL_FONT)#QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.saveDirLabel.setFont(font)
        self.saveDirLabel.setAutoFillBackground(False)
        self.saveDirLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.saveDirLabel.setLineWidth(0)
        self.saveDirLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.saveDirLabel.setObjectName("saveDirLabel")

        self.downloadFrame = QtWidgets.QFrame(Form)
        self.downloadFrame.setGeometry(QtCore.QRect(310, 240, 81, 41))
        self.downloadFrame.setStyleSheet("border-width: 10px;\n"
"border-radius: 50px; \n"
"")
        self.downloadFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.downloadFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.downloadFrame.setObjectName("downloadFrame")

        self.exitButton_2 = QtWidgets.QPushButton(self.downloadFrame)
        self.exitButton_2.setGeometry(QtCore.QRect(0, 0, 81, 41))
        font = UNIVERSAL_FONT#deepcopy(UNIVERSAL_FONT)#QtGui.QFont()
        #font.setFamily("Sans Serif")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.exitButton_2.setFont(font)
        self.exitButton_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        self.exitButton_2.setStyleSheet("background: rgb(236,40,84); \n"
"color: rgb(255,255,255);")
        self.exitButton_2.setObjectName("exitButton_2")

        self.changeDirectoryFrame = QtWidgets.QFrame(Form)
        self.changeDirectoryFrame.setGeometry(QtCore.QRect(40, 400, 351, 41))
        self.changeDirectoryFrame.setStyleSheet("border-width: 10px;\n"
"border-radius: 50px; \n"
"")
        self.changeDirectoryFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.changeDirectoryFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.changeDirectoryFrame.setObjectName("changeDirectoryFrame")
        self.changeDirectory = QtWidgets.QPushButton(self.changeDirectoryFrame)
        self.changeDirectory.setGeometry(QtCore.QRect(0, 0, 351, 41))
        font = UNIVERSAL_FONT#deepcopy(UNIVERSAL_FONT)#QtGui.QFont()
        #font.setFamily("Sans Serif")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.changeDirectory.setFont(font)
        self.changeDirectory.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        self.changeDirectory.setStyleSheet("background: rgb(236,40,84); \n"
"color: rgb(255,255,255);")
        self.changeDirectory.setObjectName("changeDirectory")


        self.progressionBar = QtWidgets.QProgressBar(Form)
        self.progressionBar.setGeometry(QtCore.QRect(40, 510, 351, 81))
        self.progressionBar.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.progressionBar.setStyleSheet("QProgressBar::chunk {\n"
"    background-color: rgb(236,40,84); \n"
"    color:rgba(220,220,210,190)\n"
"};\n"
"")
        self.progressionBar.setProperty("value", 0)
        self.progressionBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progressionBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.progressionBar.setInvertedAppearance(False)
        self.progressionBar.setTextDirection(QtWidgets.QProgressBar.Direction.TopToBottom)
        self.progressionBar.setObjectName("progressionBar")


        self.labelStatus = QtWidgets.QLabel(Form)
        self.labelStatus.setGeometry(QtCore.QRect(40, 460, 270, 41))
        font = UNIVERSAL_FONT#deepcopy(UNIVERSAL_FONT)#QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.labelStatus.setFont(font)
        self.labelStatus.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelStatus.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.labelStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.labelStatus.setObjectName("labelStatus")


        self.BG = QtWidgets.QLabel(Form)
        self.BG.setGeometry(QtCore.QRect(0, 0, 440, 679))
        self.BG.setText("")
        self.BG.setPixmap(QtGui.QPixmap("content/bg0.png"))
        self.BG.setScaledContents(False)
        self.BG.setObjectName("BG")


        self.LOGO = QtWidgets.QLabel(Form)
        self.LOGO.setGeometry(QtCore.QRect(40, 20, 364, 160))
        self.LOGO.setText("")
        self.LOGO.setPixmap(QtGui.QPixmap("content/nh0.png"))
        self.LOGO.setObjectName("LOGO")


        self.BG.raise_()
        self.sauceBox.raise_()
        self.saveDirectory.raise_()
        self.labelSauce.raise_()
        self.saveDirLabel.raise_()
        self.downloadFrame.raise_()
        self.changeDirectoryFrame.raise_()
        self.progressionBar.raise_()
        self.labelStatus.raise_()
        self.LOGO.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate

        Form.setWindowTitle(_translate("Form", "NH"))

        self.sauceBox.setPlaceholderText(_translate("Form", "177013"))
        self.saveDirectory.setPlaceholderText(_translate("Form", "Select a Directory"))
        self.labelSauce.setText(_translate("Form", LANG_DB[SELECTED_LANG][0]))
        self.saveDirLabel.setText(_translate("Form", LANG_DB[SELECTED_LANG][1]))
        self.exitButton_2.setText(_translate("Form", LANG_DB[SELECTED_LANG][7]))
        self.changeDirectory.setText(_translate("Form", LANG_DB[SELECTED_LANG][2]))
        self.labelStatus.setText(_translate("Form", LANG_DB[SELECTED_LANG][6]))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
