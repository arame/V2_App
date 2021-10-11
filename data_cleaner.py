import neattext.functions as nfx
import re
from config import Constants

class DataCleaner:
    # Data cleaning methods taken from "Emotion and sentiment analysis of tweets using BERT", Andrea Chiorrini et al
    def lowercase_text(text):
        # The token id for a word should be the same whether it is capitalised or not
        # To ensure this happens, make the word lowercase
        return text.lower()

    def remove_noise(text):
        text = nfx.remove_html_tags(text)
        # Replace a user handle with a <USER> token, see
        text = re.sub(Constants.USER_HANDLES_REGEX, "<USER>", text)  
        text = nfx.remove_urls(text)
        text = re.sub(Constants.NEW_LINE_REGEX, " ", text)     # remove /n
        text = nfx.remove_multiple_spaces(text)
        text = nfx.remove_non_ascii(text)
        return text