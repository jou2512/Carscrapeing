import requests

api_url = "http://localhost:8000/scrape/"
params = {
    "brand": "citroen",
    "model": "spacetourer",
    "build_year": 2016,
    "engine_hp": "1.6-bluehdi-95",
}



response = requests.get(api_url, params=params)

print(response)