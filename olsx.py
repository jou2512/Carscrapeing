from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/scrape/")
def scrape_data(brand: str, model: str, build_year: int, engine_hp: str):

    print(brand, model, build_year, engine_hp)

    # Create the URL with the encoded variables
    url = f"https://www.olsx.lu/en/chiptuning/{brand}/{model}/{build_year}/{engine_hp}"

    # Send a GET request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with class "results"
    table = soup.find("table", class_="results")

    # Find all rows (tr) in the table body
    rows = table.find_all("tr")

    # Extract the required information from the table
    power_stock = rows[1].find_all("td")[1].text
    power_stage1 = rows[1].find_all("td")[2].text
    power_gain = rows[1].find_all("td")[3].text

    torque_stock = rows[2].find_all("td")[1].text
    torque_stage1 = rows[2].find_all("td")[2].text
    torque_gain = rows[2].find_all("td")[3].text
    return {
        "Power": {
            "Stock": power_stock,
            "Stage 1": power_stage1,
            "Gain": power_gain,
        },
        "Torque": {
            "Stock": torque_stock,
            "Stage 1": torque_stage1,
            "Gain": torque_gain,
        },
    }


def scrape_manufacturers(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        manufacturers = soup.select('small.manufacturer')
        return [manufacturer.text for manufacturer in manufacturers]
    else:
        return []


@app.get("/manufacturers")
def scrape_and_save():
    url = 'https://www.olsx.lu/en/chiptuning'
    manufacturers = scrape_manufacturers(url)
    if manufacturers:
        with open('manufacturers.txt', 'w') as file:
            file.write('\n'.join(manufacturers))
        return {'message': 'Scraping and saving completed successfully!'}
    else:
        return {'message': 'Error accessing the URL or no manufacturers found.'}
