import summarizer_tool as summarizer
import os

class Controller:
    def __init__(self,view):
        self.view = view
        self.connect_signals()


    def connect_signals(self):
        self.view.input_combobox.currentIndexChanged.connect(self.handle_input_combobox)
        self.view.select_file_button.clicked.connect(self.handle_select_file_button)
        self.view.summarize_button.clicked.connect(self.handle_summarize_button)
        self.view.copy_button.clicked.connect(self.handle_copy_button)
        self.view.save_button.clicked.connect(self.handle_save_button)


    def handle_input_combobox(self):
        self.view.update_text_box_placeholder(self.view.input_combobox.currentText())


    def handle_select_file_button(self):
        self.view.update_text_box_input(self.view.generate_file_dialog())
                

    def handle_summarize_button(self):
        # Collect necessary parameter data: type of input, input, format of response
        input_type = self.view.input_combobox.currentText()
        input = self.view.text_box.toPlainText()
        format = self.view.format_combobox.currentText()

        # Summarize data/display error messages
        if input == "" or input == None:
            self.view.generate_message_dialog("Input Field Error", input_type + " field must be filled.")
        elif input_type == "File" and "\"" in input:
            self.view.update_summary(input_type, input[1:-1], format) 
        else:
            self.view.update_summary(input_type, input, format)


    def handle_copy_button(self):
        # Copy all summarized text to clipboard
        self.view.summary_box.selectAll()
        self.view.summary_box.copy()
        self.view.clear_selection(self.view.summary_box)
        

    def handle_save_button(self):
        file_path = self.view.generate_file_dialog()

        # Ask user if they want to overwrite existing file
        try:
            if os.path.exists(file_path):
                decision = self.view.generate_question_dialog("Overwrite Confirmation", "Overwrite existing file?")
                if (decision == 0):
                    return
                elif (decision == 1):
                    mode = "w"
                else:
                    mode = "a"
            else:
                mode = "w"
        except:
            return
        
        # Write summarized text to file/display error messages
        file_extension = os.path.splitext(file_path)[1]
        formatted_file_types = [".html", ".htm", ".rtf"]
        if file_extension in formatted_file_types:
            if summarizer.write_to_file(file_path,self.view.summary_box.toHtml(), mode) == "Unable to write to file.":
                self.view.generate_message_dialog("Save Error", "Unable to write to file.")
        elif file_extension == ".txt": 
            if summarizer.write_to_file(file_path,self.view.summary_box.toPlainText(), mode) == "Unable to write to file.":
                self.view.generate_message_dialog("Save Error", "Unable to write to file.")
        else:
            self.view.generate_message_dialog("File Type Error", "Only the following extensions are acceptable: .html, .htm, .rtf, .txt")
   