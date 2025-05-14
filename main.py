import sys
from PySide6.QtWidgets import QApplication
import summarizer_view
import summarizer_controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = summarizer_view.MainWindow()
    controller = summarizer_controller.Controller(window)
    window.show()
    app.exec()