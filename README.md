# 🎬 MovieTracker

MovieTracker is a Flask-based web application that allows users to search, select, and save movies to their personal watchlist. It integrates a MySQL movie database for movie information and uses AWS DynamoDB to manage user accounts and watchlists.

---

## 📌 Project Summary

MovieTracker enables users to:
- Sign up and log in securely
- Browse and search through a list of movies
- Add selected movies to a personal watchlist
- View and manage (remove) items in the watchlist

It uses a combination of relational (MySQL) and non-relational (DynamoDB) databases to provide a flexible and scalable experience.

---

## 🛠 Technologies Used

- **Flask** – Python web framework
- **MySQL** – Stores movie metadata (ID, title, overview, etc.)
- **AWS DynamoDB** – Stores user data and watchlists
- **Select2.js** – Enhanced dropdown search UI
- **Bootstrap 3** – Front-end layout and styling
- **bcrypt** – Password hashing for secure login

---

## 🚀 Setup and Run Instructions

### 1. Clone the repository
```bash
git clone https://github.com/juanito2110/CS178Project1
cd CS178Project1
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate 
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure credentials
```bash
# creds.py
host = 'your-mysql-host'
user = 'your-mysql-username'
password = 'your-mysql-password'
db = 'your-database-name'
```

### 5. Run the application
```bash
python flaskapp.py
```

