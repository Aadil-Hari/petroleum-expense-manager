# Petroleum Expense Management System

A command-line application to track and manage fuel expenses, built with Python and MySQL. Originally developed as a Class 12 computer science project.

## Features

- **User authentication** — signup and login system backed by a MySQL users table
- **Add expenses** — log fuel purchases with date, litres, price per litre, and description; cost is calculated automatically
- **Custom expense IDs** — each expense gets a unique ID encoding the month it was logged (e.g., `JN001` for June, `JL002` for July), making records easy to identify chronologically
- **View expenses** — view all records, or filter by a specific month
- **Delete expenses** — remove a record by its ID
- **User directory** — view all registered users, sorted alphabetically by name

## Tech Stack

- **Language:** Python
- **Database:** MySQL
- **Library:** `mysql-connector-python`

## How It Works

1. On launch, the user either logs in or signs up.
2. Once authenticated, a menu lets the user add, view, filter, or delete expense records.
3. All data is stored in and retrieved from a MySQL database (`petrol_expense`), with two tables: `users` and `expenses`.

## Setup

1. Install the required library:
   ```
   pip install mysql-connector-python
   ```
2. Create a MySQL database named `petrol_expense` with `users` and `expenses` tables.
3. Update the database connection details (host, user, password) in the script to match your local setup.
4. Run the script:
   ```
   python Computer_Project_with_SQL__SIMPLE_.py
   ```

## Notes

This was built as a school project to practice database design and Python-MySQL integration. Future improvements could include parameterized queries and password hashing for better security practices.
