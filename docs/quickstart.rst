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

The pytradier package uses environment variables to access the Tradier Platform. Once a user has 
established an account with them access your API tokens and save them to your machine::

    >>export TRADIER_SANDBOX_TOKEN=<YOUR_SANDBOX_TOKEN>
    >>export LIVE_TRADIER_TOKEN=<YOUR_LIVE_TOKEN>

Users can choose their own environment variable names, but all the modules use the ``TRADIER_SANDBOX_TOKEN``
key by default. To specific your own name just intialize client with ``token=<YOUR_ENV_NAME>``. To switch
to live mode, also must pass ``paper=False``.

