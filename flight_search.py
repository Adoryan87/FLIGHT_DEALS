import os
import requests
from dotenv.main import load_dotenv
load_dotenv()


class FlightSearch:

    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.out_date = None
        self.fly_to = None
        self.fly_from = None
        self.city_to = None
        self.city_from = None
        self.return_date = None
        self.price = None

    def get_destination_code(self, city_name):
        params = {"term": city_name,
                  "location_types": "city"}
        headers = {"apikey": os.environ.get("TEQUILA_API_KEY")}
        response = requests.get("https://api.tequila.kiwi.com/locations/query", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["locations"][0]["code"]

    def check_flights(self, destination_city_code, from_time, to_time):
        headers = {"apikey": os.environ.get("TEQUILA_API_KEY")}
        params = {
            "fly_from": "LON",
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR"
        }
        response = requests.get("https://api.tequila.kiwi.com/v2/search", params=params, headers=headers)
        response.raise_for_status()

        try:
            data = response.json()
            self.city_to = data["data"][0]["cityTo"]
            self.city_from = data["data"][0]["cityFrom"]
            self.price = data["data"][0]["price"]
            self.fly_from = data["data"][0]["flyFrom"]
            self.fly_to = data["data"][0]["flyTo"]
            self.out_date = data["data"][0]["route"][0]["local_departure"].split("T")[0]
            self.return_date = data["data"][0]["route"][1]["local_departure"].split("T")[0]
            return f"{self.city_to}: EUR{self.price}"
        except IndexError:
            print(f"No flights found for {self.fly_to}.")
            return None
