from enum import Enum, auto
from typing import Any, Dict, Optional, Tuple, List
from threading import Lock, RLock, Event, Thread
import time
import uuid
from decimal import Decimal
from datetime import datetime
import secrets


class InvalidAmount(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Invalid amount: {self.value}"


class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__()
        self.balance, self.amount = balance, amount

    def __str__(self):
        return f"Invalid withdrawal: {self.amount}, balance is: {self.balance}"


class TransactionType(Enum):
    DEPOSIT = auto()
    WITHDRAWAL = auto()
    TRANSFER_IN = auto()
    TRANSFER_OUT = auto()


class TransactionRecord(object):
    def __init__(self,
                 account_id: uuid.UUID,
                 timestamp: datetime,
                 type: TransactionType,
                 amount: Decimal,
                 balance_after: Decimal,
                 related_account: uuid.UUID = None):
        random_suffix = secrets.token_hex(8).upper()
        self.account_id = account_id
        self.timestamp = timestamp
        self.transaction_id = f"TXN-{self.timestamp.strftime("%Y%m%d%H%M%S")}-{random_suffix}"
        self.amount = amount
        self.balance_after = balance_after
        if related_account is not None:
            self.related_account = related_account


class Account(object):
    def __init__(self, balance: Decimal = 0):
        self._id = uuid.uuid4()
        self.balance: Decimal = Decimal(balance)
        self._lock = RLock()

    def deposit(self, amount: Decimal = 0, *args):
        if amount < 0:
            raise InvalidAmount(amount)
        with self._lock:
            self.balance += amount
            return self.balance_inquiry()

    def withdraw(self, amount: Decimal = 0, *args):
        if amount < 0:
            raise InvalidAmount(amount)
        with self._lock:
            if amount > self.balance:
                raise InsufficientFundsError(self.balance_inquiry(), amount)
            self.balance -= amount
            return self.balance_inquiry()

    def balance_inquiry(self):
        with self._lock:
            return self.balance

    def get_id(self):
        return self._id

    def calculate_interest(self, *args):
        pass

    def pay_interest(self, current_date: datetime):
        pass


class SavingsAccount(Account):
    def __init__(self, balance=0, apy: float = .0365, creation_date: datetime = None, compounded: bool = False):
        """bank class must set last transaction date after every transaction and call calculate_interest"""
        super().__init__(balance)
        if compounded:
            self.base = 1 + apy/365
        else:
            self.apy = apy/365
        self._interest_this_month = 0
        self.last_transaction = creation_date if creation_date is not None else datetime.now()

    def calculate_interest(self, current_date: datetime):
        """calculate interest earned between this date and the last transaction"""
        with self._lock:
            delta = (current_date - self.last_transaction).days
            if self.base:
                interest = self.balance_inquiry() * self.base ** delta
            else:
                interest = self.balance_inquiry() * self.apy * delta
            self._interest_this_month += Decimal(str(interest))

    def pay_interest(self, current_date: datetime):
        with self._lock:
            self.calculate_interest(current_date)
            self.deposit(self._interest_this_month)
            self._interest_this_month = 0
            self.last_transaction = current_date

    def deposit(self, amount: Decimal, date: datetime):
        balance = super().deposit(amount)
        self.calculate_interest(date)
        self.last_transaction = date
        return balance

    def withdraw(self, amount: Decimal, date: datetime):
        balance = super().withdraw(amount)
        self.calculate_interest(date)
        self.last_transaction = date
        return balance


class CheckingAccount(Account):
    def __init__(self, balance=0):
        super().__init__(balance)


class Bank(object):
    def __init__(self):
        self._accounts: Dict[uuid.UUID, Account] = {}
        self._ledger: List[TransactionRecord] = []

    def get_time(self):
        return datetime.now()

    def set_time(self, time: datetime = None):
        """in testing mode, allow artificial date to be passed"""
        self.time = time

    def set_testing_mode(self, testing_mode: bool = True):
        """in testing mode, allow artificial date to be passed"""
        if testing_mode:
            def get_fake_time(self):
                return self.time
            self.get_time = get_fake_time
        else:
            def get_time(self):
                return datetime.now()
            self.get_time = get_time

    def add_account(self, account: Account):
        self._accounts[account.get_id()] = account

    def pay_interest(self):
        "pay interest for all accounts held at the bank.  This should be run once per month."
        current_date = self.get_time()
        for account in self._accounts.values():
            account.pay_interest(current_date)

    def transfer(self, from_account_id: uuid.UUID,
                 to_account_id: uuid.UUID,
                 amount: Decimal):
        """transfer between two accounts held at this bank"""
        try:
            from_account, to_account = self._accounts[from_account_id], self._accounts[to_account_id]
        except KeyError as e:
            print('account not found!')
            raise e

        timestamp = self.get_time()

        from_account_balance = from_account.withdraw(
            amount,
            timestamp)  # errors in withdraw will exit here
        try:
            to_account_balance = to_account.deposit(
                amount,
                timestamp)  # errors in deposit must be reverted and must not be stored in the ledger

            self._ledger.append(TransactionRecord(from_account_id,
                                                  timestamp,
                                                  TransactionType.TRANSFER_OUT,
                                                  amount,
                                                  from_account_balance,
                                                  related_account=to_account_id))
            self._ledger.append(TransactionRecord(to_account_id,
                                                  timestamp,
                                                  TransactionType.TRANSFER_IN,
                                                  amount,
                                                  to_account_balance,
                                                  related_account=from_account_id))
        except Exception as e:
            from_account.deposit(amount, timestamp)
            raise e

    def withdraw(self, account_id: uuid.UUID, amount):
        """withdraw from an account held at this bank, adding transaction to global ledger"""
        account = self._accounts[account_id]
        timestamp = self.get_time()
        new_balance = account.withdraw(amount, timestamp)
        self._ledger.append(TransactionRecord(account_id,
                                              timestamp,
                                              TransactionType.WITHDRAWAL,
                                              amount,
                                              new_balance))

    def deposit(self, account_id, amount):
        """deposit to an account held at this bank, adding transaction to global ledger"""
        account = self._accounts[account_id]
        timestamp = self.get_time()
        new_balance = account.deposit(amount)
        self._ledger.append(TransactionRecord(account_id,
                                              timestamp,
                                              TransactionType.DEPOSIT,
                                              amount, new_balance))

    def get_history(self, account_id: uuid.UUID,
                    start_date: datetime = None,
                    end_date: datetime = None,
                    type: TransactionType = None):
        """get an account's history"""
        records = []
        for record in self._ledger:
            if record.account_id == account_id:
                if (start_date is None or start_date <= record.timestamp) and (end_date is None or end_date >= record.timestamp) and (type is None or type == record.type):
                    records.append(record)
        return sorted(records, key=lambda x: x.timestamp, reverse=True)
