import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"

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



def show_menu():
    # Display the main menu options
    print("\n===== Expense Tracker =====")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Filter by category")
    print("4. Spending summary")
    print("5. Exit")
    print("===========================")


def main():
    # Start with an empty list of expenses
    expenses = load_expenses()

    print("Welcome to Expense Tracker!")

    # Keep showing the menu until the user chooses to exit
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            filter_by_category(expenses)
        elif choice == "4":
            show_summary(expenses)
        elif choice == "5":
            print("Goodbye! Your expenses have been saved.")
            break
        else:
            print("Invalid option. Please enter 1-5.")


if __name__ == "__main__":
    main()