import os, re

class Hyper:
    no_language_cnt = 0
    tweet_saved_cnt = 0
    _date = "_2021_apr_04_08"
    db = f"../sql/twitter{_date}.db"
    countries_file = "countries.csv"
    language = "en"
    create_schema = True
    IsStartAgain = True
    IsLoadCountries = True
    IsLoadUserLocations = True
    IsResetTweets = False
    # Keys, access tokens and secrets taken from Twitter are stored as environment variables
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET'] 
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    no_retweets = True                 #@param {type:"boolean"}
    covid_2021_loc = "../COVID19_2021_Tweets_Dataset"
    covid_loc = "../COVID19_Tweets_Dataset"
    date_format = '%Y%m%d'
    
    def __init__(self) -> None:
        #@title Enter range of dates to Hydrate { run: "auto" }
        self.start_date = '2021-04-04' #@param {type:"date"}
        self.end_date = '2021-04-04' #@param {type:"date"}
        #@title Check Keywords to Hydrate { run: "auto" }
        coronavirus = True #@param {type:"boolean"}
        virus = False #@param {type:"boolean"}
        covid = True #@param {type:"boolean"}
        ncov19 = True #@param {type:"boolean"}
        ncov2019 = True #@param {type:"boolean"}
        self.keyword_dict = {"coronavirus": coronavirus, "virus": virus, "covid": covid, "ncov19": ncov19, "ncov2019": ncov2019}
        
 
class Constants:
    USER_HANDLES_REGEX = re.compile(r"@\S+")
    NEW_LINE_REGEX = re.compile(r'\s+|\\n')