import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        # calling parent constructor to correctly instantiate an instance of
        # my class
        super().__init__()
        self.setWindowTitle("Age Calculator")

        # creating grid
        grid = QGridLayout()

        # labels for grid
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_birth_label = QLabel("Date of Birth (MM/DD/YYYY):")
        self.date_birth_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # adding labels as elements to my grid
        # setting up my window with elements
        # addWidget(widget, row, column, rowSpan, columnSpan)
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_birth_label, 1, 0)
        grid.addWidget(self.date_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        # setting layout using my grid
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.today().year
        date_of_birth = self.date_birth_line_edit.text()
        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y").date().year
        age = current_year - int(year_of_birth)
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")

# creating my application instance
app = QApplication(sys.argv)
# that is my window inherited from QWidget class
age_calculator = AgeCalculator()
age_calculator.show()

#run the app
sys.exit(app.exec())
