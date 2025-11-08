import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, \
    QStatusBar, QLabel, QGridLayout, QMessageBox, QHeaderView

# -------------------------
# Custom Exception for DB
# -------------------------
class DatabaseError(Exception):
    """Custom exception for db-related errors"""
    pass

# -------------------------
# Database Connection Wrapper
# -------------------------
class DatabaseConnection:
    """Handles SQLite connection and queries"""
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def query(self, sql, params=(), fetch=False):
        """Execute SQL query with optional fetch; raise DatabaseError on failure"""
        try:
            with sqlite3.connect(self.database_file) as connection:
                cursor = connection.cursor()
                cursor.execute(sql, params)
                if fetch:
                    return cursor.fetchall()
                connection.commit()
                return None
        except sqlite3.Error as error:
            raise DatabaseError(f"Database Error: {error}")

# -------------------------
# Main Application Window
# -------------------------
class MainWindow(QMainWindow):
    """Main GUI window for student management"""
    instance = None  # Class-level reference for dialogs to access main window

    def __init__(self):
        super().__init__(parent=None)
        MainWindow.instance = self
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(800)
        self.setFixedHeight(500)

        # -------------------------
        # Menu Bar Setup
        # -------------------------
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add Student action
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # About action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        # Search action
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # -------------------------
        # Table Setup
        # -------------------------
        self.table = QTableWidget(parent=None)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Appearance and UX
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: #f2f2f2; background-color: #ffffff;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setToolTip("Click a row to select a student")

        # Header styling
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            "background-color: #4CAF50;"  # green header background
            "color: white;"  # text color
            "font-weight: bold;"  # bold text
            "font-size: 14px;"
            "}"
        )

        # -------------------------
        # Toolbar Setup
        # -------------------------
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # -------------------------
        # Status Bar Setup
        # -------------------------
        self.statusBar = QStatusBar(parent=None)
        self.setStatusBar(self.statusBar)

        # Connect table click to handler
        self.table.cellClicked.connect(self.cell_clicked)

    # -------------------------
    # Handle table row click
    # -------------------------
    def cell_clicked(self, row):
        student_id = self.table.item(row, 0).text()

        # Create Edit and Delete buttons dynamically
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(lambda _, s=student_id: self.open_edit_dialog(s))
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(lambda _, s=student_id: self.open_delete_dialog(s))

        edit_button.setToolTip("Edit the selected student")
        delete_button.setToolTip("Delete the selected student")

        # Remove previous buttons from status bar
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)

    # -------------------------
    # Load data from database into table
    # -------------------------
    def load_data(self):
        connection = DatabaseConnection()
        result = connection.query("SELECT * FROM students", fetch=True)
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_number, column_number, item)

    # -------------------------
    # Open dialogs
    # -------------------------
    def open_edit_dialog(self, sid):
        MainWindow.edit(sid)
        self.load_data()

    def open_delete_dialog(self, sid):
        MainWindow.delete(sid)
        self.load_data()

    # -------------------------
    # Static utility methods for menus
    # -------------------------
    @staticmethod
    def insert():
        """Open InsertDialog"""
        dialog = InsertDialog()
        dialog.exec()

    @staticmethod
    def search():
        """Open SearchDialog"""
        dialog = SearchDialog()
        dialog.exec()

    @staticmethod
    def edit(sid):
        """Open EditDialog"""
        dialog = EditDialog(sid)
        dialog.exec()

    @staticmethod
    def delete(sid):
        """Open DeleteDialog"""
        dialog = DeleteDialog(sid)
        dialog.exec()

    @staticmethod
    def about():
        """Open AboutDialog"""
        dialog = AboutDialogMessage()
        dialog.exec()

# -------------------------
# About Dialog
# -------------------------
class AboutDialogMessage(QMessageBox):
    """Shows information about the application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        Created for a University Python course, this app showcases key Python skills
        including database handling, object-oriented programming, and building
        intuitive GUIs with PyQt6.
        """
        self.setText(content)

