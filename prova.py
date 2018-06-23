#!/usr/bin/python

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')

paragraph="WOW! Truly the best pizza I have in my life time! That was amazing! I be tried three pizza in Napoli(in one day) and this one is really much better than the other two! So fresh and healthy yet tastes so good!"

lines_list = tokenize.sent_tokenize(paragraph)

sid = SentimentIntensityAnalyzer()
for sentence in lines_list:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    print ss
