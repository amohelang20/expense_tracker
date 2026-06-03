import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"


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
    print(f"Added: {description} - ${amount:.2f} [{category}]")

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
    expenses = []
    print("Welcome to Expense Tracker!")
    # Keep showing the menu until the user chooses to exit
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            print("Goodbye! Your expenses have been saved.")
            break
        else:
            print("Invalid option. Please enter 1-5.")


if __name__ == "__main__":
    main()