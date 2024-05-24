import sqlite3

# Connect to the database and "bank_management_system.db" is database file.
conn = sqlite3.connect('bank_management_system.db')
c = conn.cursor()

try:
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS Banker
              (Bankerid INTEGER PRIMARY KEY,
              Bname VARCHAR(20) NOT NULL,
              Age INTEGER NOT NULL, 
              Salary REAL NOT NULL, 
              BranchId INTEGER,
              FOREIGN KEY (BranchId) REFERENCES Branch(Branchid) 
              ON DELETE CASCADE ON UPDATE CASCADE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Branch
              (Branchid INTEGER PRIMARY KEY, 
              Bname VARCHAR(20) NOT NULL, 
              Blocation VARCHAR(20) NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Account
              (Accid INTEGER PRIMARY KEY, 
              Balance REAL NOT NULL CHECK(Balance > 0), 
              Branchid INTEGER NOT NULL, 
              FOREIGN KEY (Branchid) REFERENCES Branch(Branchid) 
              ON DELETE CASCADE ON UPDATE CASCADE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Customer
              (Cusid INTEGER PRIMARY KEY, 
              Cname VARCHAR(20) NOT NULL, 
              PhoneNo VARCHAR(20) NOT NULL, 
              Age INTEGER NOT NULL, 
              Email VARCHAR(20) NOT NULL, 
              Accid INTEGER NOT NULL, 
              FOREIGN KEY (Accid) REFERENCES Account(Accid) 
              ON DELETE CASCADE ON UPDATE CASCADE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Loan
              (LoanId INTEGER PRIMARY KEY, 
              IssuedAmount REAL NOT NULL, 
              RemainingAmount REAL NOT NULL, 
              Accid INTEGER NOT NULL, 
              Branchid INTEGER NOT NULL, 
              FOREIGN KEY (Accid) REFERENCES Account(Accid), 
              FOREIGN KEY (Branchid) REFERENCES Branch(Branchid))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS LoanPayment
              (LoanPaymentId INTEGER PRIMARY KEY, 
              PaymentAmount REAL NOT NULL,
              LoanId INTEGER NOT NULL,
              FOREIGN KEY (LoanId) REFERENCES Loan(LoanId) 
              ON DELETE CASCADE ON UPDATE CASCADE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS CustomerLog
              (Cusid INTEGER NOT NULL, 
              Cname VARCHAR(20) NOT NULL, 
              PhoneNo VARCHAR(20) NOT NULL, 
              Age INTEGER NOT NULL, 
              Email VARCHAR(20) NOT NULL, 
              Accid INTEGER NOT NULL, 
              Status VARCHAR(15) NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS BankerLog
              (Bankerid INTEGER NOT NULL,
              Bname VARCHAR(20) NOT NULL,
              Age INTEGER NOT NULL, 
              Salary REAL NOT NULL, 
              BranchId INTEGER NOT NULL,
              Status VARCHAR(15) NOT NULL)''')

    # Create triggers
    c.execute('''CREATE TRIGGER IF NOT EXISTS InsertCustomerTrigger
          AFTER INSERT ON Customer
          FOR EACH ROW
          BEGIN
              INSERT INTO CustomerLog VALUES (NEW.Cusid, NEW.Cname, NEW.PhoneNo, NEW.Age, NEW.Email, NEW.Accid,'Insert');
          END''')

    c.execute('''CREATE TRIGGER IF NOT EXISTS UpdateCustomerTrigger
          AFTER UPDATE ON Customer
          FOR EACH ROW
          BEGIN
              INSERT INTO CustomerLog VALUES (NEW.Cusid, NEW.Cname, NEW.PhoneNo, NEW.Age, NEW.Email, NEW.Accid,'Update');
          END''')

    c.execute('''CREATE TRIGGER IF NOT EXISTS DeleteCustomerTrigger
          AFTER DELETE ON Customer
          FOR EACH ROW
          BEGIN
              INSERT INTO CustomerLog VALUES (OLD.Cusid, OLD.Cname, OLD.PhoneNo, OLD.Age, OLD.Email, OLD.Accid,'Delte');
          END''')
    
    c.execute('''CREATE TRIGGER IF NOT EXISTS InsertBankerTrigger
          AFTER INSERT ON Banker
          FOR EACH ROW
          BEGIN
              INSERT INTO BankerLog VALUES (NEW.Bankerid, NEW.Bname, NEW.Age, NEW.Salary, NEW.Branchid,'Insert');
          END''')
    
    c.execute('''CREATE TRIGGER IF NOT EXISTS UpdateBankerTrigger
          AFTER Update ON Banker
          FOR EACH ROW
          BEGIN
              INSERT INTO BankerLog VALUES (NEW.Bankerid, NEW.Bname, NEW.Age, NEW.Salary, NEW.Branchid,'Update');
          END''')
    
    c.execute('''CREATE TRIGGER IF NOT EXISTS deleteBankerTrigger
          AFTER DELETE ON Banker
          FOR EACH ROW
          BEGIN
              INSERT INTO BankerLog VALUES (OLD.Bankerid, OLD.Bname, OLD.Age, OLD.Salary, OLD.Branchid,'Delete');
          END''')

except:
    print("Already Exist")

def view1():
    c.execute("""
        CREATE VIEW IF NOT EXISTS CustomerAccountView AS
        SELECT c.Cusid, c.Cname, c.PhoneNo, c.Age, c.Email, a.Accid, a.Balance, a.Branchid
        FROM Customer c
        INNER JOIN Account a ON c.Accid = a.Accid
    """)

# Insert data
def insert_banker_data(Bid, Bname, Age, Salary, BranchId):
    c.execute("INSERT INTO Banker VALUES (?, ?, ?, ?, ?)", (Bid, Bname, Age, Salary, BranchId))
    conn.commit()
    print("Data inserted successfully!")

def insert_branch_data(Bid, Bname, Blocation):
    c.execute("INSERT INTO Branch VALUES (?, ?, ?)", (Bid, Bname, Blocation))
    conn.commit()
    print("Data inserted successfully!")

def insert_customer_data(Cid, Cname, PhoneNo, Age, Email, Aid):
    c.execute("INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?)", (Cid, Cname, PhoneNo, Age, Email, Aid))
    conn.commit()
    print("Data inserted successfully!")

def insert_account_data(Aid, Balance, Bid):
    c.execute("INSERT INTO Account VALUES (?, ?, ?)", (Aid, Balance, Bid))
    conn.commit()
    print("Data inserted successfully!")

def insert_loan_data(Lid, IssuedAmount, RemainingAmount, Aid, Bid):
    c.execute("INSERT INTO Loan VALUES (?, ?, ?, ?, ?)", (Lid, IssuedAmount, RemainingAmount, Aid, Bid))
    conn.commit()
    print("Data inserted successfully!")

def insert_loan_payment_data(LoanPaymentId,LoanId, PaymentAmount):
    c.execute("INSERT INTO LoanPayment VALUES (?, ?, ?)", (LoanPaymentId, PaymentAmount, LoanId))
    conn.commit()
    print("Data inserted successfully!")

# Retrieve data
def retrieve_banker_data(Bid):
    c.execute("SELECT * FROM Banker WHERE Bankerid = ?", (Bid,))
    return c.fetchone()

def retrieve_branch_data(Bid):
    c.execute("SELECT * FROM Branch WHERE Branchid = ?", (Bid,))
    return c.fetchone()

def retrieve_customer_data(Cid):
    c.execute("SELECT * FROM Customer WHERE Cusid = ?", (Cid,))
    return c.fetchone()

def retrieve_account_data(Accid):
    c.execute("SELECT * FROM Account WHERE Accid = ?", (Accid,))
    return c.fetchone()

def retrieve_loan_data(Lid):
    c.execute("SELECT * FROM Loan WHERE LoanId = ?", (Lid,))
    return c.fetchone()

# Update data
def update_banker_data(Bid, Bname, Age, Salary, BranchId):
    c.execute("UPDATE Banker SET Bname = ?, Age = ?, Salary = ?, BranchId = ? WHERE Branchid = ?", (Bname, Age, Salary, BranchId, Bid))
    conn.commit()
    print("Data updated successfully!")

def update_customer_data(Cid, Cname, PhoneNo, Age, Email):
    c.execute("UPDATE Customer SET Cname = ?, PhoneNo = ?, Age = ?, Email = ? WHERE Cusid = ?", (Cname, PhoneNo, Age, Email, Cid))
    conn.commit()
    print("Data updated successfully!")

def update_account_data(Aid, Balance):
    c.execute("UPDATE Account SET Balance = ?,WHERE Accid = ?", (Balance, Aid))
    conn.commit()
    print("Data updated successfully!")

def update_branch_data(Bid, Bname, Blocation):
    c.execute("UPDATE Branch SET Bname = ?, Blocation = ? WHERE Branchid = ?", (Bname, Blocation, Bid))
    conn.commit()
    print("Data updated successfully!")

def update_loan_data(Lid, IssuedAmount, RemainingAmount, Aid, Bid):
    c.execute("UPDATE Loan SET IssuedAmount = ?, RemainingAmount = ?, Accid = ?, Branchid = ? WHERE LoanId = ?", (IssuedAmount, RemainingAmount, Aid, Bid, Lid))
    conn.commit()
    print("Data updated successfully!")

# Delete data
def delete_banker_data(Bid):
    c.execute("DELETE FROM Banker WHERE Bankerid = ?", (Bid,))
    conn.commit()
    print("Data deleted successfully!")

def delete_customer_data(Cid):
    c.execute("DELETE FROM Customer WHERE Cusid = ?", (Cid,))
    conn.commit()
    print("Data deleted successfully!")

def delete_account_data(Aid):
    c.execute("DELETE FROM Account WHERE Accid = ?", (Aid,))
    conn.commit()
    print("Data deleted successfully!")

def delete_loan_data(Lid):
    c.execute("DELETE FROM Loan WHERE LoanId = ?", (Lid,))
    conn.commit()
    print("Data deleted successfully!")

# Other functions
def check_account_balance(Aid):
    c.execute("SELECT Balance FROM Account WHERE Accid = ?", (Aid,))
    return c.fetchone()[0]

def transfer_amount(Aid, amount):
    c.execute("UPDATE Account SET Balance = Balance - ? WHERE Accid = ?", (amount, Aid))
    conn.commit()
    print("Amount transferred successfully!")

def deposit_amount(Aid, amount):
    c.execute("UPDATE Account SET Balance = Balance + ? WHERE Accid = ?", (amount, Aid))
    conn.commit()
    print("Amount deposited successfully!")

def withdraw_amount(Aid, amount):
    c.execute("UPDATE Account SET Balance = Balance - ? WHERE Accid = ?", (amount, Aid))
    conn.commit()
    print("Amount withdrawn successfully!")

def pay_remaining_loan(Lid, payment_amount):
    c.execute("SELECT RemainingAmount FROM Loan WHERE LoanId = ?", (Lid,))
    remaining_amount = c.fetchone()[0]
    if payment_amount <= remaining_amount:
        c.execute("UPDATE Loan SET RemainingAmount = RemainingAmount - ? WHERE LoanId = ?", (payment_amount, Lid))
        conn.commit()
        
        while True:
                LoanPaymentId=int(input("Enter Loan Payment ID: "))
                if check_loanPayment_exists(LoanPaymentId):
                    print("ALREADY EXISTED")
                else:
                    insert_loan_payment_data(LoanPaymentId,Lid, payment_amount)
                    print("Payment successful!")
    else:
        print("Payment amount exceeds remaining loan amount!")

    
def check_customer_exists(Cusid):
    c.execute("SELECT 1 FROM Customer WHERE Cusid=?", (Cusid,))
    return c.fetchone() is not None

def check_banker_exists(Bankerid):
    c.execute("SELECT 1 FROM Banker WHERE Bankerid=?", (Bankerid,))
    return c.fetchone() is not None

def check_branch_exists(Branchid):
    c.execute("SELECT 1 FROM Branch WHERE Branchid=?", (Branchid,))
    return c.fetchone() is not None

def check_account_exists(Accid):
    c.execute("SELECT 1 FROM Account WHERE Accid=?", (Accid,))
    return c.fetchone() is not None

def check_loan_exists(LoanId):
    c.execute("SELECT 1 FROM Loan WHERE LoanId=?", (LoanId,))
    return c.fetchone() is not None

def check_loanPayment_exists(LoanPaymentId):
    c.execute("SELECT 1 FROM Loan WHERE LoanPaymentId=?", (LoanPaymentId,))
    return c.fetchone() is not None

# Menus
def main_menu():
    print("--------------------------------------")
    print("        BANK MANAGEMENT SYSTEM        ")
    print("--------------------------------------")
    while True:
        print("1. Branch Details")
        print("2. Banker Information")
        print("3. Customer Services")
        print("4. Loan")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            branch_menu()
        elif choice == "2":
            banker_menu()
        elif choice == "3":
            customer_menu()
        elif choice == "4":
            loan_menu()
        elif choice == "5":
            exit()
        else:
            print("Invalid choice. Please try again.")
            main_menu()

def banker_menu():
    print("1. Insert Banker Data")
    print("2. Retrieve Banker Data")
    print("3. Update Banker Data")
    print("4. Delete Banker Data")
    print("5. Back to Main Menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        while True:
                Bankerid = int(input("Enter Banker ID: "))
                if check_banker_exists(Bankerid):
                    print("ALREADY EXISTED")
                else:
                    Bname = input("Enter Banker Name: ")
                    Age = int(input("Enter Banker Age: "))
                    Salary = float(input("Enter Banker Salary: "))
                    BranchId = int(input("Enter Branch ID: "))
                    insert_banker_data(Bankerid, Bname, Age, Salary, BranchId)
                    break
    elif choice == "2":
        Bid = int(input("Enter Banker ID: "))
        data = retrieve_banker_data(Bid)
        if data:
            print("_______________________________")
            print("Banker ID: ", data[0])
            print("Banker Name: ", data[1])
            print("Banker Age: ", data[2])
            print("Banker Salary: ", data[3])
            print("Branch ID: ", data[4])
            print("_______________________________")
        else:
            print("No data found!")
    elif choice == "3":
        Bid = int(input("Enter Banker ID: "))
        Bname = input("Enter Banker Name: ")
        Age = int(input("Enter Banker Age: "))
        Salary = float(input("Enter Banker Salary: "))
        BranchId = int(input("Enter Branch ID: "))
        update_banker_data(Bid, Bname, Age, Salary, BranchId)
    elif choice == "4":
        Bid = int(input("Enter Banker ID: "))
        delete_banker_data(Bid)
    elif choice == "5":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        banker_menu()

def branch_menu():
    print("1. Insert Branch Data")
    print("2. Retrieve Branch Data")
    print("3. Update Branch Data")
    print("4. Back to Main Menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        while True:
            Branchid = int(input("Enter Branch ID: "))
            if check_branch_exists(Branchid):
                print("ALREADY EXISTED")
            else:
                Bname = input("Enter Branch Name: ")
                Blocation = input("Enter Branch Location: ")
                insert_branch_data(Branchid, Bname, Blocation)
                break
        
    elif choice == "2":
        Branchid = int(input("Enter Branch ID: "))
        data = retrieve_branch_data(Branchid)
        if data:
            print("_______________________________")
            print("Branch ID: ", data[0])
            print("Branch Name: ", data[1])
            print("Branch Location: ", data[2])
            print("_______________________________")
        else:
            print("No data found!")
    elif choice == "3":
        Branchid = int(input("Enter Branch ID: "))
        Bname = input("Enter Branch Name: ")
        Blocation = input("Enter Branch Location: ")
        update_branch_data(Branchid, Bname, Blocation)
    elif choice == "4":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        branch_menu()

def customer_menu():
    print("1. Insert Customer Data")
    print("2. Retrieve Customer Data")
    print("3. Update Customer Data")
    print("4. Delete Customer Data")
    print("5. Check Account Balance")
    print("6. Transfer Amount")
    print("7. Deposit Amount")
    print("8. Withdraw Amount")
    print("9. Create View")
    print("10. Back to Main Menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        while True:
            Cusid = int(input("Enter Customer ID: "))
            if check_customer_exists(Cusid):
                print("ALREADY EXISTED")
            else:
                Cname = input("Enter Customer Name: ")
                PhoneNo = input("Enter Customer Phone Number: ")
                Age = int(input("Enter Customer Age: "))
                Email = input("Enter Customer Email: ")
                while True:
                    Accid = int(input("Enter Account ID: "))
                    if check_account_exists(Accid):
                        print("ALREADY EXISTED")
                    else:
                        Balance=int(input("Enter initially Balance: "))
                        Branchid=int(input("Enter Branchid: "))
                        insert_customer_data(Cusid, Cname, PhoneNo, Age, Email, Accid)
                        insert_account_data(Accid,Balance,Branchid)
                        break
                break
            
    elif choice == "2":
        Cusid = int(input("Enter Customer ID: "))
        data = retrieve_customer_data(Cusid)
        if data:
            print("_______________________________")
            print("Customer ID: ", data[0])
            print("Customer Name: ", data[1])
            print("Phone No.: ", data[2])
            print("Age: ", data[3])
            print("_______________________________")
        else:
            print("No data found!")
    elif choice == "3":
        Cusid = int(input("Enter Customer ID: "))
        Cname = input("Enter Customer Name: ")
        PhoneNo = input("Enter Customer Phone Number: ")
        Age = int(input("Enter Customer Age: "))
        Email = input("Enter Customer Email: ")
        update_customer_data(Cusid, Cname, PhoneNo, Age, Email)
    elif choice == "4":
        Cusid = int(input("Enter Customer ID: "))
        delete_customer_data(Cusid)
    elif choice == "5":
        Accid = int(input("Enter Account ID: "))
        print(check_account_balance(Accid))
    elif choice == "6":
        Accid = int(input("Enter Account ID: "))
        amount = float(input("Enter amount to transfer: "))
        transfer_amount(Accid, amount)
    elif choice == "7":
        Accid = int(input("Enter Account ID: "))
        amount = float(input("Enter amount to deposit: "))
        deposit_amount(Accid, amount)
    elif choice == "8":
        Accid = int(input("Enter Account ID: "))
        amount = float(input("Enter amount to withdraw: "))
        withdraw_amount(Accid, amount)
    elif choice == "9":
        view1()
    elif choice == "10":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        customer_menu()

def loan_menu():
    print("1. Insert Loan Data")
    print("2. Retrieve Loan Data")
    print("3. Update Loan Data")
    print("4. Delete Loan Data")
    print("5. Loan Payment")
    print("6. Back to Main Menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        while True:
            LoanId = int(input("Enter Loan ID: "))
            if check_loan_exists(LoanId):
                print("ALREADY EXISTED")
            else:
                IssuedAmount = float(input("Enter Issued Amount: "))
                RemainingAmount = float(input("Enter Remaining Amount: "))
                Accid = int(input("Enter Account ID: "))
                Branchid = int(input("Enter Branch ID: "))
                insert_loan_data(LoanId, IssuedAmount, RemainingAmount, Accid, Branchid)
                break
    elif choice == "2":
        LoanId = int(input("Enter Loan ID: "))
        data = retrieve_loan_data(LoanId)
        if data:
            print("_______________________________")
            print("Loan ID: ", data[0])
            print("Issued Amount: ", data[1])
            print("Remaining Amount: ", data[2])
            print("Account ID: ", data[3])
            print("Branch ID: ", data[4])
            print("_______________________________")
        else:
            print("No data found!")
    elif choice == "3":
        LoanIdd = int(input("Enter Loan ID: "))
        IssuedAmount = float(input("Enter Issued Amount: "))
        RemainingAmount = float(input("Enter Remaining Amount: "))
        Accid = int(input("Enter Account ID: "))
        Branchid = int(input("Enter Branch ID: "))
        update_loan_data(LoanId, IssuedAmount, RemainingAmount, Accid, Branchid)
    elif choice == "4":
        LoanId = int(input("Enter Loan ID: "))
        delete_loan_data(LoanId)
    elif choice == "5":
        LoanId = int(input("Enter Loan ID: "))
        payment_amount = float(input("Enter payment amount: "))
        pay_remaining_loan(LoanId, payment_amount)

    elif choice == "6":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        loan_menu()

main_menu()
