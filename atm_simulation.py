
from datetime import datetime

class Account:
    def __init__(self, username, pin, balance=0):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.daily_withdrawn = 0
        self.last_withdrawal_date = datetime.now().date()

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        today = datetime.now().date()
        if self.last_withdrawal_date != today:
            self.daily_withdrawn = 0
            self.last_withdrawal_date = today

        if amount > self.balance:
            return "Insufficient balance"
        if self.daily_withdrawn + amount > 500:
            return "Withdrawal limit exceeded ($500/day)"

        self.balance -= amount
        self.daily_withdrawn += amount
        return self.balance

    def transfer(self, amount, recipient):
        if amount > self.balance:
            return "Insufficient balance"
        self.balance -= amount
        recipient.balance += amount
        return True


class ATM:
    def __init__(self, accounts):
        self.accounts = accounts
        self.current_account = None

    def authenticate(self, username, pin):
        account = self.accounts.get(username)
        if account and account.pin == pin:
            self.current_account = account
            return True
        return False

    def logout(self):
        self.current_account = None


def run_atm_cli(atm):
    print("==== Welcome to the CLI ATM ====")
    attempts = 0
    max_attempts = 3

    while True:
        username = input("Enter username: ").strip()
        pin = input("Enter PIN: ").strip()

        if atm.authenticate(username, pin):
            print(f"\nLogin successful. Welcome, {username}!\n")
            break
        else:
            attempts += 1
            print("Incorrect username or PIN.")
            if attempts >= max_attempts:
                print("Too many failed attempts. Exiting.")
                return

    while True:
        print("\n--- Main Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Logout / Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            balance = atm.current_account.check_balance()
            print(f"Your current balance is: ${balance:.2f}")

        elif choice == '2':
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("Amount must be positive.")
                else:
                    new_balance = atm.current_account.deposit(amount)
                    print(f"Deposit successful. New balance: ${new_balance:.2f}")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '3':
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("Amount must be positive.")
                else:
                    result = atm.current_account.withdraw(amount)
                    if isinstance(result, str):
                        print(result)
                    else:
                        print(f"Withdrawal successful. New balance: ${result:.2f}")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '4':
            recipient_name = input("Enter recipient username: ").strip()
            if recipient_name == atm.current_account.username:
                print("Cannot transfer to your own account.")
                continue
            recipient = atm.accounts.get(recipient_name)
            if not recipient:
                print("Recipient not found.")
                continue
            try:
                amount = float(input("Enter amount to transfer: "))
                if amount <= 0:
                    print("Amount must be positive.")
                else:
                    result = atm.current_account.transfer(amount, recipient)
                    if isinstance(result, str):
                        print(result)
                    else:
                        print(f"Transfer successful. New balance: ${atm.current_account.balance:.2f}")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '5':
            print(f"Goodbye, {atm.current_account.username}!")
            atm.logout()
            break
        else:
            print("Invalid choice. Please choose a valid option (1-5).")


if __name__ == "__main__":
    accounts_data = {
        "alice": Account("alice", "1234", 1000),
        "bob": Account("bob", "5678", 800),
    }

    atm = ATM(accounts_data)
    run_atm_cli(atm)
