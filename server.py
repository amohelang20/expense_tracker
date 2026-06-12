import json
import csv
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

DATA_FILE = "expenses.csv"


def load_expenses():
    # Read all expenses from the CSV file and return as a list of dicts
    expenses = []
    if not os.path.exists(DATA_FILE):
        return expenses
    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses


def save_expense(expense):
    # Append a single expense dict to the CSV file
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(expense)


class ExpenseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/expenses":
            # Return all expenses as JSON
            expenses = load_expenses()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(expenses).encode())
        else:
            # Serve the dashboard HTML file
            try:
                with open("dashboard.html", "r") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"dashboard.html not found")

    def do_POST(self):
        if self.path == "/api/expenses":
            # Read the request body and save the new expense
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            expense = json.loads(body)
            # Add today's date if not provided
            if not expense.get("date"):
                expense["date"] = datetime.today().strftime("%Y-%m-%d")
            save_expense(expense)
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "created"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default request logging to keep the terminal clean
        pass


if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("", port), ExpenseHandler)
    print(f"Dashboard running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()