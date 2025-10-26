#
# donlp.py
#
#   use NLTK.vader to extract names from the bible, insert them into an sqlite database with their sentiment scores
#   This makes use of the json formatted bible found here: https://github.com/honza/bibles/blob/master/ESV/ESV.json
#

import json
import sqlite3
import re
import string
from collections import defaultdict

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import SpaceTokenizer
from nltk import pos_tag

# Initialize sentiment analyzer once for performance
sentiment_analyzer = SentimentIntensityAnalyzer()

# analyze_line(line):
#   Analyze a line of text, return names and sentiment polarity scores
def analyze_line(line):
    """Analyze a line of text and extract names with sentiment scores."""
    tokens = pos_tag(SpaceTokenizer().tokenize(line))

    names = []
    for token in tokens:
        if token[1] == 'NNP':
            names.append(re.sub('['+string.punctuation+']', '', token[0]))

    return {"names": names, "sentiment": sentiment_analyzer.polarity_scores(line)}



# build_namedb(filepath): 
#   Analyze the json formatted bible text (from https://github.com/honza/bibles/) and insert detected names into an sqlite table
def build_bible_namedb(filepath):

    connection = sqlite3.connect('name.db')
    cursor = connection.cursor()

    # Create database objects
    cursor.execute('''CREATE TABLE IF NOT EXISTS names
                (name text, descr text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS occurances
                (name text, source text, reference text, sentence text, 
                    neg real, neu real, pos real, compound real)''')

    # Cleanup previous name occurance data if any
    cursor.execute('''
            delete from occurances where source = ?
        ''', (filepath,) )

    # iterate through the bible
    bible = json.load(open(filepath, "r"))
    for book in bible:
        print 'Processing: ' + book
        connection.commit()

        for chapter in bible[book]:
            for verse in bible[book][chapter]:
                
                # For each verse, insert sentiment analysis + name occurances into sqlite
                analysis = analyze_line(bible[book][chapter][verse])
                for name in analysis['names']:
                    cursor.execute('''
                        insert into occurances (name, source, reference, sentence, neg, neu, pos, compound) 
                        values (?,?,?,?,?,?,?,?)
                    ''', (
                        name,                               #name
                        filepath,                           #source
                        book + ' ' + chapter + ':' + verse, #reference
                        bible[book][chapter][verse],        #sentence
                        analysis['sentiment']['neg'],       #neg
                        analysis['sentiment']['neu'],       #neu
                        analysis['sentiment']['pos'],       #pos
                        analysis['sentiment']['compound']   #compound
                        ))



    # todo: Remove the trailing 's' for plural / possesive noun occurances

    # Delete false-positive nouns from the list.
    notnames = open("notnames.txt", "r") 
    for name in notnames:
        cursor.execute('delete from occurances where name = ?', (name,))

    # todo: Differenciate place names from person names.
    
    connection.commit()


# note: ESV.json has to be downloaded from : https://github.com/honza/bibles/blob/master/ESV/ESV.json
build_bible_namedb('ESV.json')
