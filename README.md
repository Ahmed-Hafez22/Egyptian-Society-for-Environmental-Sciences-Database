# Egyptian Society for Environmental Sciences Database  

A Python + SQLAlchemy + SQLite project designed to manage and organize the database of the **Egyptian Society for Environmental Sciences**.  
The project provides both a **Graphical User Interface (GUI)** and a **FastAPI-powered RESTful API**, making it accessible for end-users and developers.  

---

## 📂 Project Structure
- **`API.py`** – FastAPI application with REST endpoints.  
- **`DB.py`** – SQLAlchemy database setup and connection handling.  
- **`Functions.py`** – Core project functions and utilities.  
- **`GUI.py`** – Graphical interface for interacting with the database.  
- **`libraries.py`** – Required libraries and helper modules.  
- **`schemas.py`** – SQLAlchemy models and Pydantic schemas used by the API.  
- **`ESES.db`** – SQLite database file storing persistent data.  

---

## 🚀 Getting Started  

### Prerequisites  
Make sure you have installed:  
- [Python 3.8+](https://www.python.org/downloads/)  
- SQLite3 (comes pre-installed with Python).  

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

---

## ▶️ Running the Project  

### Run the GUI  
```bash
python GUI.py
```  

### Run the API  
```bash
uvicorn API:app --reload
```  

Default API URL: `http://127.0.0.1:8000/`  

Interactive API docs available at:  
- Swagger UI → `http://127.0.0.1:8000/docs`  
- ReDoc → `http://127.0.0.1:8000/redoc`  

---

## 📦 Features  
- SQLAlchemy-powered ORM for database interactions.  
- Centralized SQLite database (`ESES.db`).  
- Easy-to-use **GUI** for data entry, updates, and queries.  
- **FastAPI REST API** with automatic interactive docs.  
- **Schemas** for validating API requests and responses.  
- Modular project structure for maintainability and scalability.  

---

## 🛠 Technologies Used  
- **Python 3**  
- **SQLite3** (database backend)  
- **SQLAlchemy** (ORM)  
- **Tkinter** (GUI)  
- **FastAPI** (API)  

Badges (optional):  
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)  
![SQLite](https://img.shields.io/badge/Database-SQLite3-green.svg)  
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)  
![GUI](https://img.shields.io/badge/Interface-Tkinter-orange.svg)  
![API](https://img.shields.io/badge/API-FastAPI-blue.svg)  

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
