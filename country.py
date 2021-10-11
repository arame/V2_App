import csv
from csv import writer
from config import Hyper
from data_cleaner import DataCleaner
from geopy.geocoders import Nominatim

class Country:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent='Tweet_locator')
        self.saved_countries = []
        reader = csv.reader(open(Hyper.UserLocationFile, encoding='utf-8', errors="ignore"))
        for row in reader:
            country = DataCleaner.remove_noise(row[0])
            self.saved_countries.append(country)

