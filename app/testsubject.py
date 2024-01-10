from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import binascii

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    account_number = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Float)

class Bank:
    def __init__(self):
        self.engine = create_engine('sqlite:///bank.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.load_accounts()

    def load_accounts(self):
        self.session = self.Session()

    def create_account(self, name, balance):
        account_number = self.generate_account_number()
        account = Account(account_number=account_number, name=name, balance=balance)
        self.session.add(account)
        self.session.commit()
        return account_number

    def get_account(self, account_number):
        return self.session.query(Account).filter_by(account_number=account_number).first()

    def display_balance(self, account_number):
        account = self.get_account(account_number)
        return account.balance if account else None

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.balance += amount
            self.session.commit()
            return True
        return False

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if account and account.balance >= amount:
            account.balance -= amount
            self.session.commit()
            return True
        return False

    def generate_account_number(self):
        return int(binascii.hexlify(os.urandom(4)), 16)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    bank = Bank()

    while True:
        clear_screen()
        print("\n1. Create Account\n2. Display Balance\n3. Deposit\n4. Withdraw\n5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            initial_balance = float(input("Enter initial balance: "))
            account_number = bank.create_account(name, initial_balance)
            print(f"Account created successfully. Your account number is: {account_number}")

        elif choice == "2":
            account_number = int(input("Enter your account number: "))
            balance = bank.display_balance(account_number)
            if balance is not None:
                print(f"Your account balance is: {balance}")
            else:
                print("Invalid account number.")

        elif choice == "3":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter deposit amount: "))
            if bank.deposit(account_number, amount):
                print("Deposit successful.")
            else:
                print("Invalid account number or insufficient balance.")

        elif choice == "4":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter withdrawal amount: "))
            if bank.withdraw(account_number, amount):
                print("Withdrawal successful.")
            else:
                print("Invalid account number or insufficient balance.")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue.")

if __name__ == "__main__":
    main()
