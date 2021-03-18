import pytest
from PyTradier.rest import REST
from PyTradier.exceptions import *


class TestRest:

    rest = REST()
    # create a rest with various defaults
    # defaulted_rest = REST()

    def test_equity_order(self, randomTicker):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_option_order(self, randomOption):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_combo_order(self, randomTicker, randomOption):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_multileg_order(self, randomTicker, randomOption):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_one_cancels_other(self, randomTicker, randomOption):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_one_triggers_other(self, randomTicker, randomOption):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_one_cancels_other_triggers_other(self, randomTicker, randomOption):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass
