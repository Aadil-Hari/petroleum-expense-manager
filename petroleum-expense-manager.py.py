import mysql.connector
from datetime import datetime
import calendar

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",            
    password="",  
    database="petrol_expense"
)

# Month → Unique Code mapping
month_letters = {
    1: "JA", 2: "F", 3: "M", 4: "A", 5: "MA", 6: "JN",
    7: "JL", 8: "AU", 9: "S", 10: "O", 11: "N", 12: "D"
}

# Signup
def signup():
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()
    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username='%s'" % username)
    if cur.fetchone():
        print("Username already exists.")
    else:
        cur.execute("INSERT INTO users VALUES ('%s','%s','%s','%s')" % (username, password, name, email))
        db.commit()
        print("Signup successful.")

# Login
def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password))
    user = cur.fetchone()
    if user:
        print("Login successful.")
        return username
    else:
        print("Invalid credentials.")
        return None

# Get user name
def get_name(username):
    cur = db.cursor()
    cur.execute("SELECT name FROM users WHERE username='%s'" % username)
    result = cur.fetchone()
    return result[0] if result else "Unknown"

# Add expense
def add_expense(user):
    try:
        date_str = input("Date (YYYY-MM-DD): ").strip()
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        litres = float(input("Fuel quantity (litres): "))
        price = float(input("Fuel price per litre: "))
        amount = litres * price
        desc = input("Description (optional): ").strip()

        name = get_name(user)
        month_code = month_letters[date.month]

        cur = db.cursor()
        # Global ID (not per user anymore)
        cur.execute("SELECT id FROM expenses WHERE id LIKE '%s%%' ORDER BY id DESC LIMIT 1" % month_code)
        last = cur.fetchone()

        if last:
            last_num = int(last[0][len(month_code):])  # remove month code, keep number
            new_num = last_num + 1
        else:
            new_num = 1

        expense_id = month_code + str(new_num).zfill(3)  # e.g. JN001, JL002

        cur.execute("INSERT INTO expenses (id,username,name,date,litres,price_per_litre,amount,description) VALUES ('%s','%s','%s','%s',%f,%f,%f,'%s')" %
                    (expense_id, user, name, date, litres, price, amount, desc))
        db.commit()
        print("Expense added with ID:", expense_id)
    except Exception as e:
        print("Error:", e)

# View all expenses (shared, only name shown)
def view_expenses(month=None):
    cur = db.cursor()
    if month:
        cur.execute("SELECT id,name,date,litres,price_per_litre,amount,description FROM expenses WHERE MONTH(date)=%d ORDER BY date" % month)
    else:
        cur.execute("SELECT id,name,date,litres,price_per_litre,amount,description FROM expenses ORDER BY date")

    rows = cur.fetchall()
    if not rows:
        print("No records found.")
        return

    print(f"\n{'ID':<6} {'Date':<12} {'Litres':<8} {'Price':<8} {'Amount':<10} {'Name':<15} Description")
    print("-" * 95)
    for r in rows:
        print(f"{r[0]:<6} {r[2]}  {r[3]:<8.2f} {r[4]:<8.2f} {r[5]:<10.2f} {r[1]:<15} {r[6]}")

# Delete expense
def delete_expense():
    view_expenses()
    expense_id = input("Enter the ID of the expense to delete (e.g., JN001): ").strip()
    try:
        cur = db.cursor()
        cur.execute("DELETE FROM expenses WHERE id='%s'" % expense_id)
        db.commit()
        if cur.rowcount > 0:
            print("Expense deleted.")
        else:
            print("No expense found with that ID.")
    except Exception as e:
        print("Error:", e)

# View all users sorted by name
def view_users_by_name():
    cur = db.cursor()
    cur.execute("SELECT name, email FROM users ORDER BY name")
    rows = cur.fetchall()
    print(f"\n{'Name':<20} {'Email'}")
    print("-" * 50)
    for r in rows:
        print(f"{r[0]:<20} {r[1]}")

# Main program
def main():
    print("1. Login\n2. Signup")
    choice = input("Choose: ").strip()
    user = None
    if choice == "1":
        user = login()
    elif choice == "2":
        signup()
        user = login()
    else:
        print("Invalid option.")
        return

    if not user:
        return

    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. View Monthly Expenses")
        print("4. Delete an Expense")
        print("5. View All Users (Sorted by Name)")
        print("6. Exit")
        action = input("Select: ").strip()

        if action == "1":
            add_expense(user)
        elif action == "2":
            view_expenses()
        elif action == "3":
            month_name = input("Enter month name (e.g., July): ").capitalize()
            if month_name in calendar.month_name:
                month_num = list(calendar.month_name).index(month_name)
                view_expenses(month_num)
            else:
                print("Invalid month.")
        elif action == "4":
            delete_expense()
        elif action == "5":
            view_users_by_name()
        elif action == "6":
            print("Bye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
    db.close()
