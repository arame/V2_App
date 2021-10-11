from data_cleaner import DataCleaner

def main():
    tweet = "@igloo, Time for 34 pints!!!\n\n  #herewego https://www.bbc.com"
    print(f"Tweet start = {tweet}")
    tweet1 = DataCleaner.lowercase_text(tweet)
    tweet2 = DataCleaner.remove_noise(tweet1)
    print(f"Tweet end = {tweet2}")



if __name__ == "__main__":
    main()