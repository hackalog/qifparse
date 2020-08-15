# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
import unittest
import os
from qifparse.parser import QifParser

filename = os.path.join(os.path.dirname(__file__), 'file.qif')
filename2 = os.path.join(os.path.dirname(__file__), 'transactions_only.qif')
filename_multi = os.path.join(os.path.dirname(__file__), 'multiAccount.qif')
filename_security = os.path.join(os.path.dirname(__file__), 'security.qif')


class TestQIFParsing(unittest.TestCase):

    def testParseFile(self):
        with open(filename) as f:
            QifParser.MONTH_IS_BEFORE_DAY_IN_DATES = False
            qif = QifParser.parse(f)
        self.assertTrue(qif)

    def testWriteFile(self):
        with open(filename) as f:
            data = f.read()
        with open(filename) as f:
            QifParser.MONTH_IS_BEFORE_DAY_IN_DATES = False
            qif = QifParser.parse(f)
#        out = open('out.qif', 'w')
#        out.write(str(qif))
#        out.close()
        self.assertEqual(data, str(qif))

    def testParseTransactionsFile(self):
        with open(filename2) as f:
            data = f.read()
        with open(filename2) as f:
            QifParser.MONTH_IS_BEFORE_DAY_IN_DATES = False
            qif = QifParser.parse(f)
#        out = open('out.qif', 'w')
#        out.write(str(qif))
#        out.close()
        self.assertEqual(data, str(qif))

    def testSecurities(self):
        with open(filename_security) as f:
            qif = QifParser.parse(f)

    def testParseMultiAccountFile(self):
        with open(filename_multi) as f:
            QifParser.MONTH_IS_BEFORE_DAY_IN_DATES = True
            qif = QifParser.parse(f)

        self.assertEqual(2, len(qif.get_accounts()))
        self.assertEqual('City Checking', qif.get_accounts()[0].name)
        self.assertEqual('Bank', qif.get_accounts()[0].account_type)
        self.assertEqual('Global Credit Card', qif.get_accounts()[1].name)
        self.assertEqual('CCard', qif.get_accounts()[1].account_type)

        city_account_list = qif.get_accounts(name='City Checking')
        self.assertEqual(1, len(city_account_list))
        city_transactions = city_account_list[0].get_transactions()[0]
        self.assertEqual(2, len(city_transactions))
        self.assert_transaction(city_transactions[0], self.to_datetime('2003-03-27'), Decimal('0.00'),
                'X', 'Opening Balance', to_account='City Checking')
        self.assert_transaction(city_transactions[1], self.to_datetime('1992-01-02'), Decimal('123.45'),
                'X', 'Deposit', category='Salary')

        credit_card_account_list = qif.get_accounts(name='Global Credit Card')
        self.assertEqual(1, len(credit_card_account_list))
        credit_transactions = credit_card_account_list[0].get_transactions()[0]
        self.assertEqual(3, len(credit_transactions))
        self.assert_transaction(credit_transactions[0], self.to_datetime('2015-06-17'), Decimal('0.00'),
                'X', 'Opening Balance', to_account='Global Credit Card')
        self.assert_transaction(credit_transactions[1], self.to_datetime('2015-06-18'), Decimal('-1234.56'),
                '*', 'Local Store', category='Food')
        self.assert_transaction(credit_transactions[2], self.to_datetime('2015-06-19'), Decimal('1234.56'),
                '*', 'Local Store', category='Food')


    def assert_transaction(self, txn, when, amount, cleared, payee, category=None, to_account=None):
        self.assertEqual(txn.date, when)
        self.assertEqual(txn.amount, amount)
        self.assertEqual(txn.cleared, cleared)
        self.assertEqual(txn.payee, payee)
        if category:
            self.assertEqual(txn.category, category)
        if to_account:
            self.assertEqual(txn.to_account, to_account)

    def to_datetime(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d')

if __name__ == "__main__":
    import unittest
    unittest.main()
