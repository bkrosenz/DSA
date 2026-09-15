# **Assignment Specification: Core Banking System**

## **Overview**

You are tasked with building the core logic for a lightweight, in-memory banking system in Python. This system will manage user accounts, handle financial transactions (deposits, withdrawals, transfers), maintain a searchable transaction history, and calculate time-based interest.

This assignment assesses your ability to design robust object-oriented systems, ensure state consistency, handle edge cases (like insufficient funds), and manage time-dependent logic.

## **Part 1: Core Account Management**

**Objective:** Implement basic account creation, deposits, withdrawals, and balance inquiries.

### **Requirements:**

> 1. **Account Creation:**  
   * Implement an Account class (or similar structure).  
   * Each account must have a unique, system-generated account\_number (string).  
   * Accounts must have an initial balance of 0.0 unless specified otherwise during creation.  
   * Balances must be tracked with financial precision (e.g., using decimal.Decimal, not standard floating-point numbers).  
> 2. **Deposits & Withdrawals:**  
   * Implement methods to deposit and withdraw funds.  
   * Withdrawals that exceed the current balance must be rejected, raising an InsufficientFundsError.  
   * Deposits or withdrawals of negative amounts must be rejected, raising an InvalidAmountError.  
> 3. **Balance Query:**  
   * Implement a method to retrieve the current balance.

## **Part 2: Inter-Account Transfers**

**Objective:** Implement secure, atomic transfers between accounts.

### **Requirements:**

> 1. **Transfer Logic:**  
   * Implement a method (e.g., in a Bank management class) to transfer funds from a source\_account to a destination\_account.  
   * The transfer must fail if the source account has insufficient funds.  
   * The transfer must fail if the transfer amount is negative or zero.  
> 2. **Atomicity (Simulated):**  
   * The transfer must be treated as a single atomic action. If the withdrawal from the source account succeeds but the deposit to the destination account fails for any reason (e.g., an internal system error, or the destination account was closed), the source account's funds *must* be restored.

## **Part 3: Transaction History & Filtering**

**Objective:** Maintain an immutable ledger of all account activities and provide search capabilities.

### **Requirements:**

> 1. **Ledger:**  
   * Every successful action (Deposit, Withdrawal, Transfer In, Transfer Out) must generate a Transaction record.  
   * A Transaction must contain:  
     * Unique transaction\_id (string).  
     * timestamp (datetime object).  
     * type (e.g., 'DEPOSIT', 'WITHDRAWAL', 'TRANSFER\_IN', 'TRANSFER\_OUT').  
     * amount (Decimal).  
     * balance\_after\_transaction (Decimal).  
     * (Optional but recommended) related\_account\_id for transfers.  
> 2. **History Retrieval:**  
   * Implement a method to retrieve the transaction history for a specific account.  
   * Transactions must be ordered by timestamp (newest first).  
> 3. **Filtering:**  
   * The retrieval method must support optional filters:  
     * start\_date and end\_date: Return only transactions within this date range (inclusive).  
     * transaction\_type: Return only transactions of a specific type.

## **Part 4: Time-Dependent Interest Calculation**

**Objective:** Implement a system to apply daily interest to savings accounts based on their daily closing balance.

### **Requirements:**

> 1. **Account Types:**  
   * Differentiate between a CheckingAccount (no interest) and a SavingsAccount (earns interest).  
> 2. **Interest Logic:**  
   * SavingsAccount has an Annual Percentage Yield (APY), e.g., 3.65%.  
   * Interest is calculated daily but paid monthly (or on demand via a specific method call).  
   * **The Challenge:** The interest calculation must correctly account for balance changes *throughout* the month. For example, if an account has $1000 for 15 days, and then $500 for the next 15 days, the interest earned should reflect those distinct daily balances.  
> 3. **Time Simulation:**  
   * Since you cannot wait actual days to test this, your system must accept an external "current time" or allow time to be artificially advanced for testing purposes.

## **Evaluation Criteria**

> * **Financial Precision:** Proper use of Decimal to avoid floating-point errors.  
> * **State Consistency:** Guaranteeing that funds are never lost or created out of thin air, especially during failed transfers.  
> * **Error Handling:** Graceful rejection of invalid operations using custom exception classes.  
> * **Object-Oriented Design:** Clean encapsulation, appropriate use of inheritance (e.g., Base Account \-\> Checking/Savings), and separation of concerns (e.g., Bank Manager vs. Account Object).  
> * **Testability:** The time-dependent logic must be easily testable without using time.sleep().