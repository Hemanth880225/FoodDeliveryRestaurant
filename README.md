# 🍽️ FoodDeliveryRestaurant — Flask Restaurant Ordering System

**FoodDeliveryRestaurant** is a **Flask-based restaurant food ordering web application** that allows users to browse menu items, view food images, and place orders through a clean and responsive interface.

This project demonstrates **full-stack web development fundamentals** including backend routing, database integration, template rendering, and UI design.

---

# 🚀 Project Overview

FoodDeliveryRestaurant is designed to simulate a **basic restaurant ordering system** where users can:

* Browse food menu
* View food images
* Place food orders
* Navigate through a responsive UI

This project focuses on **clean architecture**, **Flask fundamentals**, and **database integration**.

---

# 🏗️ High-Level Architecture

```
┌──────────────────────────────────────────────┐
│                 Client Layer                 │
│----------------------------------------------│
│ Browser (User Interface)                     │
└─────────────────────┬────────────────────────┘
                      │ HTTP Request
                      ▼
┌──────────────────────────────────────────────┐
│                 Flask App                    │
│----------------------------------------------│
│ routes.py                                   │
│                                              │
│ Responsibilities                             │
│ • Handle user requests                       │
│ • Render templates                           │
│ • Process orders                             │
└─────────────────────┬────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│               Template Layer                 │
│----------------------------------------------│
│ Jinja2 Templates                             │
│                                              │
│ • HTML Pages                                 │
│ • Dynamic Rendering                          │
└─────────────────────┬────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│               Data Layer                     │
│----------------------------------------------│
│ SQLite Database                              │
│ SQLAlchemy Models                            │
│ JSON Menu Data                               │
└──────────────────────────────────────────────┘
```

---

# ⚙️ Tech Stack

## Backend

* Python
* Flask
* SQLAlchemy

## Frontend

* HTML
* CSS
* Bootstrap
* Jinja2 Templates

## Database

* SQLite
* SQLAlchemy ORM

## Tools

* Git
* GitHub
* JSON (Menu Data)

---

# ✨ Features

## Menu System

* Browse food items
* View food images
* Display pricing
* Clean layout

---

## Ordering System

* Place orders
* Simple UI
* Dynamic rendering

---

## UI Features

* Responsive design
* Bootstrap styling
* Clean navigation

---

# 📂 Project Structure

```
FoodDeliveryRestaurant
│
├── static/            # CSS, Images, JS
├── templates/         # HTML Templates
├── models.py          # Database Models
├── routes.py          # Flask Routes
├── run.py             # Entry Point
└── items.json         # Menu Data
```

---

# 🧠 Application Flow

```
User visits website
        ↓
Browse Menu
        ↓
Select Food Item
        ↓
Place Order
        ↓
Render Response
```

---

# 🗄️ Database Design

## Food Item Model

| Field       | Type    |
| ----------- | ------- |
| id          | Integer |
| name        | String  |
| price       | Float   |
| image       | String  |
| description | String  |

---

# 🚀 Installation

Clone Repository

```
git clone https://github.com/Hemanth880225/FoodDeliveryRestaurant.git
```

Navigate to Project

```
cd FoodDeliveryRestaurant
```

Create Virtual Environment

```
python -m venv .venv
```

Activate Environment

Windows

```
.venv\Scripts\activate
```

Install Dependencies

```
pip install -r requirements.txt
```

Run Application

```
python run.py
```

Open in Browser

```
http://127.0.0.1:5000
```

---

# 🧪 Learning Outcomes

This project demonstrates:

* Flask fundamentals
* Template rendering
* Database integration
* MVC architecture basics
* Full-stack web development basics

---

# ⭐ Resume Description

**FoodDeliveryRestaurant — Flask Web Application**
Built a restaurant food ordering web application using Flask with dynamic menu rendering, SQLite database integration, and responsive UI using Bootstrap. Implemented routing, template rendering, and clean project structure.

---

# 🔮 Future Improvements

* User authentication
* Cart system
* Order history
* Payment integration
* Admin dashboard
* REST API conversion

---

# 👨‍💻 Author

Hemanth
Python | Flask | Backend Development

---

# 📄 License

MIT License
