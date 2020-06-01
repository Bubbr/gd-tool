import gdmt, os, json
import mainwin as mainwin
import startup as startup
from PyQt5 import QtMultimedia
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

# pyuic5 -x mainwin.ui -o mainwin.py

songs = json.load(open("Game.json", "r"))["songs"]

class InitWindow(QtWidgets.QMainWindow, startup.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.btn_openFile.clicked.connect(self.openDialog)

    def openDialog(self):
        self.file = QFileDialog.getOpenFileName(self, "Open file", filter="Ejecutable (*.exe)")[0]
        game = json.load(open('game.json', 'r'))
        game['meta']['game_dir'] = self.file

        with open('game.json', 'w') as f:
            json.dump(game, f)
        
        self.show_popup("Cierre y vuela a abrir la aplicación")
    
    def show_popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Listo")
        msg.setText(text)

        x = msg.exec_()

class MainWindow(QtWidgets.QMainWindow, mainwin.Ui_Dialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle(f"GDMT v2 - {gdmt.playerName}")
        self.searchLevel.clicked.connect(self.search)
        self.playSong.setEnabled(False)
        self.downloadSong.setEnabled(False)
        self.listensong.setEnabled(False)
        self.downloadSong.clicked.connect(self.downloadSongId)
        self.playSong.clicked.connect(self.playAudio)
        self.listensong.clicked.connect(self.setPage)
        self.searchSong.clicked.connect(self.searchSongList)
        self.loadSongs()

        #self.list_songs.mouseDoubleClickEvent.connect()
        self.deleteSong.clicked.connect(self.remSong)

        self.btn_load_local_levels.clicked.connect(self.loadLocals)

    def loadLocals(self):
        levels = gdmt.getLocalLevels()
        self.table_local_levels.setRowCount(len(levels))
        for i in range(len(levels)):
            item = QtWidgets.QTableWidgetItem()
            self.table_local_levels.setVerticalHeaderItem(i, item)
            item = self.table_local_levels.verticalHeaderItem(i)
            item.setText(levels[i].key)
            self.table_local_levels.setItem(i, 0, QtWidgets.QTableWidgetItem(levels[i].name))
            self.table_local_levels.setItem(i, 1, QtWidgets.QTableWidgetItem(levels[i].description.decode()))
            self.table_local_levels.setItem(i, 2, QtWidgets.QTableWidgetItem(levels[i].songInfo["name"]))
            self.table_local_levels.setItem(i, 3, QtWidgets.QTableWidgetItem(levels[i].len))

    def setPage(self):
        self.tab_music.setCurrentIndex(2)
        self.searchSongList(self.level.songInfo["id"])
        self.setAudio()
        self.playAudio()

    def show_popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)

        x = msg.exec_()

    def show_plumb(self, title, message, buttons):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        yes = msg.addButton(buttons[0], QMessageBox.YesRole)
        msg.addButton(buttons[1], QMessageBox.YesRole)

        x = msg.exec_()

        if msg.clickedButton() == yes:
            return True
        else:
            return False

    def searchSongList(self, sid=None):
        x = False
        if not sid:
            sid = self.songString.text().lower()
            for i in range(self.list_songs.count()):
                if not self.list_songs.item(i).text().lower().find(sid) == -1:
                    x = "_" + str(i)
                else:
                    pass
        else:
            for i in range(self.list_songs.count()):
                if str(self.list_songs.item(i).text().split(' | ')[0]) == str(sid):
                    x = "_" + str(i)
                else:
                    pass
        if x:
            self.list_songs.setCurrentRow(int(x[1:]))
        else:
            self.show_popup("No se encontró la busqueda")

    def loadSongs(self):
        self.updateSongs()
        if len(self.songs) > 0:
            for i in range(len(self.songs)):
                self.list_songs.takeItem(self.list_songs.row(self.list_songs.item(i)))
                self.list_songs.addItem(QtWidgets.QListWidgetItem())
                txt = f"{list(self.songs.keys())[i]} | {list(self.songs.values())[i]['name']}"
                self.list_songs.item(i).setText(txt)
        else:
            self.list_songs.takeItem(self.list_songs.row(self.list_songs.item(0)))

    def addSong(self, song):
        with open("Game.json", "r") as f:
            data = json.load(f)
        data["songs"][str(song["id"])] = {
            "id":song["id"],
            "name":song["name"],
            "by":song["by"],
            "id":song["id"],
            "Mb":song["Mb"],
            "url":song["url"],
            "path":f"./songs/{song['pathname']}"
        }
        json.dump(data, open("Game.json", "w"))

    def remSong(self):
        song = self.list_songs.selectedItems()[0].text()
        x = self.show_plumb(song, "Esta canción se eliminará de forma permanente.", ["Dale", "Mejor no"])
        if x:
            song = song.split(' | ')
            os.remove(self.songs[str(song[0])]["path"])
            self.removeSong(song[0])
            self.loadSongs()

    def removeSong(self, s):
        try:
            with open("Game.json", "r") as f:
                data = json.load(f)
            del data["songs"][str(s)]
            json.dump(data, open("Game.json", "w"))
            del self.songs[str(s)]
        except:
            pass

    def updateSongs(self):
        with open("Game.json", 'r') as f:
            self.songs = json.load(f)["songs"]
        awa = None
        err = True
        while err:
            try:
                err = False
                for s in self.songs:
                    awa = s
                    open(self.songs[str(awa)]["path"])
            except:
                err = True
                print("No existe", self.songs[str(awa)]["name"], "\nProcediendo a borrar")
                self.removeSong(awa)
                print("Listo!")

    def search(self):
        try:
            self.player.stop()
        except:
            pass
        self.listensong.setEnabled(False)
        self.level = gdmt.Level(name=self.levelString.text())
        if not self.level.err:
            self.level_info.setItem(0, 0, QtWidgets.QTableWidgetItem(self.level.id))
            self.level_info.setItem(0, 1, QtWidgets.QTableWidgetItem(self.level.name))
            self.level_info.setItem(0, 2, QtWidgets.QTableWidgetItem(self.level.description.decode()))
            self.level_info.setItem(0, 3, QtWidgets.QTableWidgetItem(self.level.creator.name))
            self.level_info.setItem(0, 4, QtWidgets.QTableWidgetItem(self.level.songInfo["url"]))
            try:
                self.songs[str(self.level.songInfo["id"])]
                self.listensong.setEnabled(True)
                self.setAudio()
            except:
                self.playSong.setEnabled(False)
                self.downloadSong.setEnabled(True)
                self.downloadSong.setText(f"Descargar canción ({self.level.songInfo['Mb']}MB)")
                self.playSong.setText("Reproducir")
        else:
            self.show_popup("Al parecer el nivel no existe :/. ¿Lo escribiste bien?")

    def downloadSongId(self):
        gdmt.downloadSong(self.level.songInfo, "./songs/")
        self.addSong(self.level.songInfo)
        self.setAudio()
        self.loadSongs()

    def setAudio(self):
        self.listensong.setEnabled(True)
        self.updateSongs()
        filename = self.songs[str(self.level.songInfo["id"])]["path"]
        fullpath = QtCore.QDir.current().absoluteFilePath(filename)
        url = QtCore.QUrl.fromLocalFile(fullpath)
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.playSong.setEnabled(True)
        self.downloadSong.setEnabled(False)
        self.playSong.setText("Reproducir")

    def playAudio(self):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
            self.playSong.setText("Reproducir")
        else:
            self.player.play()
            self.movinglikeatree = False
            self.player.positionChanged.connect(self.updateSong)
            self.songbar.sliderPressed.connect(self.tree)
            self.songbar.sliderReleased.connect(self.treent)
            self.playSong.setText("Pausar")

    def updateSong(self):
        try:
            if not self.movinglikeatree:
                self.songbar.setValue(int(self.player.position()/self.player.duration()*100))
                self.updateTimeStamp()
            if self.songbar.value() == 100:
                self.setAudio()
        except:
            pass
    
    def tree(self):
        self.movinglikeatree = True
    
    def treent(self):
        self.updateBar()
        self.movinglikeatree = False

    def updateTimeStamp(self):
        secs = int(self.player.position()/1000%60)
        if secs < 10:
            secs = f"0{secs}"
        timeStamp = f"{int(self.player.position()/1000/60%60)}:{secs}"
        total = f"{int(self.player.duration()/1000/60%60)}:{int(self.player.duration()/1000%60)}"
        self.song_timeStamp.setText(f"{timeStamp}/{total}")

    def updateBar(self):
        self.player.setPosition(int(self.songbar.sliderPosition()/100*self.player.duration()))

class MusicPlayer:
    def __init__(self):
        pass

    def play(self, url=None):
        pass

    def stop(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    arg = gdmt.Init()

    if arg[1] == -1:
        window = InitWindow()
    elif arg[1] == 0:
        window = MainWindow()

    window.show()
    app.exec_()
