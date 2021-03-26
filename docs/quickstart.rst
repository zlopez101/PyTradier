QuickStart
==========


Disclaimer
++++++++++

This package helps python interact with the Tradier Platform to execute algorithmic trading
strategies.  Use at your own discretion, and thoroughly test before using in production.

Getting Started
+++++++++++++++

Install the package with pip::

    >>> pip install pytradier

This package is actually not currently available to pip. Once I finish the testing I will publish. Thanks!

The pytradier package uses environment variables to access the Tradier Platform. Once a user has 
established an account with them access your API tokens and save them to your machine::

    >>export TRADIER_SANDBOX_TOKEN=<YOUR_SANDBOX_TOKEN>
    >>export LIVE_TRADIER_TOKEN=<YOUR_LIVE_TOKEN>

Users can choose their own environment variable names, but all the modules use the ``TRADIER_SANDBOX_TOKEN``
key by default. To specific your own name just intialize client with ``token=<YOUR_ENV_NAME>``. To switch
to live mode, also must pass ``paper=False``.

Account Information
+++++++++++++++++++

Access all account related information using the Account Module::

    from PyTradier import Account
    account = Account() # for live trading pass in paper=False, token=<YOUR_TOKEN>

All account methods return either a dictionary with information or a list of dictionaries with account information.
3 methods take additional arguments::

    # order
    specific_order = account.order(orderId) # return the status and info for a specific order

    # history
    history = account.history(**kwargs)

    # gainloss
    gainloss = account.gainloss(**kwargs)


Trading
+++++++

Concepts
--------

PyTradier imposes structure on the Tradier trading process. Orders are typically instantiated as their specific type within
the ``REST`` object methods. These methods also specify the type of order being placed. The ordering methods take the information
and place a ``post`` request to the Tradier API with the correct ordering parameters. They perform some minimal error checking to 
ensure that the order is properly composed (by raising some errors) but are not guaranteed to catch all errors. Any errors that aren't 
caught (from the Tradier API) are recorded in the order response object under the key ``"error"``. 

The instantiated rest object also configures some optional defaults for users. These defaults should be passed as keyword argument
when the rest object is instantiated, as ``preview=True``, ``duration="gtc"``, and/or ``tag=func``. Note the tag keyword should be a function that returns order tags when called.


Setting ``preview=True`` to any order in a group of orders [like in a ``one_triggers_one_cancels_other()`` call] or as the default on the
rest object will instruct the Tradier API to return the order preview object. Users can inspect this object to make sure trades are properly
formatted.


Equity Trading
---------------

Placing trade orders with PyTradier is intuitive::

    from Pytradier.orders import *
    from PyTradier import REST

    rest = REST() # for live trading pass in paper=False, token=<YOUR_TOKEN>

    rest.equity(MarketOrder("AAPL", "buy", 10, duration='gtc'))

    # first order is the index order, second and third are ones to be cancelled
    # these are fake orders so the may not make any sense
    rest.one_triggers_one_cancels_other(
      LimitOrder(),
      StopOrder(),
      StopLimitOrder()
    )


Placing an order will return the Tradier API order response object

Options, Combo Orders, and Multileg Trades
------------------------------------------

Interacting with options contracts is also simple with the PyTradier package::

    from Pytradier.orders import *
    from PyTradier import REST

    rest = REST() # for live trading pass in paper=False, token=<YOUR_TOKEN>

    rest.option(MarketOrder("AAPL211205C00060000", 'buy_to_open', 1, duration='day')) # number of contracts to purchase

    # combo orders are 1 equity leg, and either 1 or 2 option legs for a max of 3 orders
    rest.combo_order()

Order Objects
-------------



Order Response Object
---------------------



Ordering Errors
---------------

Taking a look at the tradier documentation, you can see that errors can be easily made when making even simple trades.
PyTradier simplifies the ordering process


Data
+++++++++++

Market Data
-----------

Market Data is easily accessed through the data module. 

Fundamental Data
----------------

Tradier's fundamental data API is currently in a beta status. This package does support the current version, but per tradier
these methods shouldn't be relied in production

Watchlists
++++++++++


Websocket
+++++++++

