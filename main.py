import datetime as dt
import pandas as pd
from twarc import Twarc
import jsonlines, os, sys
from config import Hyper
from hydratedTweets import HydratedTweets
from helper import Helper
from database import Data

'''
    This program is the first in a suite of programs to be executed in this order
    1/ App - gets tweets from Twitter API
    2/ Location - gets the country of the tweet from user location
    3/ Annotate - calculates the sentiment of each tweet
    4/ Wordcload - shows the words most in use in tweets from different countries
    5/ Datapreparation - gets the data in the correct form
    6/ Transformer - builds a transformer model from the tweets
'''

def main():
    hyper = Hyper()
    d = Data()
    if Hyper.create_schema:
        d.create_schema()
    elif Hyper.IsResetTweets:
        d.reset_tweets()    
    consumer_key = Hyper.consumer_key
    consumer_secret = Hyper.consumer_secret
    access_token = Hyper.access_token
    access_token_secret = Hyper.access_token_secret
    t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)
    year = Helper.string_to_date(hyper.start_date).year
    ids = None
    if year == 2020:
        ids = get_2020_tweet_ids(hyper) 
        
    if year == 2021:
        ids = get_2021_tweet_ids(hyper)
        
    # Number of tweets read.
    Helper.printline(f"   {round((len(ids)/1000000), 3)} million unique tweets.")

    #@title Enter ID output file {run: "auto"}
    final_tweet_ids_filename = "final_ids.txt" #@param {type: "string"}
    # The set of IDs is stored in this file.
    with open(final_tweet_ids_filename, "w+") as f:
        for id in ids:
            f.write('%s\n' % id)

    #@title Set up Directory { run: "auto"}
    output_filename = "output.csv" #@param {type: "string"}

    # Stores hydrated tweets here as jsonl objects
    # Contains one json object per line
    output_json_filename = output_filename[:output_filename.index(".")] + ".txt"
    ids = []
    with open(final_tweet_ids_filename, "r") as ids_file:
        ids = ids_file.read().split()
    hydrated_tweets = []
    ids_to_hydrate = set(ids)

    # Looks at the output file for already hydrated tweets
    if os.path.isfile(output_json_filename):
        with jsonlines.open(output_json_filename, "r") as reader:
            for i in reader.iter(type=dict, skip_invalid=True):
                # These tweets have already been hydrated. So remove them from ids_to_hydrate
                hydrated_tweets.append(i)
                ids_to_hydrate.remove(i["id_str"])
    
    Helper.printline(f"Total IDs: {len(ids)}, IDs to hydrate: {len(ids_to_hydrate)}")
    Helper.printline(f"Hydrated: {len(hydrated_tweets)}")

    count = len(hydrated_tweets)
    start_index = count # The index from where tweets haven't been saved to the output_json_file
    # Stores hydrated tweets to output_json_file every num_save iterations.
    num_save  = 1000

    # Now, use twarc and start hydrating
    for tweet in t.hydrate(ids_to_hydrate):
        hydrated_tweets.append(tweet)
        count += 1
        # If num_save iterations have passed,
        if (count % num_save) == 0:
            tweets = HydratedTweets(d, hydrated_tweets[start_index:])
            tweets.output_to_database()
            Helper.printline(f"   Processed {count} hydrated tweets.")
            Helper.printline(f"   Saved     {Hyper.tweet_saved_cnt} hydrated tweets.")
            # Now, since everything has been written. Reset start_index
            start_index = count
            
    # There might be tweets unwritten in the last iteration if the count is not a multiple of num_tweets.
    # In that case, just write out the remainder of tweets.
    if count != start_index:
        print("Here with start_index", start_index)
        tweets = HydratedTweets(hydrated_tweets[start_index:])
        tweets.output_to_database()
        Helper.printline(f"   Processed {count} hydrated tweets.")
        Helper.printline(f"   Saved     {Hyper.tweet_saved_cnt} hydrated tweets.")

    Helper.printline(f"   ** Completed output **")



def get_2020_tweet_ids(hyper):
    files = []
    # Looks at each folder
    for folder in os.listdir(hyper.covid_loc):
        foldername = os.fsdecode(folder)
        # The folder name is a keyword. We continue for keywords selected above
        if hyper.keyword_dict.get(foldername.split()[0].lower()) == True:
            folderpath = os.path.join(hyper.covid_loc, foldername)
            # Each file is of the format [keyword]_yyyy_mm_dd.txt
            for file in os.listdir(folderpath):
                filename = os.fsdecode(file)
                date = filename[filename.index("_")+1:filename.index(".")]

                # If the date is within the required range, it is added to the
                # list of files to read.
                if (dt.datetime.strptime(hyper.start_date, "%Y-%m-%d").date() 
                    <= dt.datetime.strptime(date, '%Y_%m_%d').date()
                    <= dt.datetime.strptime(hyper.end_date, "%Y-%m-%d").date()):
                    files.append(os.path.join(folderpath, filename))
    # The final list is read, and each of the individual IDs is stored in a collective
    # set of IDs. Duplicates are removed.
    ids = set()
    for filename in files:
        with open(filename) as f:
            # The files are of the format: [id1,id2,id3,...,idn]
            # Remove the brackets and split on commas
            for i in f.readline().strip('][').replace(" ", "").split(","):
                ids.add(i)
    return ids


def get_2021_tweet_ids(hyper):
    _files = get_files_between_dates(hyper)
    ids = set()
    os.chdir(hyper.covid_2021_loc)
    for filename in _files:
        csv_input = pd.read_csv(filename, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
        for _, row in csv_input.iterrows():
            if row["Language"] != Hyper.language:
                continue    # Ignore tweets not in the language
            if Hyper.no_retweets and row["RT"] == "YES":
                continue    # Ignore retweets if no_retweets flag is set to true
            id = int(row["Tweet_ID"])
            ids.add(id)
            if len(ids) % 100000 == 0:
                Helper.printline(f"filename: {filename}, {len(ids)} tweet ids saved")
    
    Helper.printline(f"A total of {len(ids)} tweet ids were found")        
    return ids

def get_files_between_dates(hyper):
    files = Helper.find_csv_filenames(hyper.covid_2021_loc)
    files_in_range = []
    start_date = Helper.string_to_date(hyper.start_date)
    end_date = Helper.string_to_date(hyper.end_date)
    for file in files:
        _file_date = file[0:10]
        file_date = Helper.string_to_date(_file_date)
        if file_date < start_date:
            continue
        if file_date > end_date:
            continue 
        files_in_range.append(file)
        
    return files_in_range
        
    

if __name__ == "__main__":
    main()

