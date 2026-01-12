# IUBAT Central Library Management System

A complete **full-stack Library Management System** built with Django, specially designed for **IUBAT Central Library**.

This project implements almost all major functionalities required in a modern university library — from admin book/user management to student borrowing, librarian operations, overdue notifications, and report generation.

**Project Status:** Fully functional locally — all CSV functionalities completed!

## 🎥 Project Showcase Video

https://github.com/user-attachments/assets/d889fd12-4ce6-4d09-ace4-ef46503b6faa

## ✨ All Implemented Features (from Requirement CSV)

| Functionality                          | Input                                                                                  | Output / Result                                      |
|----------------------------------------|----------------------------------------------------------------------------------------|------------------------------------------------------|
| **Admin Add the Book Information**     | Book Title, Cover Page, Category, Price, Description, Quantity                         | Confirmation MSG or Error MSG                        |
| **Click to add book to the Book List** | Add Button                                                                             | Confirmation MSG or Error MSG                        |
| **User/Admin Login**                   | Username/Email, Password, Role Selection                                               | Redirect to Dashboard or "Invalid Credentials" Error |
| **Search for Books**                   | Keywords (Title, Author, ISBN)                                                         | Filtered book list                                   |
| **Filter Book Results**                | Select Category or Availability Status                                                 | Updated/Narrowed Book List                           |
| **View Book Details**                  | Click on Book Title/Image                                                              | Display Full Details (Author, Location, etc.)        |
| **Request to Borrow Book (Student)**   | Click "Request Borrow" Button                                                          | "Request Pending" Notification or "Limit Reached" Error |
| **View User Dashboard**                | Click "My Dashboard"                                                                   | Shows Due Dates, Pending/Issued Books, Fines         |
| **Librarian Issue Book (Check-out)**   | Scan User ID, Scan Book Barcode                                                        | "Book Issued Successfully" MSG & Update Inventory    |
| **Return Book (Check-in)**             | Scan Book Barcode/Enter Book ID                                                        | "Return Successful" MSG & Update Inventory           |
| **View Borrowing History**             | Click "My History" Tab                                                                 | List of previously borrowed and returned items       |
| **Check Overdue Status**               | System Date Check (Automated) or Click "Overdue List"                                  | List of Users with overdue books and fine amounts    |
| **Admin Create User Account**          | Name, ID, Email, Role, Password                                                        | "Account Created Successfully" MSG                   |
| **Admin Update User Account**          | Select User, Edit Details (Role, Status)                                               | "User Details Updated" MSG                           |
| **Admin Delete User Account**          | Select User ID, Click Delete, Confirm                                                  | "User Deleted" MSG                                   |
| **Admin Configure Settings**           | Loan Duration Days, Fine Amount per Day                                                | "System Settings Saved" MSG                          |
| **Librarian Update Stock**             | Select Book, Enter New Quantity                                                        | "Stock Updated" MSG                                  |
| **Send Overdue Notification**          | Select User or Click "Send All Reminders"                                              | Email/System Notification sent to User               |
| **Generate Library Report**            | Select Date Range, Report Type (Borrowing/Stock)                                       | Downloadable Excel File                              |
| **Logout**                             | Click "Logout" Button                                                                  | Redirect to Login Page                               |

## 🖼️ Screenshots

###  Homepage – Book Cards with Search & Filter
![Admin_Panel_Home](https://github.com/user-attachments/assets/7718709f-7702-4e44-9efe-bfcf8cc9bdc0)
###  Admin Add Book Form – Upload Cover, Details
![Admin_Panel_AddBook](https://github.com/user-attachments/assets/2a2037d1-d8e6-4042-8b37-85d6c81ddc2c)
###  Student Dashboard – Current & History Books
![Student_Panel_Dashboard](https://github.com/user-attachments/assets/871548d7-db0e-402c-8a4e-28af2bcf2911)

## 🛠️ Tech Stack

- **Backend** → Django 5.2.9  
- **Frontend** → Bootstrap 5.3 + Bootstrap Icons  
- **Database** → SQLite (development)  
- **File Handling** → Django ImageField (book covers)  
- **Reports** → openpyxl (Excel generation)  
- **Forms & Filters** → crispy-forms, django-filter  

## 🚀 Local Installation Guide (Step-by-Step)

```bash
# 1. Clone the repository
git clone https://github.com/Shamsun-Nahar-Nitu/iubat-library-management.git
cd iubat-library-management

# 2. Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts: username (e.g. admin_nitu), email, password

# 6. Run the development server
python manage.py runserver

Open browser → http://127.0.0.1:8000/
📂 Project Structure Overview
iubat_library_project/
├── iubat_library/          # Project settings, urls, wsgi
├── users/                  # Custom user, login, dashboard, admin tools
├── books/                  # Book model, home page, add book
├── borrowing/              # Borrow request, issue/return, reports, notifications
├── templates/              # All HTML templates (organized by app)
├── static/                 # CSS, JS, images (logo)
├── media/                  # Uploaded book covers (book_covers/)
├── manage.py
├── requirements.txt
└── README.md

Acknowledgments & Notes
This project was a complete learning journey — handling custom user roles, file uploads, permissions, real-time calculations, and beautiful UI design.
Special thanks to Django documentation, Bootstrap community, Stack Overflow, and every late-night debugging session 💻
© 2026 Shamsun Nahar Nitu
Feedback & suggestions are always welcome 🚀



