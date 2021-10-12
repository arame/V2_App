import os
import datetime
from config import Hyper
import ftfy
from data_cleaner import DataCleaner
from database import Data
from sentiment import Sentiment
from helper import Helper

class HydratedTweets:
    def __init__(self, db_twitter, hydrated_tweets):
        self.hydrated_tweets = hydrated_tweets
        self.no_language_cnt = 0
        self.tweet_saved_cnt = 0
        self.sent = Sentiment()
        self.first_tweet = True
        self.db_twitter = db_twitter

    def output_to_database(self):
        directory_path = os.getcwd()
        for tweet in self.hydrated_tweets:
            os.chdir(directory_path)
            language = tweet["lang"]
            if len(language) == 0 or language == "und":
                self.no_language_cnt += 1
                continue

            #ignore retweets
            
            if 'retweeted_status' in tweet:
                continue            
            
            self.country_code = self.get_country_code_from_place(tweet)
            self.user_location = self.get_user_location(tweet)
            if len(self.country_code) > 0:
                self.output_to_db(tweet)
                continue

            if len(self.user_location) > 0:
                self.output_to_db(tweet)
                continue
            
        # Return to root directory
        Hyper.no_language_cnt += self.no_language_cnt
        Hyper.tweet_saved_cnt += self.tweet_saved_cnt   
    
    def get_user_location(self, tweet):
        user = tweet["user"]
        if user == None or len(user) == 0:
            return ""

        user_location = self.get_string_json_data(user, "location")
        if user_location == None or len(user_location) == 0:
            return ""

        user_location = DataCleaner.remove_noise(user_location)
        return user_location

    def get_country_code_from_place(self, tweet):
        place = tweet["place"]
        if place == None or len(place) == 0:
            return ""

        country_code = self.get_string_json_data(place, "country_code")
        if country_code == None or len(country_code) == 0:
            return ""

        return country_code

    # Helper method to get the string from the JSON data
    def get_string_json_data(self, json, property):
        if property not in json:
            print(f"!! object {property} not in json {json}")
            return ""

        if json[property] == None:
            return ""

        return ftfy.fix_text(json[property])    # ftfy library ensures the encoding works, see https://ftfy.readthedocs.io/en/latest/

    def get_date_json_data(self, json, property):
        if property not in json:
            print(f"!! object {property} not in json {json}")
            return datetime.datetime(1900, 1, 1)

        if json[property] == None:
            return datetime.datetime(1900, 1, 1)
        
        _temp = json[property]
        _date = Helper.convert_string_to_date(_temp)
        return _date

    def output_to_db(self, tweet):
        tweet_id = tweet["id"]
        created_at = self.get_date_json_data(tweet, "created_at")
        language = self.get_string_json_data(tweet, "lang")
        full_text = self.get_string_json_data(tweet, "full_text")
        clean_text = DataCleaner.lowercase_text(full_text)         
        clean_text = DataCleaner.remove_noise(clean_text)
        
        if len(clean_text) == 0:
            return      # Do not output an empty tweet
        
        self.sent.calc(clean_text)
        if self.sent._sentiment == self.sent.NEUTRAL:
            return      # Do not output a tweet with neutral sentiment
        
        is_facemask = self.facemask_in_text(clean_text)
        is_lockdown = self.lockdown_in_text(clean_text)
        is_vaccine = self.is_vaccine_in_text(clean_text)
        retweet_count = tweet["retweet_count"]
        favourite_cnt = tweet["favorite_count"]
        row = {'tweet_id':tweet_id, 
               'lang': language, 
               'created_at': created_at, 
               'place_country_code': self.country_code, 
               'user_location': self.user_location, 
               'country_code': self.country_code, 
               'full_text': full_text, 
               'clean_text': clean_text, 
               'sentiment': self.sent._sentiment, 
               'retweet_cnt': retweet_count, 
               'favourite_cnt': favourite_cnt, 
               'is_facemask': is_facemask, 
               "is_lockdown": is_lockdown, 
               "is_vaccine": is_vaccine}

        self.db_twitter.save_tweet(row)
        self.tweet_saved_cnt += 1
        if self.tweet_saved_cnt % 10000 == 0:
            Helper.printline(f"{self.tweet_saved_cnt} tweets saved")

    def facemask_in_text(self, text):
        if "facemask" in text or "face-mask" in text or "mask" in text:
            return True

        return False  
    
    def lockdown_in_text(self, text):
        if "lockdown" in text:
            return True
        
        return False
    
    def is_vaccine_in_text(self, text):
            # vaccina is short for vaccinated, vaccination. Vax is a short form of the word vaccine or vaccinated
        if "vaccine" in text or "vaccina" in text or "vax" in text:
            return True

        return False      
        