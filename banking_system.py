import streamlit as st
import sqlite3
import random

# The BankAccount class is a basic representation of a bank account.
class BankAccount:
    # Class variable 'balance' which is common for all instances
    balance = 0.0

    # Constructor (__init__ method) to initialize an object when it's created.
    # This demonstrates encapsulation as account_name and account_number are encapsulated within the class.
    balance = 0.0
    def __init__(self, account_name, account_pin, account_number=None):
        self.account_name = account_name
        self.account_pin = account_pin
        self.account_number = account_number if account_number else str(random.randint(1000, 9999))

    # Method to deposit an amount. Demonstrates behavior of the object.
    def deposit(self, amount):
        self.balance += amount
        st.write(f"Your new balance is: {self.balance}")

    # Method to withdraw an amount with a check for sufficient funds.
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            st.write(f"Your new balance is: {self.balance}")
        else:
            st.write("Insufficient funds")

    # Method to check the current balance of the account.
    def check_balance(self):
        st.write(f"Your balance is: {self.balance}")

    # Method to display account details.
    def account_details(self):
        st.write(f"Account name: {self.account_name}")
        st.write(f"Account number: {self.account_number}")
        st.write(f"Account balance: {self.balance}")
    
    # Method to transfer money between accounts.
    def transfer(self, amount, account):
        if self.balance >= amount:
            self.balance -= amount
            account.balance += amount
            st.write(f"Your new balance is: {self.balance}")
        else:
            st.write("Insufficient funds")

# The SavingsAccount class is derived from the BankAccount class, demonstrating inheritance.
class SavingsAccount(BankAccount):
    # Constructor initializes attributes and sets interest_rate.
    def __init__(self, account_name, account_number):
        # 'super()' is used to call the constructor of the parent class (BankAccount).
        super().__init__(account_name, account_number)   
        self.interest_rate = 0.05

    # Method to add interest to the current balance.
    def add_interest(self):
        self.balance += self.balance * self.interest_rate
        st.write(f"Your new balance is: {self.balance}")
    
    # Overriding the account_details method from parent class to include interest rate, demonstrating polymorphism.
    def account_details(self):
        super().account_details()
        st.write(f"Interest rate: {self.interest_rate}")
    
    # Overriding deposit method to include adding interest after every deposit.
    def deposit(self, amount):
        super().deposit(amount)
        self.add_interest()
    
    # Overriding withdraw method to include adding interest after every withdrawal.
    def withdraw(self, amount):
        super().withdraw(amount)
        self.add_interest()
    
    # transfer method to demonstrate polymorphism, allowing transfer between CurrentAccount and SavingsAccount.
    def transfer(self, amount, account):
        super().transfer(amount, account)
        self.add_interest()

# The CurrentAccount class is another child class of BankAccount, again demonstrating inheritance.
class CurrentAccount(BankAccount):
    # Constructor initializes attributes and sets overdraft_limit.
    def __init__(self, account_name, account_number):
        super().__init__(account_name, account_number)
        self.overdraft_limit = 1000

    # Overriding the withdraw method from parent class to include an overdraft limit check.
    def withdraw(self, amount):
        if self.balance + self.overdraft_limit >= amount:
            self.balance -= amount
            st.write(f"Your new balance is: {self.balance}")
        else:
            st.write("Insufficient funds")

    # transfer method to demonstrate polymorphism, allowing transfer between CurrentAccount and SavingsAccount.
    def transfer(self, amount, account):
        super().transfer(amount, account)
        self.overdraft_limit = 1000
        
    # Overriding the account_details method to include overdraft limit.
    def account_details(self):
        super().account_details()
        st.write(f"Overdraft limit: {self.overdraft_limit}")

# Function to demonstrate abstraction, as it's not specific to either SavingsAccount or CurrentAccount.
def save_account_details(account):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT, number TEXT, balance REAL, pin TEXT)")
    c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (account.account_name, account.account_number, account.balance, account.account_pin))
    c.execute("UPDATE accounts SET balance = ? WHERE number = ?", (account.balance, account.account_number))
    conn.commit()
    conn.close()

    # Update the balance of the account object in the session state
    st.session_state['account_balance'] = account.balance

def get_account(account_number, account_pin):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("SELECT name, number, balance, pin FROM accounts WHERE number=? AND pin=?", (account_number, account_pin))
    account_data = c.fetchone()
    conn.close()
    if account_data:
        # Create the account object with the retrieved name and pin, then return it with the balance
        account = BankAccount(account_data[0], account_data[3], account_data[1])
        print(f"Retrieved balance from database: {account_data[2]}")

        return account, account_data[2]
    return None, None


# Main application function using Streamlit to interface with the classes.
def app():
    st.title("Banking System ATM")

    # Initialize session state for login and account
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'account' not in st.session_state:
        st.session_state.account = None

    if not st.session_state.logged_in:
        activity = st.selectbox("Choose Activity", ["Login", "Create Account"])

        if activity == "Login":
            st.subheader("Login to Your Account")
            account_number = st.text_input("Account Number")
            account_pin = st.text_input("PIN", type="password")
            if st.button("Login"):
                account, retrieved_balance = get_account(account_number, account_pin)
                if account:
                    account.balance = retrieved_balance
                    st.success("Logged in successfully!")
                    st.session_state.logged_in = True
                    st.session_state.account = account

                else:
                    st.error("Invalid account number or PIN!")

        elif activity == "Create Account":
            st.subheader("Create a New Account")
            account_name = st.text_input("Your Name")
            account_pin = st.text_input("Set a PIN", type="password")
            account_type = st.selectbox("Account Type", ["Savings", "Current"])

            if account_type == "Savings":
                account = SavingsAccount(account_name, account_pin)
            elif account_type == "Current":
                account = CurrentAccount(account_name, account_pin)

            if st.button("Create Account"):
                save_account_details(account)
                st.success(f"Account created successfully! Your account number is: {account.account_number}")
                st.session_state.logged_in = True
                st.session_state.account = account

    else:  # If user is logged in
        account = st.session_state.account
        action = st.selectbox("Choose operation", ["Deposit", "Withdraw", "Transfer", "Check Balance", "Account Details", "Logout"])
        
        if action == "Deposit":
            amount = st.number_input("Enter Deposit Amount", step=0.01)
            if st.button("Confirm Deposit"):
                account.deposit(amount)
                save_account_details(account)
                
        elif action == "Withdraw":
            amount = st.number_input("Enter Withdrawal Amount", step=0.01)
            if st.button("Confirm Withdraw"):
                account.withdraw(amount)
                save_account_details(account)
        
        elif action == "Transfer":
            amount = st.number_input("Enter Transfer Amount", step=0.01)
            account_number = st.text_input("Enter Account Number")
            account_pin = st.text_input("Enter Account PIN", type="password")
            if st.button("Confirm Transfer"):
                account.transfer(amount, get_account(account_number, account_pin)[0])
                save_account_details(account)
                
        elif action == "Check Balance":
            account.check_balance()

        elif action == "Account Details":
            account.account_details()
            
        if st.button("Logout"):
            st.session_state.logged_in = False  # Reset the login state

# Run Streamlit app
if __name__ == "__main__":
    app()
