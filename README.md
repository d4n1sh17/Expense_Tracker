# Personal Expense Tracker (Flask + SQLite)

A simple full-stack web application for tracking personal expenses.  
The project demonstrates backend development using **Flask**, **SQLite**, and **Jinja2 templates** with complete CRUD functionality.

This project was developed as part of a Full Stack Web Development assessment to demonstrate frontend–backend integration and database-driven application development.

---

## Features

- Add new expenses
- View all recorded expenses
- Edit existing expenses
- Delete expenses
- Input validation for form data
- Dashboard statistics (total spending, number of entries, latest expense date)
- SQLite database storage
- Clean responsive UI built with HTML + CSS
- Flash messages for success and error handling

---

## Tech Stack

Backend
- Python
- Flask

Frontend
- HTML
- CSS
- Jinja2 Templates

Database
- SQLite

---

## Project Structure


expense-tracker/
│
├── app.py
├── expenses.db
│
├── templates/
│ ├── index.html
│ ├── add_expense.html
│ └── edit_expense.html


---

## Database Structure

The application uses a single table called **expenses**.

| Column | Type | Description |
|------|------|------|
| id | INTEGER | Primary Key |
| title | TEXT | Expense title |
| category | TEXT | Expense category |
| amount | REAL | Expense amount |
| expense_date | TEXT | Date of expense |

The table is automatically created when the application runs for the first time.

---

## Application Workflow

1. User opens the dashboard.
2. The Flask backend retrieves expense data from SQLite.
3. Expenses are displayed using Jinja2 templates.
4. User can:
   - Add a new expense
   - Edit an existing expense
   - Delete an expense
5. Form inputs are validated before database operations.
6. The database updates and the dashboard refreshes.

---

## CRUD Operations

### Create
Add a new expense through the **Add Expense** form.

### Read
View all expenses on the dashboard.

### Update
Edit existing expense details.

### Delete
Remove an expense from the database.

---

## Running the Project

### 1 Install Dependencies


pip install flask


### 2 Navigate to Project Folder


cd expense-tracker


### 3 Run the Application


python app.py


### 4 Open in Browser


http://127.0.0.1:5000


---

## Learning Outcomes

This project demonstrates:

- Flask routing and application structure
- Database connectivity with SQLite
- Server-side validation
- CRUD operations with SQL
- Template rendering using Jinja2
- Frontend and backend integration

---

## Future Improvements

- User authentication system
- Expense category analytics
- Monthly expense reports
- Data visualization using charts
- REST API integration
- Cloud deployment


