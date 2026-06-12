import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

def load_expenses():
    expenses = []
    if not os.path.exists(DATA_FILE):
        return expenses
    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses

def save_expenses(expenses):
    with open(DATA_FILE, "w", newline="") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)


def add_expense(expenses):
    print("\n--- Add New Expense ---")
    # Prompt for date, defaulting to today if left blank
    date = input("Date (YYYY-MM-DD, or press Enter for today): ").strip()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    category = input("Category (e.g., Food, Transport, Entertainment): ").strip()
    description = input("Description: ").strip()
    # Keep asking for amount until the user enters a valid number
    while True:
        amount_input = input("Amount: $")
        try:
            amount = float(amount_input)
            break
        except ValueError:
            print("Please enter a valid number.")
    # Store the expense as a dictionary
    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added: {description} - ${amount:.2f} [{category}]")

    total = sum(item["amount"] for item in expenses)
    print(f"{'Total:':<49} ${total:>7.2f}")


def view_expenses(expenses):
    print("\n--- All Expenses ---")
    # Handle empty list case
    if not expenses:
        print("No expenses recorded yet.")
        return
    # Print column headers with f-string alignment
    print(f"{'Date':<12} {'Category':<15} {'Description':<20} {'Amount':>8}")
    print("-" * 58)
    # Print each expense row
    for expense in expenses:
        print(
            f"{expense['date']:<12} {expense['category']:<15} "
            f"{expense['description']:<20} ${expense['amount']:>7.2f}"
        )
    # Print total at the bottom
    print("-" * 58)
    total = sum(expense["amount"] for expense in expenses)
    print(f"{'Total:':<49} ${total:>7.2f}")


def filter_by_category(expenses):
    print("\n--- Filter by Category ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    # Show available categories using a set comprehension
    categories = sorted(set(expense["category"] for expense in expenses))
    print("Available categories:", ", ".join(categories))
    choice = input("Enter category to filter: ").strip()
    # Filter with list comprehension and case-insensitive comparison
    filtered = [e for e in expenses if e["category"].lower() == choice.lower()]
    if not filtered:
        print(f"No expenses found in category '{choice}'.")
        return
    # Display filtered results
    print(f"\n{'Date':<12} {'Description':<20} {'Amount':>8}")
    print("-" * 43)
    for expense in filtered:
        print(
            f"{expense['date']:<12} {expense['description']:<20} "
            f"${expense['amount']:>7.2f}"
        )
    print("-" * 43)
    total = sum(expense["amount"] for expense in filtered)
    print(f"{'Total:':<34} ${total:>7.2f}")

def show_summary(expenses):
    print("\n--- Spending Summary ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    # Calculate overall statistics
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total expenses: ${total:.2f}")
    print(f"Number of transactions: {len(expenses)}")
    print(f"Average expense: ${total / len(expenses):.2f}")

    # Break down spending by category
    print("\nSpending by category:")
    categories = {}
    for expense in expenses:
        cat = expense["category"]
        categories[cat] = categories.get(cat, 0) + expense["amount"]
    # Sort by amount spent, highest first
    for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:<15} ${amount:>7.2f}")

def load_budget():
    # Return the saved budget as a float, or None if no budget is set
    if not os.path.exists(BUDGET_FILE):
        return None
    with open(BUDGET_FILE, "r") as file:
        try:
            return float(file.read().strip())
        except ValueError:
            return None


def save_budget(amount):
    # Write the budget amount to the budget file
    with open(BUDGET_FILE, "w") as file:
        file.write(str(amount))

def set_budget():
    print("\n--- Set Monthly Budget ---")
    # Show the current budget if one exists
    current = load_budget()
    if current is not None:
        print(f"Current budget: ${current:.2f}")
    # Prompt for a new budget with validation
    while True:
        budget_input = input("Enter your monthly budget: $")
        try:
            budget = float(budget_input)
            if budget <= 0:
                print("Budget must be a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    save_budget(budget)
    print(f"Monthly budget set to ${budget:.2f}")


def check_budget(expenses):
    print("\n--- Budget Status ---")
    budget = load_budget()
    if budget is None:
        print("No budget set. Use 'Set budget' to set one.")
        return
    # Get the current month and year for filtering
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    # Filter expenses to only those in the current month
    monthly_expenses = []
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if expense_date.month == current_month and expense_date.year == current_year:
                monthly_expenses.append(expense)
        except ValueError:
            continue
    # Calculate spending stats
    spent = sum(e["amount"] for e in monthly_expenses)
    remaining = budget - spent
    percentage = (spent / budget) * 100 if budget > 0 else 0
    # Build a 20-character progress bar
    bar_length = 20
    filled = int(bar_length * min(percentage, 100) / 100)
    bar = "\u2588" * filled + "\u2591" * (bar_length - filled)
    # Display the budget status
    print(f"Month: {today.strftime('%B %Y')}")
    print(f"Budget:  ${budget:.2f}")
    print(f"Spent:   ${spent:.2f}")
    print(f"Remaining: ${remaining:.2f}")
    print(f"\n[{bar}] {percentage:.1f}%")
    # Show warnings based on threshold
    if percentage >= 100:
        print("\n\u26a0\ufe0f  OVER BUDGET! You've exceeded your monthly limit.")
    elif percentage >= 80:
        print("\n\u26a0\ufe0f  Warning: You've used over 80% of your monthly budget.")
    else:
        print("\n\u2705 You're within budget. Keep it up!")

def show_menu():
    print("\n===== Expense Tracker =====")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Filter by category")
    print("4. Spending summary")
    print("5. Set budget")
    print("6. Check budget")
    print("7. Exit")
    print("===========================")

def main():
    expenses = load_expenses()
    print("Welcome to Expense Tracker!")
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            filter_by_category(expenses)
        elif choice == "4":
            show_summary(expenses)
        elif choice == "5":
            set_budget()
        elif choice == "6":
            check_budget(expenses)
        elif choice == "7":
            print("Goodbye! Your expenses have been saved.")
            break
        else:
            print("Invalid option. Please enter 1-7.")


if __name__ == "__main__":
    main()