# IUBAT Central Library Management System

A complete **full-stack Library Management System** built with Django, specially designed for **IUBAT Central Library**.

This project implements almost all major functionalities required in a modern university library — from admin book/user management to student borrowing, librarian operations, overdue notifications, and report generation.

**Project Status:** Fully functional locally — all CSV functionalities completed!

### 🎥 Project Showcase Video
https://github.com/user-attachments/assets/189a35b9-8cce-4d43-8bbc-47d99af433b8
### ✨ All Implemented Features (from Requirement CSV)

| # | Functionality                          | Input / Action                                                                 | Output / Result                                      |
|---|----------------------------------------|--------------------------------------------------------------------------------|------------------------------------------------------|
| 1 | **Admin Add Book**                     | Book Title, Cover Page, Category, Price, Description, Quantity                 | Success message + Book appears in list with cover   |
| 2 | **Admin Create/Update/Delete User**    | Username, Email, Role, Student ID (for students), Password                     | Confirmation message, user added/updated/deleted     |
| 3 | **User/Admin Login**                   | Username/Email + Password + Role selection                                     | Redirect to home/dashboard or "Invalid Credentials"  |
| 4 | **Search & Filter Books**              | Keywords (Title/Author/ISBN), Category filter                                  | Updated book list                                    |
| 5 | **View Book Details**                  | Click on book title or cover                                                   | Full details (author, description, availability)     |
| 6 | **Student Borrow Request**             | Click "Request Borrow" button on book card                                     | "Request Pending" or "Limit Reached" message         |
| 7 | **User Dashboard**                     | Click "My Dashboard"                                                           | Shows current/pending books, due dates, fines        |
| 8 | **Librarian Issue Book**               | Scan/Select user + book                                                        | "Book Issued Successfully" + inventory update        |
| 9 | **Librarian Return Book**              | Scan/Enter book ID                                                             | "Return Successful" + fine calculation if overdue    |
|10 | **Borrowing History**                  | Click "My History"                                                             | List of previously borrowed & returned books         |
|11 | **Overdue Status & Notification**      | Automated check or manual "Send All Reminders"                                 | List of overdue + email/console notifications        |
|12 | **Generate Library Report**            | Select date range + report type (Borrowing/Stock)                              | Downloadable Excel file                              |
|13 | **Logout**                             | Click "Logout" button                                                          | Redirect to login page                               |

### 🖼️ Screenshots

#####  Homepage – Book Cards with Search & Filter
![Admin_Panel_Home](https://github.com/user-attachments/assets/7718709f-7702-4e44-9efe-bfcf8cc9bdc0)
#####  Admin Add Book Form – Upload Cover, Details
![Admin_Panel_AddBook](https://github.com/user-attachments/assets/2a2037d1-d8e6-4042-8b37-85d6c81ddc2c)
#####  Student Dashboard – Current & History Books
![Student_Panel_Dashboard](https://github.com/user-attachments/assets/871548d7-db0e-402c-8a4e-28af2bcf2911)

### 🛠️ Tech Stack

- **Backend** → Django 5.2.9  
- **Frontend** → Bootstrap 5.3 + Bootstrap Icons  
- **Database** → SQLite (development)  
- **File Handling** → Django ImageField (book covers)  
- **Reports** → openpyxl (Excel generation)  
- **Forms & Filters** → crispy-forms, django-filter  

### 🚀 Local Installation Guide (Step-by-Step)

##### 🔹 1. Clone the repository
```bash
git clone https://github.com/Shamsun-Nahar-Nitu/iubat-library-management.git
cd iubat-library-management
```
##### 🔹 2. Create & activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```
##### 🔹 3. Install all dependencies
```bash
pip install -r requirements.txt
```
##### 🔹 4. Apply database migrations
```bash
python manage.py migrate
```
##### 🔹 5. Create superuser (admin account)
```bash
python manage.py migrate
```
Follow prompts: username (e.g. admin_nitu), email, password

##### 🔹 6. Run the development server
```bash
python manage.py runserver
```
🌐 Open browser → http://127.0.0.1:8000/


### 📂 Project Structure Overview

```text
iubat_library_project/                  ← Project root folder 
│
├── db.sqlite3                          ← Local SQLite database (ignored in .gitignore)
├── manage.py                           ← Django management script
│
├── iubat_library/                      ← Main project package (settings, urls, wsgi, asgi)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                     ← All project settings (DEBUG, apps, media/static, etc.)
│   ├── urls.py                         ← Main URL routing (includes admin + app urls)
│   └── wsgi.py
│
├── static/                             ← Project-level static files (CSS, JS, images)
│   └── images/
│       └── iubat-logo.png              ← Logo used in header
│
├── media/                              ← Uploaded user files (book covers, etc.)
│   └── book_covers/                    ← Where cover_page images are saved
│
├── templates/                          ← Project-level templates
│   └── admin/                          ← Custom admin templates
│       └── base_site.html              
│
├── requirements.txt                    ← All Python dependencies
│
├── users/                              ← App: User management & authentication
│   ├── __init__.py
│   ├── admin.py                        ← Custom admin for CustomUser
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                       ← CustomUser model (role, student_id, etc.)
│   ├── views.py                        ← login, logout, dashboard, admin tools
│   ├── templates/
│   │   └── users/
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       ├── create_user.html
│   │       ├── update_user.html
│   │       └── delete_user.html
│   └── urls.py                        
│
├── books/                              ← App: Book & Category management
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                       ← Book & Category models
│   ├── views.py                        ← home, add_book
│   ├── templates/
│   │   └── books/
│   │       ├── home.html               ← Main book listing page
│   │       └── add_book.html           ← Admin add book form
│   └── urls.py                       
│
├── borrowing/                          ← App: Borrowing, issuing, returning, reports
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                       ← Borrowing model
│   ├── views.py                        ← borrow_request, issue_book, return_book,
│   │                                     update_stock, send_overdue_notification,
│   │                                     generate_report, etc.
│   ├── templates/
│   │   └── borrowing/
│   │       ├── issue_book.html
│   │       ├── return_book.html
│   │       ├── update_stock.html
│   │       ├── send_overdue_notification.html
│   │       └── generate_report.html
│   └── urls.py                         
│
├── venv/                               ← Virtual environment (ignored in .gitignore)
│
├── .gitignore                          ← Ignore venv, __pycache__, *.pyc, db.sqlite3, media/
└── README.md                           ← Project documentation
```
### Acknowledgments & Notes
This project was a complete learning journey — handling custom user roles, file uploads, permissions, real-time calculations, and beautiful UI design.
Special thanks to Django documentation, Bootstrap community, Stack Overflow, and every late-night debugging session 💻

© 2026 Shamsun Nahar Nitu  
Feedback & suggestions are always welcome 🚀
