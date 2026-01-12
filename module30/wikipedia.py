from http.client import HTTPException

import requests
url = "https://en.wikipedia.org"

try:
    response = requests.get(url)
    response.raise_for_status()
    print(response.text)
except requests.exceptions.RequestException as req_err:
    print(f"Request error occured: {req_err}")
except requests.exceptions.HTTPError as http_error:
    print(f"Request error occured: {http_error}")
except requests.exceptions.tiem as conn_err:
    print(f"Request error occured: {conn_err}")