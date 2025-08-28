# Egyptian Society for Environmental Sciences Database

A Python + SQLite3 project designed to manage and organize the database of the **Egyptian Society for Environmental Sciences**.  
It provides functionality for handling data operations, database queries, and modular Python scripts in a structured way.  

---

## 📂 Project Structure
- **`Database.py`** – Handles SQLite3 database setup and connections.  
- **`Functions.py`** – Core project functions and utilities.  
- **`libraries.py`** – Required libraries and helper modules.  
- **`main.py`** – Entry point to run the application.  

---

## 🚀 Getting Started

### Prerequisites
Make sure you have installed:  
- [Python 3.8+](https://www.python.org/downloads/)  
- SQLite3 (comes pre-installed with Python, but you can also install separately).  

### Installation
Clone the repository:
```bash
git clone https://github.com/Ahmed-Hafez22/Egyptian-Society-for-Environmental-Sciences-Database.git
cd Egyptian-Society-for-Environmental-Sciences-Database
```

Install dependencies:
```bash
pip install -r requirements.txt
```

*(If you don’t have a `requirements.txt`, create one by running `pip freeze > requirements.txt` after installing your packages.)*

### Running the Project
Run the main file:
```bash
python main.py
```

---

## 📦 Features
- Centralized SQLite3 database management system.  
- SQL queries for storing and retrieving member data.  
- Python functions for data operations.  
- Organized modular Python structure.  
- Easy to extend and maintain.  

---

## 🛠 Technologies Used
- **Python 3**  
- **SQLite3 (SQL)**  

Badges (optional):  
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)  
![SQLite](https://img.shields.io/badge/Database-SQLite3-green.svg)  

---

## 🗄 Database Schema

The database schema is defined in [Database.py`](Database.py).  
You can initialize the database by running:

```bash
sqlite3 society.db < Database.py
```

This will create the necessary tables (e.g., `Members`, `Activities`, etc.) for the project.  

---

## 🤝 Contributing
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-branch`)  
3. Commit changes (`git commit -m "Add feature"`)  
4. Push to the branch (`git push origin feature-branch`)  
5. Open a Pull Request  

---

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  