# -------------------------
# Edit Student Dialog
# -------------------------
class EditDialog(QDialog):
    """Dialog for editing a student's data"""
    def __init__(self, sid):
        super().__init__(parent=None)
        self.student_id = sid
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Load student data
        try:
            connection = DatabaseConnection()
            result = connection.query(
                "SELECT name, course, mobile FROM students WHERE id = ?",
                (sid,), fetch=True
            )
            if not result:
                QMessageBox.critical(self, "Error", "Student not found.")
                self.close()
                return
            name, course, mobile = map(str, result[0])

            # Input fields
            self.student_name = QLineEdit(name)
            self.student_name.setPlaceholderText("Name")
            layout.addWidget(self.student_name)

            self.course_name = QComboBox(parent=None)
            courses = ["Biology", "Math", "Astronomy", "Physics"]
            self.course_name.addItems(courses)
            self.course_name.setCurrentText(course)
            layout.addWidget(self.course_name)

            self.mobile = QLineEdit(mobile)
            self.mobile.setPlaceholderText("Mobile")
            layout.addWidget(self.mobile)

        except DatabaseError as e:
            QMessageBox.critical(self, "Database Error", str(e))
            self.close()
            return

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(lambda _, s=sid: self.update_student(s))
        layout.addWidget(button)

        self.setLayout(layout)

    # -------------------------
    # Update student in DB
    # -------------------------
    def update_student(self, sid):
        if not self.student_name.text().strip() or not self.mobile.text().strip():
            QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")
            return

        try:
            connection = DatabaseConnection()
            connection.query(
                "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                (self.student_name.text(), self.course_name.currentText(),
                 self.mobile.text(), sid)
            )
            MainWindow.instance.load_data()
            QMessageBox.information(None, "Success", "Student updated successfully.")
            self.close()
        except DatabaseError as e:
            QMessageBox.critical(None, "Database Error", str(e))

# -------------------------
# Delete Student Dialog
# -------------------------
class DeleteDialog(QDialog):
    """Dialog to confirm and delete a student"""
    def __init__(self, sid):
        super().__init__(parent=None)
        self.sid = sid
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout(parent=None)
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        # Connect buttons
        yes.clicked.connect(lambda _, s=sid: self.delete_student(s))

    # Delete student from DB
    def delete_student(self, sid):
        try:
            connection = DatabaseConnection()
            connection.query("DELETE FROM students WHERE id = ?", (sid,))
            MainWindow.instance.load_data()
            confirmation_widget = QMessageBox()
            confirmation_widget.setText("The record was deleted successfully")
            confirmation_widget.exec()
            self.close()
        except DatabaseError as e:
            QMessageBox.critical(None, "Database Error", str(e))

# -------------------------
# Insert Student Dialog
# -------------------------
class InsertDialog(QDialog):
    """Dialog to insert a new student"""
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Input fields
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox(parent=None)
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    # Add new student to DB
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        if not name or not mobile:
            QMessageBox.information(None, "Warning", "Please enter your name and mobile")
            return

        try:
            connection = DatabaseConnection()
            connection.query(
                "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                (name, course, mobile)
            )
            MainWindow.instance.load_data()
            QMessageBox.information(None, "Success", "Student added successfully")
            self.close()
        except DatabaseError as e:
            QMessageBox.information(None, "Database Error", str(e))

# -------------------------
# Search Dialog
# -------------------------
class SearchDialog(QDialog):
    """Dialog to search students by name"""
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Search Student")
        layout = QVBoxLayout()

        self.searched_student_name = QLineEdit()
        self.searched_student_name.setPlaceholderText("Name")
        layout.addWidget(self.searched_student_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)

    # Search student in DB and highlight in table
    def search_student(self):
        name = self.searched_student_name.text()
        if not name:
            QMessageBox.warning(self, "Missing Info", "Please enter the name.")
            return
        try:
            connection = DatabaseConnection()
            result = connection.query("SELECT * FROM students WHERE name = ?", (name,), fetch=True)
            rows = list(result)
            print(rows)

            MainWindow.instance.table.clearSelection()

            items = MainWindow.instance.table.findItems(name, Qt.MatchFlag.MatchFixedString)
            if items:
                for item in items:
                    print(item)
                    MainWindow.instance.table.item(item.row(), 1).setSelected(True)
                    MainWindow.instance.table.scrollToItem(item)
                self.close()
            else:
                QMessageBox.information(None, "Info", "Student not found")
                print("Not found")
        except DatabaseError as e:
            QMessageBox.critical( None, "Database Error", str(e))

# -------------------------
# Application Entry Point
# -------------------------
app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())