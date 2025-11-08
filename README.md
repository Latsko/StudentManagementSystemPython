# 🏫 Student Management System (Python & PyQt6)

A **desktop application** for managing student records, built with **Python**, **PyQt6**, and **SQLite**.  
Designed for educational purposes and real-world usability in small student databases.

---

## ✨ Features

### ✅ Core Functionality
- **Add, Edit, Delete** student records
- **Search** students by name
- Automatic table updates after operations

### 🖥️ UI / UX Enhancements
- Responsive dialogs with automatic resizing
- Intuitive **tooltips** and **confirmation dialogs** for safer operations
- **Stylish table appearance**: alternating row colors, centered content, bold colored headers
- Toolbar and status bar integration for a professional look

### 🧩 Database Integration
- Uses **SQLite** for lightweight, local database storage
- Centralized `DatabaseConnection` class with custom error handling

### ⚙️ Code Quality
- **Wrapper functions** for repetitive operations
- **Magic methods** implemented for dialogs
- Demonstrates **polymorphism** in dialog classes
- Modular, clean architecture for maintainability

---

## 🛠️ Technologies Used
- Python 3.x
- PyQt6
- SQLite3

---

## 🚀 Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/Latsko/StudentManagementSystemPython.git
```
2. Install required packages:
```bash
pip install PyQt6
```
3. Run the app
```bash
python main.py

