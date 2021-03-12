import requests
import os

response = requests.get(
    "https://api.tradier.com/v1/user/profile",
    params={},
    headers={
        "Authorization": f'Bearer {os.environ.get("TRADIER_BROKERAGE_TOKEN")}',
        "Accept": "application/json",
    },
)
print(response.status_code)
print(response.headers)
