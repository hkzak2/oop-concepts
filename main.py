from abc import ABC, abstractmethod
# Simple Banking system to demonstrate OOP in Python
class BankAccount:
    balance = 0.0
    def __init__(self, account_name, account_number):
        self.account_name = account_name
        self.account_number = account_number

    def deposit(self, amount):
        self.balance += amount
        print(f"Your new balance is: {self.balance}") 
        

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Your new balance is: {self.balance}")
        else:
            print("Insufficient funds")

    def check_balance(self):
        print(f"Your balance is: {self.balance}")

    def account_details(self):
        print(f"Account name: {self.account_name}")
        print(f"Account number: {self.account_number}")
        print(f"Account balance: {self.balance}")
        

# Create an instance of the BankAccount class
account = BankAccount("John Doe", "1234567890")

# Call the methods on the account object
account.deposit(1000)
account.withdraw(500)
account.check_balance()
account.account_details()

# Inheritance
class SavingsAccount(BankAccount):
    def __init__(self, account_name, account_number):
        super().__init__(account_name, account_number)
        self.interest_rate = 0.05

    def add_interest(self):
        self.balance += self.balance * self.interest_rate
        print(f"Your new balance is: {self.balance}")
    
    def account_details(self):
        super().account_details()
        print(f"Interest rate: {self.interest_rate}")
    
    def deposit(self, amount):
        super().deposit(amount)
        self.add_interest()
    
    def withdraw(self, amount):
        super().withdraw(amount)
        self.add_interest()

savings_account = SavingsAccount("Jane Doe", "0987654321")
savings_account.deposit(1000)
savings_account.withdraw(500)
savings_account.check_balance()
savings_account.account_details()

# Polymorphism
class CurrentAccount(BankAccount):
    def __init__(self, account_name, account_number):
        super().__init__(account_name, account_number)
        self.overdraft_limit = 1000

    def withdraw(self, amount):
        if self.balance + self.overdraft_limit >= amount:
            self.balance -= amount
            print(f"Your new balance is: {self.balance}")
        else:
            print("Insufficient funds")

    def transfer(self, amount, account):
        if self.balance + self.overdraft_limit >= amount:
            self.balance -= amount
            account.balance += amount
            print(f"Your new balance is: {self.balance}")
        else:
            print("Insufficient funds")
        
    def account_details(self):
        super().account_details()
        print(f"Overdraft limit: {self.overdraft_limit}")
    
    @abstractmethod
    def deposit(self, amount):

 
current_account = CurrentAccount("John Doe", "1234567890")
current_account.deposit(2000)
current_account.withdraw(500)
current_account.check_balance()
current_account.account_details()
# transfer money from current account to savings account
current_account.transfer(500, savings_account)
current_account.check_balance()
savings_account.check_balance()

    