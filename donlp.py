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
import os
from collections import defaultdict
from pathlib import Path

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
    """Build SQLite database of biblical names with sentiment analysis."""

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
    with open(filepath, "r") as bible_file:
        bible = json.load(bible_file)

    for book in bible:
        print(f'Processing: {book}')
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
    with open("notnames.txt", "r") as notnames:
        for name in notnames:
            cursor.execute('delete from occurances where name = ?', (name.strip(),))

    # todo: Differenciate place names from person names.

    connection.commit()
    connection.close()


def export_json_data(output_dir='static/data'):
    """Export database to JSON files for static site generation.

    Creates:
    - names-summary.json: List of all names with counts and average sentiment
    - names/[name].json: Individual files with all verses for each name
    """

    # Create output directories
    output_path = Path(output_dir)
    names_path = output_path / 'names'
    output_path.mkdir(parents=True, exist_ok=True)
    names_path.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect('name.db')
    cursor = connection.cursor()

    # Get all unique names with their statistics
    cursor.execute('''
        SELECT
            name,
            COUNT(*) as count,
            AVG(neg) as avg_neg,
            AVG(neu) as avg_neu,
            AVG(pos) as avg_pos,
            AVG(compound) as avg_compound
        FROM occurances
        GROUP BY name
        ORDER BY count DESC
    ''')

    summary_data = []
    all_names = []

    for row in cursor.fetchall():
        name, count, avg_neg, avg_neu, avg_pos, avg_compound = row

        summary_data.append({
            'name': name,
            'count': count,
            'sentiment': {
                'neg': round(avg_neg, 3),
                'neu': round(avg_neu, 3),
                'pos': round(avg_pos, 3),
                'compound': round(avg_compound, 3)
            }
        })
        all_names.append(name)

    # Write summary file
    summary_file = output_path / 'names-summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary_data, f, indent=2)

    print(f'Exported summary with {len(summary_data)} names to {summary_file}')

    # Export individual name files
    for name in all_names:
        cursor.execute('''
            SELECT reference, sentence, neg, neu, pos, compound
            FROM occurances
            WHERE name = ?
            ORDER BY reference
        ''', (name,))

        verses = []
        for row in cursor.fetchall():
            reference, sentence, neg, neu, pos, compound = row
            verses.append({
                'reference': reference,
                'verse': sentence,
                'sentiment': {
                    'neg': round(neg, 3),
                    'neu': round(neu, 3),
                    'pos': round(pos, 3),
                    'compound': round(compound, 3)
                }
            })

        # Write individual name file
        name_file = names_path / f'{name.lower()}.json'
        with open(name_file, 'w') as f:
            json.dump({
                'name': name,
                'verses': verses
            }, f, indent=2)

    print(f'Exported {len(all_names)} individual name files to {names_path}')

    connection.close()


# note: ESV.json has to be downloaded from : https://github.com/honza/bibles/blob/master/ESV/ESV.json
build_bible_namedb('ESV.json')
export_json_data('site/static/data')
