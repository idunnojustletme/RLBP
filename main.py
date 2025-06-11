# main.py

import asyncio
import socket
import threading

from PySide6 import QtWidgets
from qasync import QApplication

import server
from intiface import IntifaceManager

app = QApplication
gui: QtWidgets.QMainWindow
server_thread: threading.Thread


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.intiface = IntifaceManager(self)
        self.setWindowTitle("RLBP")
        self.setGeometry(100, 100, 800, 800)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        hostname = socket.gethostname().lower()
        url_button = QtWidgets.QPushButton(
            f"Server (click to copy): http://{hostname}.local/Temporary_Listen_Addresses/"
        )
        url_button.clicked.connect(
            lambda: app.clipboard().setText(f"http://{hostname}.local/Temporary_Listen_Addresses/")
        )
        main_layout.addWidget(url_button)

        top_row = QtWidgets.QHBoxLayout()

        button1 = QtWidgets.QPushButton("Reconnect")
        button1.clicked.connect(lambda: asyncio.create_task(self.intiface.reconnect()))
        button2 = QtWidgets.QPushButton("Test Device(s)")
        button2.clicked.connect(lambda: asyncio.create_task(self.intiface.test_all_devices()))
        button3 = QtWidgets.QPushButton("Stop Vibration")
        button3.clicked.connect(lambda: asyncio.create_task(self.intiface.stop_vibrate()))
        self.button4 = QtWidgets.QPushButton("Start Score Monitoring")
        self.button4.clicked.connect(lambda: asyncio.create_task(self.intiface.score_vibrate()))
        button5 = QtWidgets.QPushButton("Reload Config")
        button5.clicked.connect(lambda: asyncio.create_task(self.intiface.config()))

        top_row.addWidget(button1)
        top_row.addWidget(button2)
        top_row.addWidget(button3)
        top_row.addWidget(self.button4)
        top_row.addWidget(button5)

        main_layout.addLayout(top_row)

        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        main_layout.addWidget(self.console)

    def closeEvent(self, event):
        cleanup()
        event.accept()

    def print(self, message: str):
        self.console.append(message)


def cleanup():
    global gui, server_thread
    asyncio.create_task(gui.intiface.stop_vibrate())
    asyncio.create_task(gui.intiface.disconnect())
    app.quit()
    gui.running = False
    server.stop()
    server_thread.join()


async def main():
    global app, gui, server_thread
    app = QApplication([])
    app.setStyle("Windows")
    gui = MainWindow()
    gui.show()
    gui.running = True
    await gui.intiface.config()
    asyncio.create_task(gui.intiface.create_client())
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    gui.print("HTTP listener started on port 80")
    asyncio.create_task(gui.intiface.contact_status())
    while gui.running:
        app.processEvents()
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
