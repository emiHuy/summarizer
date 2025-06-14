from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QTextEdit, QLabel, QComboBox, QPushButton , QMessageBox, QFileDialog
from PySide6.QtCore import QSize
from PySide6 import QtGui
from PySide6.QtGui import QIcon
import summarizer_tool as summarizer
from utils import resource_path

class MainWindow(QMainWindow):   

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Summarizer Tool")
        self.setFixedSize(QSize(1000,720))
        self.setWindowIcon(QIcon(resource_path("images/summarizer-icon.png")))
        self.setup_components()

        layout = QGridLayout()        
        # left side (text input)
        layout.addWidget(self.input_label,0,0)
        layout.addWidget(self.input_combobox,0,1)
        layout.addWidget(self.select_file_button,0,2)
        layout.addWidget(self.text_box,1,0,1,5)
        layout.addWidget(self.summarize_button,2,0,1,2)
        # right side (summary)
        layout.addWidget(self.format_label,0,5)
        layout.addWidget(self.format_combobox,0,6)
        layout.addWidget(self.summary_box,1,5,1,7)
        layout.addWidget(self.copy_button,2,10)
        layout.addWidget(self.save_button,2,11)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def setup_components(self):
        # LEFT SIDE ------------------------
        self.input_label = QLabel("Input Type:")
        self.input_label.setFixedWidth(60)

        # Combobox for text input types
        self.input_combobox = QComboBox()
        self.input_combobox.addItems(["Text", "Url", "File"])

        # Button for file selector
        self.select_file_button = QPushButton("Select File")
        self.select_file_button.setVisible(False)

        # TextEdit for displaying input
        self.text_box = QTextEdit() 
        self.text_box.setPlaceholderText("Enter text here...")
        self.text_box.setAcceptRichText(False)
        
        # Button to summarize the given text
        self.summarize_button = QPushButton("Summarize")
        self.summarize_button.setFixedWidth(80)

        # RIGHT SIDE ------------------------
        self.format_label = QLabel("Format:")
        self.format_label.setFixedWidth(42)

        # Combobox for response format
        self.format_combobox = QComboBox()
        self.format_combobox.addItems(["Bullet points", "Notes", "TL;DR", "Sentences"])

        # TextEdit for displaying summary
        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)

        # Post-summary buttons for copying text and saving text to a file
        self.copy_button = QPushButton("Copy Text")
        self.copy_button.setFixedWidth(80)
        self.save_button = QPushButton("Save To File")
        self.save_button.setFixedWidth(100)


    def update_text_box_placeholder(self, input_type):
        match input_type:
            case "Text":
                self.text_box.setPlaceholderText("Enter text here...")
                self.select_file_button.setVisible(False)
            case "Url":
                self.text_box.setPlaceholderText("Enter url here...")
                self.select_file_button.setVisible(False)
            case "File": 
                self.text_box.setPlaceholderText("Enter file path here...")
                self.select_file_button.setVisible(True)
    

    def update_text_box_input(self, text):
        self.text_box.setText(text)


    def update_summary(self, input_type, input, format):
        match input_type:
            case "Text": 
                self.summary_box.setHtml(summarizer.summarize(format,input))
            case "Url":
                self.summary_box.setHtml(summarizer.summarize_url(format,input))
            case "File":
                self.summary_box.setHtml(summarizer.summarize_file(format,input))


    def generate_message_dialog(self, title, message):
        message_dlg = QMessageBox(self)
        message_dlg.setWindowTitle(title)
        message_dlg.setWindowIcon(QtGui.QIcon.fromTheme("dialog-information"))
        message_dlg.setText(message)
        message_dlg.setIcon(QMessageBox.Information)
        if message_dlg.exec():
            pass


    def generate_file_dialog(self):
        file_filter = "All files (*.txt *.html *.htm *.rtf);;Text files (*.txt);;HTML files (*.html *.htm);;Rich Text Format (*.rtf)"
        file_dlg = QFileDialog(self)
        file_dlg.setWindowTitle("Save To File")
        file_dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dlg.setNameFilter(file_filter)
        file_dlg.setViewMode(QFileDialog.ViewMode.Detail)
        if file_dlg.exec():
            return file_dlg.selectedFiles()[0]
        
        
    def generate_question_dialog(self, title, message):
        decision = QMessageBox.question(self, title, message)
        if decision == QMessageBox.StandardButton.Yes:
            return 1
        elif decision == QMessageBox.StandardButton.No:
            return -1
        else: 
            return 0
    

    def clear_selection(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.clearSelection()
        text_edit.setTextCursor(cursor)
