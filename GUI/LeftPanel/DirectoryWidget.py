from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox
import DIContainer, os
from PySide6.QtCore import Qt
from Utilities import MiscFunctions


class DirectoryWidget(QWidget):

    def __init__(self):
        super().__init__()
        # Elements
        self.datasetFolderLabel = QLabel("Dataset directory")
        self.pathLineEdit = QLineEdit(DIContainer.working_directory)
        self.browseButton = QPushButton("Browse")
        self.filesLabel = QLabel("Invalid path")

        # Styling
        self.datasetFolderLabel.setAlignment(Qt.AlignHCenter)

        # Finishing layout
        self.widgetLayout = QVBoxLayout()
        self.widgetLayout.addWidget(self.datasetFolderLabel)
        self.widgetLayout.addWidget(self.pathLineEdit)
        self.widgetLayout.addWidget(self.browseButton)
        self.widgetLayout.addWidget(self.filesLabel)
        self.setLayout(self.widgetLayout)

        self.on_path_chosen()
        self.setup()

    def setup(self):
        self.browseButton.clicked.connect(lambda x: self.on_browse_button())
        self.pathLineEdit.textChanged.connect(lambda x: self.on_path_chosen())

    def on_browse_button(self):
        directory = QFileDialog.getExistingDirectory(dir=DIContainer.working_directory)

        if directory == "":
            return
        else:
            self.pathLineEdit.setText(directory)
            self.on_path_chosen()

    def on_path_chosen(self):
        if os.path.isdir(self.pathLineEdit.text()):
            DIContainer.working_directory = self.pathLineEdit.text()
            length = MiscFunctions.get_dataset_length(self.pathLineEdit.text())
            self.update_files_label(length)
        else:
            self.filesLabel.setText("Invalid path")

    def update_files_label(self, images_count: int):
        formatted_count = MiscFunctions.format_number_string(images_count)
        self.filesLabel.setText("Directory contains " + formatted_count + " files")
