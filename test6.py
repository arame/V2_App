from user_location import UserLocation

def main():
    location = "worldwide"
    print(f"location: {location}")
    ul = UserLocation()
    country = ul.locator(location)
    print(f"country: {country}")




if __name__ == "__main__":
    main()