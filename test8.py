from hydratedTweets import HydratedTweets

def main():
    test = HydratedTweets(None)
    old_country = "the Philippines"
    new_country = test.check_country_name(old_country)
    print(f"Old Country = {old_country}, New Country = {new_country}")
    
if __name__ == "__main__":
    main()