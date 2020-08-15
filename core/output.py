from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MediaPlayer(QMediaPlayer):
    """
    Handles playing of output mode/commentary files
    """
    def __init__(self):
        super().__init__()
        self.setVolume(50)  # initial volume, not muted

    def buttonToFile(self, index):
        if index == 1:
            # whale
            self.setMedia(QMediaContent(QUrl.fromLocalFile("./sounds/hump1.mp3")))
            # self.setMedia(QMediaContent(QUrl.fromLocalFile("C:/Users/Jacob/Documents/repos/ECE-7-Passive-Sonar-Demonstration/sounds/hump1.mp3")))
            self.play()
            print("PLAYING whale sound")

        elif index == 2:
            # shrimp
            self.setMedia(QMediaContent(QUrl.fromLocalFile("./sounds/snap2.mp3")))
            print("PLAYING shrimp sound")
            self.play()
        elif index == 3:
            # ship
            self.setMedia(QMediaContent(QUrl.fromLocalFile("./sounds/light.mp3")))
            print("PLAYING ship sound")
            self.play()
        elif index == 4:
            # whale (COMMENTARY)
            self.setMedia(QMediaContent(QUrl.fromLocalFile("./sounds/hump1.mp3")))
            print("PLAYING whale (commentary)")
            self.play()
        elif index == 5:
            # shrimp (COMMENTARY)
            self.setMedia(QMediaContent(QUrl.fromLocalFile("./sounds/snap2.mp3")))
            print("PLAYING shrimp (commentary)")
            self.play()
        elif index == 6:
            # ship (COMMENTARY)
            self.setMedia(QMediaContent(QUrl.fromLocalFile("./sounds/light.mp3")))
            print("PLAYING ship (commentary)")
            self.play()
        elif index == 7:
            pass
        elif index == 8:
            pass
        else:
            pass

    def stopPlayback(self):
        self.stop()