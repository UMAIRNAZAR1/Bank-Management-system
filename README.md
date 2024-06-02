# Bank-Management-system
 This SQLite-based bank management system creates tables for Bankers, Branches, Accounts, Customers, Loans, Loan Payments, and logs, with triggers to log actions on Customers and Bankers. It provides functions to insert, update, retrieve, and delete data, manage transactions, and loan payments, along with a view for customer accounts and main menu.
# Tables
**Banker Table**
Stores information about bankers.
    Bankerid: INTEGER PRIMARY KEY
    Bname: VARCHAR(20) NOT NULL
    Age: INTEGER NOT NULL
    Salary: REAL NOT NULL
    BranchId: INTEGER, FOREIGN KEY REFERENCES Branch(Branchid)

**Branch Table**
Stores information about bank branches.
    Branchid: INTEGER PRIMARY KEY
    Bname: VARCHAR(20) NOT NULL
    Blocation: VARCHAR(20) NOT NULL

**Account Table**
Stores information about bank accounts.
    Accid: INTEGER PRIMARY KEY
    Balance: REAL NOT NULL CHECK (Balance > 0)
    Branchid: INTEGER NOT NULL, FOREIGN KEY REFERENCES Branch(Branchid)

**Customer Table**
Stores information about customers.
    Cusid: INTEGER PRIMARY KEY
    Cname: VARCHAR(20) NOT NULL
    PhoneNo: VARCHAR(20) NOT NULL
    Age: INTEGER NOT NULL
    Email: VARCHAR(20) NOT NULL
    Accid: INTEGER NOT NULL, FOREIGN KEY REFERENCES Account(Accid)

**Loan Table**
Stores information about loans.
    LoanId: INTEGER PRIMARY KEY
    IssuedAmount: REAL NOT NULL
    RemainingAmount: REAL NOT NULL
    Accid: INTEGER NOT NULL, FOREIGN KEY REFERENCES Account(Accid)
    Branchid: INTEGER NOT NULL, FOREIGN KEY REFERENCES Branch(Branchid)

**LoanPayment Table**
Stores information about loan payments.
    LoanPaymentId: INTEGER PRIMARY KEY
    PaymentAmount: REAL NOT NULL
    LoanId: INTEGER NOT NULL, FOREIGN KEY REFERENCES Loan(LoanId)

**CustomerLog Table**
Logs customer activities.
    Cusid: INTEGER NOT NULL
    Cname: VARCHAR(20) NOT NULL
    PhoneNo: VARCHAR(20) NOT NULL
    Age: INTEGER NOT NULL
    Email: VARCHAR(20) NOT NULL
    Accid: INTEGER NOT NULL
    Status: VARCHAR(15) NOT NULL
    
**BankerLog Table**
Logs banker activities.
    Bankerid: INTEGER NOT NULL
    Bname: VARCHAR(20) NOT NULL
    Age: INTEGER NOT NULL
    Salary: REAL NOT NULL
    BranchId: INTEGER NOT NULL
    Status: VARCHAR(15) NOT NULL

**Triggers**
Triggers maintain logs of inserts, updates, and deletes for the Customer and Banker tables.
InsertCustomerTrigger: Logs insert operations on Customer.
UpdateCustomerTrigger: Logs update operations on Customer.
DeleteCustomerTrigger: Logs delete operations on Customer.
InsertBankerTrigger: Logs insert operations on Banker.
UpdateBankerTrigger: Logs update operations on Banker.
DeleteBankerTrigger: Logs delete operations on Banker.

**Views**
CustomerAccountView
Displays a combined view of customers and their accounts.

# Functions
**Data Insertion**
insert_banker_data(Bid, Bname, Age, Salary, BranchId)
insert_branch_data(Bid, Bname, Blocation)
insert_customer_data(Cid, Cname, PhoneNo, Age, Email, Aid)
insert_account_data(Aid, Balance, Bid)
insert_loan_data(Lid, IssuedAmount, RemainingAmount, Aid, Bid)
insert_loan_payment_data(LoanPaymentId, LoanId, PaymentAmount)

**Data Retrieval**
retrieve_banker_data(Bid)
retrieve_branch_data(Bid)
retrieve_customer_data(Cid)
retrieve_account_data(Accid)
retrieve_loan_data(Lid)

**Data Update**
update_banker_data(Bid, Bname, Age, Salary, BranchId)
update_customer_data(Cid, Cname, PhoneNo, Age, Email)
update_account_data(Aid, Balance)
update_branch_data(Bid, Bname, Blocation)

**Data Deletion**
Apply all tables like previously
