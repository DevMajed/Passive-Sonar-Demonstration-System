# PyQt5 imports for UI elements
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QSizePolicy, \
                            QButtonGroup, QGridLayout
from PyQt5.QtCore import pyqtSignal

from PyQt5 import QtGui

# used for measuring time for debugging
import time

# For handling debug output
import logging

class ControlGroupBox(QGroupBox):
    """
    Group box containing input and output mode buttons.
    """

    # Signals for beginning and ending input/output mode.
    # They connect to MainWindow object in mainWindow.py, and are handled there.
    beginInputModeSignal = pyqtSignal()
    endInputModeSignal = pyqtSignal()
    beginOutputModeSignal = pyqtSignal(int)
    endOutputModeSignal = pyqtSignal()

    def __init__(self, debug):
        super().__init__()
        self.initUI()
        self.debug = debug

    def initUI(self):
        """
        Initializes UI elements for the group box.
        """
        self.buttonLayout = QGridLayout()
        self.initButtons()
        self.createSoundButtonGroup()
        self.createCommentaryButtonGroup()
        self.setLayout(self.buttonLayout)

    #region BUTTON SETUP
    def initButtons(self):
        """
        Initializes 6 buttons. 3 are for the output mode sounds, the other 3 are for the commentary
        for those sounds. Creates buttons, sets fonts, and adds them to the layout.
        """
        self.soundButtonLayout = QVBoxLayout()
        self.commentaryButtonLayout = QVBoxLayout()

        self.button1 = self.createButton("Whale", self.soundButtonLayout)
        self.button1.setFont(QtGui.QFont("Arial", 12,))
        self.button2 = self.createButton("Shrimp", self.soundButtonLayout)
        self.button2.setFont(QtGui.QFont("Arial", 12,))
        self.button3 = self.createButton("Ship", self.soundButtonLayout)
        self.button3.setFont(QtGui.QFont("Arial", 12,))
        #self.button4 = self.createButton("Quiet Target", self.soundButtonLayout)
        # self.hiddenButton = QPushButton()
        # self.hiddenButton.setCheckable(True)

        self.button1Commentary = self.createButton("Commentary", self.commentaryButtonLayout)
        self.button1Commentary.setFont(QtGui.QFont("Arial", 12,))
        #self.button1Commentary.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)))

        self.button2Commentary = self.createButton("Commentary", self.commentaryButtonLayout)
        self.button2Commentary.setFont(QtGui.QFont("Arial", 12,))
        #self.button2Commentary.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)))

        self.button3Commentary = self.createButton("Commentary", self.commentaryButtonLayout)
        self.button3Commentary.setFont(QtGui.QFont("Arial", 12,))
        #self.button3Commentary.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)))

        #self.button4Commentary = self.createButton("? 4", self.commentaryButtonLayout)

        self.userInputButton = QPushButton("User Input")
        self.userInputButton.setFont(QtGui.QFont("Arial", 12,))
        self.userInputButton.setCheckable(True)
        self.userInputButton.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))

        self.userInputButton.clicked.connect(self.onUserInputButtonClicked)

        self.buttonLayout.addLayout(self.soundButtonLayout, 0, 0, 4, 1)
        self.buttonLayout.addLayout(self.commentaryButtonLayout, 0, 1, 4, 1)
        self.buttonLayout.addWidget(self.userInputButton, 4, 0, 1, 2)

    def createButton(self, name, layout):
        """
        Creates a QPushButton with passed name, adds it to passed layout
        returns QPushButton object

        Arguments:
            name (str) - button label, to be displayed on button in UI
            layout (QVBoxLayout) - layout to add button to
        Returns:
            QPushButton - returns created button
        """
        btn = QPushButton(name)
        btn.setCheckable(True)
        layout.addWidget(btn)
        btn.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        return btn

    def createSoundButtonGroup(self):
        """
        Creates a QButtonGroup for the four output mode buttons. Makes it easier to determine which
        button within the group was pressed.
        """
        self.soundButtonGroup = QButtonGroup()
        self.soundButtonGroup.setExclusive(False)
        self.soundButtonGroup.addButton(self.button1, 1)
        self.soundButtonGroup.addButton(self.button2, 2)
        self.soundButtonGroup.addButton(self.button3, 3)
        # self.soundButtonGroup.addButton(self.button4, 4)
        # self.soundButtonGroup.addButton(self.hiddenButton, 5)

        self.soundButtonGroup.buttonClicked.connect(self.onSoundButtonClicked)  # when any button in group clicked, call onSoundButtonClicked method

    def createCommentaryButtonGroup(self):
        """
        Creates a QButtonGroup for the four commentary buttons. Makes it easier to determine which
        button within the group was pressed.
        """
        self.commentaryButtonGroup = QButtonGroup()
        self.commentaryButtonGroup.setExclusive(False)
        self.commentaryButtonGroup.addButton(self.button1Commentary, 1)
        self.commentaryButtonGroup.addButton(self.button2Commentary, 2)
        self.commentaryButtonGroup.addButton(self.button3Commentary, 3)
        # self.commentaryButtonGroup.addButton(self.button4Commentary, 4)

        self.commentaryButtonGroup.buttonClicked.connect(self.onCommentaryButtonClicked)

    #endregion

    #region ON BUTTON CLICKED
    # methods called when buttons clicked
    def onSoundButtonClicked(self, btn):
        """
        Method called when sound button is clicked. Determines which button was clicked,
        if it is being selected or de-selected, and emits begin/end output/input mode
        signals accordingly.

        Arguments:
            btn (QPushButton) - button that was clicked
        """

        # debug
        self.clickedTime = time.time()
        logging.info("\t{0}".format(btn.text()))    # print name of button that was pressed

        btnID = self.soundButtonGroup.checkedId()   # get the ID number of button that was pressed

        btnChecked = btn.isChecked()    # determine if the button was selected or de-selected

        # uncheck all other buttons
        self.userInputButton.setChecked(False)
        for button in self.commentaryButtonGroup.buttons():
            button.setChecked(False)
        for button in self.soundButtonGroup.buttons():
            if button != btn:
                button.setChecked(False)    # uncheck all other sound buttons

        # if button is being checked, end input mode and begin output mode for that button
        if btnChecked:
            self.endInputModeSignal.emit()
            # print("end input mode signal emitted")
            self.beginOutputModeSignal.emit(btnID)
            # print("begin output mode signal emitted (button {0})".format(btnID))
        # button is being unchecked, end output mode
        else:
            self.endOutputModeSignal.emit()
            # print("end output mode signal emitted")

    def onCommentaryButtonClicked(self, btn):
        """
        Method called when commentary button is clicked. Determines which button was clicked,
        if it is being selected or de-selected, and emits begin/end output/input mode
        signals accordingly.

        Arguments:
            btn (QPushButton) - button that was clicked
        """

        # debug
        self.clickedTime = time.time()
        logging.info("\t{0}".format(btn.text()))    # print name of button that was pressed

        btnID = self.commentaryButtonGroup.checkedId()  # get the ID number of button that was pressed

        btnChecked = btn.isChecked()    # determine if the button was selected or de-selected

        # uncheck all other buttons
        self.userInputButton.setChecked(False)
        for button in self.soundButtonGroup.buttons():
            button.setChecked(False)
        for button in self.commentaryButtonGroup.buttons():
            if button != btn:
                button.setChecked(False)

        # if button is being checked, end input mode and begin output mode for that button
        if btnChecked:
            self.endInputModeSignal.emit()
            self.beginOutputModeSignal.emit(btnID + len(self.soundButtonGroup.buttons()))
                                                    # first comm btn ID is after last sound btn ID
                                                    # allows number of sound buttons to change if needed
        # button is being unchecked, end output mode
        else:
            self.endOutputModeSignal.emit()
            # print("end output mode signal emitted")

    def onUserInputButtonClicked(self, btnChecked):
        """
        Method called when input button is clicked. Determines which button was clicked,
        if it is being selected or de-selected, and emits begin/end input/output mode
        signals accordingly.

        Arguments:
            btnChecked (bool) - button that was clicked
        """

        # debug
        self.clickedTime = time.time()

        # uncheck output mode buttons
        for button in self.commentaryButtonGroup.buttons():
            button.setChecked(False)
        for button in self.soundButtonGroup.buttons():
            button.setChecked(False)

        # if button is being checked, begin input mode
        if btnChecked:
            self.endOutputModeSignal.emit()
            # print("end output mode signal emitted")
            self.beginInputModeSignal.emit()
            # print("begin input mode signal emitted")
        # button is being unchecked, end input mode
        else:
            self.endInputModeSignal.emit()
            # print("end input mode signal emitted")

    #endregion