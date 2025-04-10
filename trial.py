import cloudscraper

scraper = cloudscraper.create_scraper()  # This imitates a browser
url = "https://www.mitaccomputing.com/en/Search"

data = {
    "search": "B7106G24EV2E2HR"  # replace with actual parameter name
}

headers =  {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.mitaccomputing.com/",
    "Connection": "keep-alive"
}
response = scraper.post(url,headers=headers,data=data)

print(response.text)
with open("mitac_search.html", "w", encoding="utf-8") as file:
    file.write(response.text)

exit()


import requests

url = "https://www.mitaccomputing.com/en/Search"  # update with actual endpoint
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.mitaccomputing.com/en/Search",
    "Content-Type": "application/json"
}


response = requests.post(url, data=data, headers=headers)

if response.ok:
    print(response.json())  # Or response.text depending on the format
else:
    print(f"Failed: {response.status_code}, {response.text}")
with open("mitac_search.html", "w", encoding="utf-8") as file:
    file.write(response.text)
