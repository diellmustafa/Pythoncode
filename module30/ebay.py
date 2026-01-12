import requests
url = "https://www.ebay.com/b/Electronics/bn_7000259124"

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Failed to retrieve the webpage. Status code: {url}")