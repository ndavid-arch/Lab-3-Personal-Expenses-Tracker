from datetime import datetime
import os
import time

Welcome_messege = "_______________________________\n\n  Welcome to the Application!\n_______________________________"


def display_menu(show_loading=True):
    # Clear screen before showing the menu
    os.system('cls' if os.name == 'nt' else 'clear')

    # Loading effect
    if show_loading:
        print("Loading ", end="")
        for _ in range(3):
            time.sleep(1)
            print(".", end="", flush=True)
    time.sleep(0.5)
    print("\r" + " " * 20 + "\r", end="")

    print(f"\n{Welcome_messege}\n\n1. Check Remaining Balance\n2. View Expenses\n3. Add New Expense\n4. Exit\n")


class Wallet:
    def __init__(self, balance_file="balance.txt"):
        self.balance_file = balance_file
        self.balance = self.read_balance()

    def read_balance(self):
        try:
            with open(self.balance_file, "r") as f:
                balance = float(f.read().strip())
        except FileNotFoundError:
            with open(self.balance_file, "w") as f:
                f.write("0")
            balance = 0
        except ValueError:
            print("Balance file is corrupted.")
            while True:
                try:
                    balance = float(input("Enter a corrected starting balance: $"))
                    break
                except ValueError:
                    print("Invalid input! Enter a number.")
            with open(self.balance_file, "w") as f:
                f.write(f"{balance:.2f}")
        return balance

    def write_balance(self):
        with open(self.balance_file, "w") as f:
            f.write(f"{self.balance:.2f}")

    def calculate_total_expenses(self):
        total = 0.0
        for file in os.listdir():
            if file.startswith("expenses_") and file.endswith(".txt"):
                try:
                    with open(file, "r") as f:
                        for line in f:
                            parts = line.strip().split("|")
                            if len(parts) == 4:
                                total += float(parts[3])
                except:
                    pass
        return total

    def check_remaining_balance(self):
        total_expenses = self.calculate_total_expenses()
        available_balance = self.balance - total_expenses

        print("\n-------- BALANCE REPORT --------")
        print(f"Initial/Current Balance: ${self.balance:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Available Balance: ${available_balance:.2f}")
        print("-------------------------------\n")

        if available_balance < 0:
            print(f"⚠ Warning: You have overspent your balance by ${-available_balance:.2f}!\n")

        while True:
            add_money = input("Do you want to add money to your balance? (y/n): ").strip().lower()
            if add_money == "y":
                while True:
                    try:
                        amount = float(input("Enter amount to add: $"))
                        if amount <= 0:
                            print("Amount must be positive! Try again.")
                        else:
                            self.balance += amount
                            self.write_balance()
                            print("")
                            print(f"Balance updated! New balance: ${self.balance:.2f}")
                            time.sleep(1)
                            print("Returning to main menu...")
                            break
                    except ValueError:
                        print("Invalid input! Enter a valid number.")
                break
            elif add_money == "n":
                print("\nNo money added.")
                time.sleep(1)
                print("Returning to main menu...")
                break
            else:
                print("Invalid input! Please enter 'y' or 'n'.")

    def add_new_expense(self):
        total_expenses = self.calculate_total_expenses()
        available_balance = self.balance - total_expenses

        print("\n-------- ADD NEW EXPENSE --------")
        print(f"Available Balance: ${available_balance:.2f}")
        print("---------------------------------\n")

        # Date
        while True:
            date_str = input("Enter expense date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.\n")

        filename = f"expenses_{date_str}.txt"

        # Item
        item = input("Enter item name: ").strip()

        # Amount
        while True:
            try:
                amount = float(input("Enter amount spent: $"))
                if amount <= 0:
                    print("Amount must be positive!")
                elif amount > available_balance:
                    print("⚠ Insufficient balance! Cannot save expense.")
                    return
                else:
                    break
            except ValueError:
                print("Invalid amount. Enter a valid number.")

        # Confirmation
        while True:
            print("\nPlease confirm the details:")
            print(f"Date:   {date_str}")
            print(f"Item:   {item}")
            print(f"Amount: ${amount:.2f}")
            confirm = input("Save this expense? (y/n): ").strip().lower()
            if confirm == "y":
                break
            elif confirm == "n":
                print("\nExpense cancelled.")
                print("Press Enter to return to the main menu...")
                input()
                return
            else:
                print("Invalid input! Please enter 'y' or 'n'.")

        # Expense ID
        expense_id = 1
        if os.path.exists(filename):
            with open(filename, "r") as f:
                lines = f.readlines()
                expense_id = len(lines) + 1

        # Timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save expense
        with open(filename, "a") as f:
            f.write(f"{expense_id}|{item}|{now}|{amount}\n")

        print("\nExpense saved successfully!")
        # Updated totals
        total_expenses = self.calculate_total_expenses()
        available_balance = self.balance - total_expenses
        print(f"Initial Balance: ${self.balance + total_expenses:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Available Balance: ${available_balance:.2f}")
        print("Press Enter to return to the main menu...")
        input()

    def view_expenses(self):
        while True:
            print("\n-------- VIEW EXPENSES --------\n1. Search by item name\n2. Search by amount\n3. Back to main menu")
            choice = input("Select an option (1-3): ").strip()

            if choice == "1":
                search_item = input("Enter item name to search: ").strip().lower()
                found = False
                for file in os.listdir():
                    if file.startswith("expenses_") and file.endswith(".txt"):
                        with open(file, "r") as f:
                            for line in f:
                                parts = line.strip().split("|")
                                if len(parts) == 4:
                                    _, item, date_time, amount = parts
                                    if search_item in item.lower():
                                        print(f"Date: {date_time}, Item: {item}, Amount: ${amount}")
                                        found = True
                if not found:
                    print(f"No expenses found with item name '{search_item}'.")

            elif choice == "2":
                while True:
                    try:
                        search_amount = float(input("Enter amount to search: $"))
                        break
                    except ValueError:
                        print("Invalid input! Enter a valid number.")
                found = False
                for file in os.listdir():
                    if file.startswith("expenses_") and file.endswith(".txt"):
                        with open(file, "r") as f:
                            for line in f:
                                parts = line.strip().split("|")
                                if len(parts) == 4:
                                    _, item, date_time, amount = parts
                                    if round(float(amount), 2) == round(search_amount, 2):
                                        print(f"Date: {date_time}, Item: {item}, Amount: ${amount}")
                                        found = True
                if not found:
                    print(f"No expenses found with amount ${search_amount:.2f}.")

            elif choice == "3":
                print("Returning to main menu...")
                time.sleep(1)
                break
            else:
                print("Invalid choice! Please select 1, 2, or 3.")


# --- Create wallet object BEFORE menu loop ---
wallet = Wallet()

# --- Menu loop ---
display_menu(show_loading=True)
while True:
    display_menu(show_loading=False)
    try:
        choice = int(input("What do you want to do? (1-4): ").strip())
    except ValueError:
        print("Invalid input! Please enter a number between 1 and 4.")
        continue

    if choice == 1:
        print("\nYou selected: Check Remaining Balance")
        time.sleep(1)
        wallet.check_remaining_balance()
        time.sleep(3)
    elif choice == 2:
        print("\nYou selected: View Expenses")
        time.sleep(1)
        wallet.view_expenses()
        time.sleep(3)
    elif choice == 3:
        print("\nYou selected: Add New Expense")
        time.sleep(1)
        wallet.add_new_expense()
        time.sleep(3)
    elif choice == 4:
        print("Exiting the program. Goodbye!")
        time.sleep(3)
        break
    else:
        print("Invalid choice! Please enter a number between 1 and 4.")
        time.sleep(1.5)
