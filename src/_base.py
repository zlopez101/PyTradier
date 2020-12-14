import os


class BasePyTradier:
    """
    A base class for all the api modules to share the create headers method
    """

    def __init__(self, paper):

        if paper:
            self.accountId = os.environ.get("TRADIER_PAPERACCOUNTID")
            self.token = os.environ.get("TRADIER_SANDBOX_TOKEN")
            self.url = "https://sandbox.tradier.com/v1/"
        else:
            self.accountId = os.environ.get("TRADIER_BROKERAGEACCOUNTID")
            self.token = os.environ.get("TRADIER_BROKERAGE_TOKEN")
            self.url = "https://api.tradier.com/v1/"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
