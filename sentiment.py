import nltk
from data_cleaner import DataCleaner
# VADER (Valence Aware Dictionary and sEntiment Reasoner) 
# is a lexicon and rule-based sentiment analysis tool that is specifically 
# attuned to sentiments expressed in social media.
# See http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config import Hyper

class Sentiment:
    def __init__(self) -> None:
        self.POSITIVE = 1
        self.NEUTRAL = 9
        self.NEGATIVE = 0
        self.THRESHOLD = 0.05
        self.count = 0

    def calc(self, text):
        self.count += 1
        self.text = text
        analyzer = SentimentIntensityAnalyzer()
        try:
            # The VADER library returns 4 values such as
            # pos: The probability of the sentiment to be positive
            # neu: The probability of the sentiment to be neutral
            # neg: The probability of the sentiment to be negative
            # compound: The normalized compound score which calculates the sum of all lexicon ratings and takes values from -1 to 1
            # See documentation https://github.com/cjhutto/vaderSentiment
            scores = analyzer.polarity_scores(self.text)
            self.positive = scores["pos"]
            self.negative = scores["neg"]
            self.neutral = scores["neu"]
            self.compound = scores["compound"]
            self._sentiment = self.get_sentiment()
            self.prev_text = text
        except:
            _t = str(text).encode('utf8')
            print(f"!! Data Error - row: {self.count}, text: {self.text}, previous text: {self.prev_text}")
            self._sentiment = self.NEUTRAL

    def get_sentiment(self):
        # The compound value is set between -1 and 1
        # See https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/

        # if the compound value is between -0.05 and 0.05 (ie self.THRESHOLD), the sentiment is probably neutral
        if abs(self.compound) < self.THRESHOLD:
            return self.NEUTRAL    

        # if the compound is otherwise positive, the sentiment is probably positive
        if self.compound > 0:
            return self.POSITIVE

        # if the compound is otherwise negative, the sentiment is probably negative
        return self.NEGATIVE

    def print_results(self):
        print(f"\ntext: {self.text}")
        print(f"result positive sentiment = {self.positive}")
        print(f"result negative sentiment = {self.negative}")
        print(f"result neutral sentiment = {self.neutral}")

        # Compound is the general overall sentiment of the input. Values between -1 (negative) and 1 (positive).
        print(f"result compound sentiment = {self.compound}")
        print(f"result sentiment = {self._sentiment}")
