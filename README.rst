QIF Parser
============

.. image:: https://travis-ci.org/giacomos/qifparse.png?branch=master
    :target: https://travis-ci.org/giacomos/qifparse

qifparse is a parser for Quicken interchange format files (.qif).

Even if the qif format is:

* quite old now
* not supported for import by Quicken any more,
* ambiguous in some data management (notably on dates)

it's still quite commonly used by many personal finance managers.


Usage
======

Here's a sample parsing::

   >>> from qifparse.parser import QifParser
   >>> qif = QifParser.parse(file('file.qif'))
   >>> qif.get_accounts()
   (<qifparse.qif.Account object at 0x16148d0>, <qifparse.qif.Account object at 0x1614850>)
   >>> qif.accounts[0].name
   'My Cash'
   >>> qif.get_categories()
   (<qifparse.qif.Category object at 0x15b3d10>, <qifparse.qif.Category object at 0x15b3450>)
   >>> qif.accounts[0].get_transactions()
   (<Transaction units=-6.5>, <Transaction units=-6.0>)
   >>> str(qif)
   '!Type:Cat\nNfood\nE\n^\nNfood:lunch\nE\n^\n!Account\nNMy Cash\nTCash\n^\n!Type:Cash...
   ...

Here's a sample of a structure creation::


   >>> qif_obj = qif.Qif()
   >>> acc = qif.Account(name='My Cc', account_type='Bank')
   >>> qif_obj.add_account(acc)
   >>> cat = qif.Category(name='food')
   >>> qif_obj.add_category(cat)
   >>> tr1 = qif.Transaction(amount=0.55)
   >>> acc.add_transaction(tr1, header='!Type:Bank')

   >>> tr2 = qif.Transaction()
   >>> tr2.amount = -6.55
   >>> tr2.to_account = 'Cash'
   >>> acc.add_transaction(tr2)
   >>> acc.add(tr2)
   >>> str(qif_obj)
   '!Type:Cat\nNfood\nE\n^\n!Account\nNMy Cc\nTBank\n^\n!Type:Bank\nD02/11/2013\nT...
   ...

If you find that your QIF files date format has the month before day (like 12/25/2019 for December 25, 2019), then set

   QifParser.MONTH_IS_BEFORE_DAY_IN_DATES = True

before calling QifParser.parse().

More infos
============
For more informations about qif format:

* http://en.wikipedia.org/wiki/Quicken_Interchange_Format
* https://github.com/Gnucash/gnucash/blob/master/gnucash/import-export/qif-imp/file-format.txt
* http://finance-qif.sourceforge.net/
