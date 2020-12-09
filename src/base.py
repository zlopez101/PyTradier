import os


class BasePyTradier:
    """
    A base class for all the api modules to share the create headers method
    """

    def __init__(self, paper):
        self.orders = []

        # previewing orders
        self.preview = True
        if paper:
            self.accountId = "VA90702788"
            self.token = os.environ.get("TRADIER_SANDBOX_TOKEN")
            self.url = "https://sandbox.tradier.com/v1/"
        else:
            self.accountId = "6YA14703"
            self.token = os.environ.get("TRADIER_BROKERAGE_TOKEN")
            self.url = "https://api.tradier.com/v1/"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
