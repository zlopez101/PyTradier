import os
import asyncio
import websockets
import requests


class STREAM:
    def __init__(self, token_env: str = "TRADIER_SANDBOX_TOKEN", paper: bool = True):
        self.token = os.environ.get(token_env)
        if paper:
            self.rest_url = "https://sandbox.tradier.com"
        else:
            self.rest_url = "https://api.tradier.com"

    def create_market_session(self) -> None:
        """POST request to API that returns the wss_url of the streaming session and a token. Valid for 5 minutes
        """
        response = requests.get(
            self.rest_url + "/v1/markets/events/session",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            },
        )
        if response.status_code == 200:
            try:
                stream_dict = response.json().get("stream")
                self.wss_url = stream_dict["url"]
                self.sessionid = stream_dict["sessionid"]
            except KeyError as e:
                print("I made a mistake somewhere")
        else:
            print(response.status_code)
            print(response.headers)
            print(response.json())
