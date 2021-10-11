from hydratedTweets import HydratedTweets

def test7():
    ht = HydratedTweets("ht")
    convert_country(ht, "C├┤te d'Ivoire")
    convert_country(ht, "People's Republic of China")
    convert_country(ht, "The Netherlands")
    convert_country(ht, "Islamic Republic of Iran")

def convert_country(ht, country):
    new_country = ht.check_country_name(country)
    print(f"Old country = {country}")
    print(f"New country = {new_country}")

if __name__ == "__main__":
    test7()
