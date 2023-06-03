import os
from dotenv.main import load_dotenv
import requests
load_dotenv()


class DataManager:

    def __init__(self):
        self.sheet_data = {}


    def check_data(self):
        response = requests.get(os.environ.get("SHEETY_API"))
        response.raise_for_status()
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    def update_destination_codes(self):
        for city in self.sheet_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{os.environ.get('SHEETY_API')}{city['id']}",
                json=new_data
            )
            print(response.text)