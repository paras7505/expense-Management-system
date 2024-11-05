import csv
from datetime import datetime

# Expense class to represent each expense entry
class Expense:
    def __init__(self, amount, date, category, description):
        self.amount = amount
        self.date = date
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "description": self.description
        }

class ExpenseTracker:
    def __init__(self, filename='expenses.csv'):
        self.expenses = []
        self.filename = filename
        self.load_expenses()

    def add_expense(self, amount, date, category, description):
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()  # Validate date format
            amount = float(amount)  # Validate amount as a positive number
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            expense = Expense(amount, date, category, description)
            self.expenses.append(expense)
            print(f"Added expense: {expense.to_dict()}")
        except ValueError as e:
            print(f"Invalid input: {e}")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        for index, expense in enumerate(self.expenses):
            print(f"Index {index}: {expense.to_dict()}")

    def delete_expense(self, index):
        try:
            removed_expense = self.expenses.pop(index)
            print(f"Deleted expense: {removed_expense.to_dict()}")
        except IndexError:
            print("Invalid index. Expense not found.")

    def update_expense(self, index, amount=None, date=None, category=None, description=None):
        try:
            expense = self.expenses[index]
            if amount:
                expense.amount = float(amount)
            if date:
                expense.date = datetime.strptime(date, "%Y-%m-%d").date()
            if category:
                expense.category = category
            if description:
                expense.description = description
            print("Expense updated.")
        except (ValueError, IndexError) as e:
            print(f"Error updating expense: {e}")

    def filter_by_category(self, category):
        categorized_expenses = [e.to_dict() for e in self.expenses if e.category == category]
        if categorized_expenses:
            for expense in categorized_expenses:
                print(expense)
        else:
            print(f"No expenses found for category: {category}")

    def generate_report(self, time_period):
        report = {}
        now = datetime.now().date()
        for expense in self.expenses:
            if time_period == "daily" and expense.date == now:
                report[expense.date] = report.get(expense.date, 0) + expense.amount
            elif time_period == "weekly" and (now - expense.date).days <= 7:
                report[expense.date] = report.get(expense.date, 0) + expense.amount
            elif time_period == "monthly" and (now.year == expense.date.year and now.month == expense.date.month):
                report[expense.date] = report.get(expense.date, 0) + expense.amount

        if report:
            for date, total in report.items():
                print(f"Date: {date}, Total Expense: {total}")
        else:
            print("No expenses found for the selected time period.")

    def save_expenses(self):
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["amount", "date", "category", "description"])
                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow(expense.to_dict())
            print("Expenses saved to CSV.")
        except IOError as e:
            print(f"Error saving file: {e}")

    def load_expenses(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.expenses.append(
                        Expense(float(row["amount"]), datetime.strptime(row["date"], "%Y-%m-%d").date(), row["category"], row["description"])
                    )
            print("Expenses loaded from CSV.")
        except FileNotFoundError:
            print("No previous data found. Starting with an empty list.")
        except IOError as e:
            print(f"Error loading file: {e}")


# Main execution block
def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. Filter by Category")
        print("6. Generate Report")
        print("7. Save Expenses")
        print("8. Exit")

        choice = input("Choose an option: ")
        
        if choice == '1':
            amount = input("Enter amount: ")
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(amount, date, category, description)
        
        elif choice == '2':
            tracker.view_expenses()
        
        elif choice == '3':
            index = int(input("Enter expense index to delete: "))
            tracker.delete_expense(index)
        
        elif choice == '4':
            index = int(input("Enter expense index to update: "))
            amount = input("Enter new amount (or leave blank): ")
            date = input("Enter new date (YYYY-MM-DD) (or leave blank): ")
            category = input("Enter new category (or leave blank): ")
            description = input("Enter new description (or leave blank): ")
            tracker.update_expense(index, amount, date, category, description)
        
        elif choice == '5':
            category = input("Enter category to filter: ")
            tracker.filter_by_category(category)
        
        elif choice == '6':
            period = input("Enter report period (daily, weekly, monthly): ")
            tracker.generate_report(period)
        
        elif choice == '7':
            tracker.save_expenses()
        
        elif choice == '8':
            tracker.save_expenses()  # Save data before exiting
            print("Exiting application.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()