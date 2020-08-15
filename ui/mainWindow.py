# PyQt5 imports for UI elements
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QSizePolicy, QLabel, qApp, QStackedWidget, QApplication, QStyle 
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtGui

# local UI imports
from ui.controlGroupBox import ControlGroupBox
from ui.plot import PlotCanvas

# local core imports
from core.input import UserInputStream
from core.output import MediaPlayer

# For handling debug output
import logging

# used for measuring time for debugging
import time

class MainWindow(QMainWindow):
    """
    Class that is called by main.py. Top level UI widget, provides connections between UI elements
    and audio functions.
    """
    def __init__(self, debug):
        super().__init__()

        # set debug mode
        self.debug = debug

        # microphone sample rate in Hz
        self.sampleRate = 48000

        # setup main window parameters
        self.title = "Passive Sonar Demonstration System"
        self.left = 100
        self.top = 100
        self.width = 1400
        self.height = 700
        self.minWidth = 800
        self.minHeight = 600
        self._main = MainWidget(debug)
        self.setCentralWidget(self._main)

        # initialize other classes
        self.inputStream = UserInputStream(self.sampleRate, debug)
        self.soundPlayer = MediaPlayer()

        # signal connections
        # input and output modes use buttons, plot, audio streams
        self._main.controlLayout.controlGroupBox.beginInputModeSignal.connect(self.beginInputMode)
        self._main.controlLayout.controlGroupBox.endInputModeSignal.connect(self.endInputMode)
        self._main.controlLayout.controlGroupBox.beginOutputModeSignal.connect(self.beginOutputMode)
        self._main.controlLayout.controlGroupBox.endOutputModeSignal.connect(self.endOutputMode)
        self._main.controlLayout.muteSignal.connect(self.mute)
        self._main.controlLayout.unmuteSignal.connect(self.unmute)

        self.initUI()
        logging.info("UI loaded.")

        # font = QtGui.QFont

    def initUI(self):
        """
        Initializes UI elements for the main window.
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(self.minWidth, self.minHeight)
        self.horizontalLayout = QHBoxLayout()
        self.setCentralWidget = self.horizontalLayout

        self.show()

    def closeEvent(self, event):
        """
        Called when the user closes the application.
        """
        logging.info("Application closed.")
        qApp.quit()

    def beginInputMode(self):
        """
        Begins input mode. Called when the user input mode button is pressed.
        """
        logging.info("BEGINNING INPUT MODE...")
        self._main.stackedwidget.setCurrentWidget(self._main.plot) # set current widget to plot
        self.inputStream.start()
        self._main.plot.beginAnimation(self.inputStream)
        if self.debug["time_buttons"]:
            logging.info("Time to begin input mode: {0} ms".format((time.time() - self._main.controlLayout.controlGroupBox.clickedTime) * 1000))

    def endInputMode(self):
        """
        Ends input mode. Called if input mode is active and user input button pressed again, or when output mode button pressed,
        before output mode begins.
        """
        logging.info("END INPUT MODE.")
        self.inputStream.stop()
        # starting output mode runs the endInputMode method
        # if input mode has not been run, the animation was not created yet and throws AttributeError
        try:
            self._main.plot.anim.event_source.stop()    # make sure animation stops
        except AttributeError:
            # error ignored, will not be raised after first frame of animation is created
            pass
        if self.debug["time_buttons"]:
            logging.info("Time to stop input mode: {0} ms".format((time.time() - self._main.controlLayout.controlGroupBox.clickedTime) * 1000))

    def beginOutputMode(self, btnID):
        """
        Begins output mode. Called when any output mode button is pressed (including commentary buttons).

        Arguments:
            btnID (int) - button ID number that was pressed, passed as part of the signal
        """
        logging.info("BEGINNING OUTPUT MODE FOR BUTTON {0}...".format(btnID))
        self._main.setImage(btnID)
        self._main.stackedwidget.setCurrentWidget(self._main.img) #set current widget to plot
        self.soundPlayer.buttonToFile(btnID)
        if self.debug["time_buttons"]:
            logging.info("Time to begin output mode: {0} ms".format((time.time() - self._main.controlLayout.controlGroupBox.clickedTime) * 1000))
            
    def endOutputMode(self):
        """
        Ends output mode. Called if output mode is active and same output button is pressed again, or when input mode button pressed,
        before output mode begins.
        """
        logging.info("END OUTPUT MODE.")
        self.soundPlayer.stopPlayback()
        if self.debug["time_buttons"]:
            logging.info("Time to stop output mode: {0} ms".format((time.time() - self._main.controlLayout.controlGroupBox.clickedTime) * 1000))

    def mute(self):
        """
        Mutes audio output. Called when mute button is activated.
        """
        logging.info("SOUND MUTED.")
        self.soundPlayer.setMuted(True)
        if self.debug["time_buttons"]:
            logging.info("Time to mute: {0} ms".format((time.time() - self._main.controlLayout.muteClickedTime) * 1000))

    def unmute(self):
        """
        Unmutes audio output. Called when mute button is deactivated.
        """
        logging.info("SOUND ON.")
        self.soundPlayer.setMuted(False)
        if self.debug["time_buttons"]:
            logging.info("Time to unmute: {0} ms".format((time.time() - self._main.controlLayout.muteClickedTime) * 1000))

class MainWidget(QWidget):
    """
    Widget containing bearing plot, sonargram displays, and buttons.
    """
    def __init__(self, debug):
        super().__init__()
        self.initUI(debug)

    def initUI(self, debug):
        """
        Initializes UI elements for the main widget.
        """
        self.layout = QHBoxLayout()
        self.stackedwidget = QStackedWidget()
        self.img = QLabel(self)
        self.pixmap1 = QPixmap('Sonargrams/Sonargram_1.png')
        self.pixmap2 = QPixmap('Sonargrams/Sonargram_2.png')
        self.pixmap3 = QPixmap('Sonargrams/Sonargram_3.png')
        self.plot = PlotCanvas(debug)
        self.stackedwidget.addWidget(self.img)
        self.stackedwidget.addWidget(self.plot)
        self.controlLayout = ControlLayout(debug)
        self.layout.addWidget(self.stackedwidget, 75)
        self.layout.addLayout(self.controlLayout, 25)
        self.setLayout(self.layout)
    
    def setImage(self, buttonID):
        """
        Changes sonargram image depending on which button was pressed.
        """
        if buttonID == 1 or buttonID == 4:
            self.img.setPixmap(self.pixmap1)
            self.img.setScaledContents(True)
        elif buttonID == 2 or buttonID == 5:
            self.img.setPixmap(self.pixmap2)
            self.img.setScaledContents(True)
        elif buttonID == 3 or buttonID == 6:
            self.img.setPixmap(self.pixmap3)
            self.img.setScaledContents(True)

class ControlLayout(QVBoxLayout):
    """
    Layout contains mute button, and control box (which contains output/input mode buttons).
    """

    # signals
    muteSignal = pyqtSignal()
    unmuteSignal = pyqtSignal()

    def __init__(self, debug):
        super().__init__()
        self.initUI(debug)

    def initUI(self, debug):
        self.controlGroupBox = ControlGroupBox(debug)    # defined in ui/controlGroupBox.py
        self.muteButton = QPushButton("Mute")
        self.muteButton.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.muteButton.setCheckable(True)
        self.muteButton.setFont(QtGui.QFont("Arial", 12))

        self.muteButton.clicked.connect(self.onMuteButtonClicked) #connect button click event to click function

        self.addWidget(self.controlGroupBox, 5)
        self.addWidget(self.muteButton, 1)

    def onMuteButtonClicked(self, btnChecked):
        self.muteClickedTime = time.time()
        if btnChecked:
            self.muteSignal.emit()
            self.muteButton.setText('Audio Disabled')

            self.muteButton.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MediaVolumeMuted)))
          
        else:
            self.unmuteSignal.emit()
            self.muteButton.setText('Audio Enabled')
            self.muteButton.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MediaVolume)))
         
# if __name__ == "__main__":
#     logging.info("Starting application.")
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     sys.exit(app.exec_())