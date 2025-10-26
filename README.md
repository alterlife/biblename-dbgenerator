# Biblical Name Database Generator

Extracts names from the Bible and analyzes the sentiment of verses where they appear using NLTK's VADER sentiment analysis. Generates both an SQLite database and JSON files for a modern static website.

## Features

### Python Data Generator (`donlp.py`)
- Extracts proper nouns (names) from Biblical text using NLTK part-of-speech tagging
- Performs sentiment analysis on each verse using VADER
- Outputs to both SQLite database and JSON files
- Filters false positives using a customizable word list

### Static Website (`site/`)
- Modern, responsive SvelteKit static site
- Real-time search and filtering
- Dark/light mode toggle
- Lazy-loaded detailed views
- Mobile-friendly design
- Zero backend dependencies

## Quick Start

### 1. Generate the Data

#### Prerequisites
- Python 3.7+
- NLTK library

```bash
# Install dependencies
pip install -r requirements.txt

# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('vader_lexicon')"

# Download the ESV Bible JSON
# Get it from: https://github.com/honza/bibles/blob/master/ESV/ESV.json
# Place it in the root directory as ESV.json

# Run the generator
python donlp.py
```

This will:
- Create `name.db` SQLite database
- Export `site/static/data/names-summary.json` (all names with stats)
- Export `site/static/data/names/*.json` (individual name files)

### 2. Run the Website

```bash
cd site
npm install
npm run dev
```

Visit `http://localhost:5173` to see the site.

### 3. Build for Production

```bash
cd site
npm run build
```

Deploy the `build/` folder to any static hosting service (GitHub Pages, Netlify, Vercel, etc.)

## Project Structure

```
biblename-dbgenerator/
├── donlp.py              # Main Python script
├── requirements.txt      # Python dependencies
├── notnames.txt         # False positive filter list
├── name.db              # SQLite database output
├── ESV.json             # Bible source (download separately)
└── site/                # SvelteKit static site
    ├── src/
    │   ├── lib/
    │   │   ├── stores/
    │   │   │   └── theme.ts
    │   │   └── types.ts
    │   └── routes/
    │       ├── +page.svelte          # Homepage
    │       └── name/[slug]/
    │           └── +page.svelte      # Name detail pages
    ├── static/
    │   └── data/                     # Generated JSON files
    └── package.json
```

## Data Format

### SQLite Database
Two tables:
- `names`: Name definitions (currently unused)
- `occurances`: Each verse where a name appears with sentiment scores

### JSON Export

**Summary** (`names-summary.json`):
```json
[
  {
    "name": "Abraham",
    "count": 175,
    "sentiment": {
      "neg": 0.023,
      "neu": 0.876,
      "pos": 0.101,
      "compound": 0.234
    }
  }
]
```

**Individual Names** (`names/{name}.json`):
```json
{
  "name": "Abraham",
  "verses": [
    {
      "reference": "Genesis 12:1",
      "verse": "Now the LORD said to Abram...",
      "sentiment": {
        "neg": 0.0,
        "neu": 0.8,
        "pos": 0.2,
        "compound": 0.4
      }
    }
  ]
}
```

## Known Limitations

The original extraction has some known issues:

1. **Plural/Possessive Forms**: Singular and plural variants of the same name are recognized as different names (e.g., "Abraham" vs "Abraham's")
2. **False Positives**: NLTK detects many common words as proper nouns. A filter list (`notnames.txt`) helps, but more curation may be needed
3. **Sentiment Accuracy**: VADER is trained on modern social media text, not Biblical English, so sentiment scores may not always be accurate
4. **No Name Classification**: The system doesn't differentiate between people, places, and other proper nouns

## Improving the Data

### Add False Positives to Filter
Edit `notnames.txt` and add one word per line (case-sensitive):
```
Accordingly
Afterward
Against
```

### Customize Output
Modify `donlp.py`:
- Change `export_json_data('site/static/data')` path
- Adjust sentiment thresholds
- Add custom processing logic

## Technology Stack

### Backend/Data Processing
- Python 3
- NLTK for NLP
- VADER for sentiment analysis
- SQLite for database storage

### Frontend
- SvelteKit 2 with static adapter
- TypeScript
- Tailwind CSS
- Svelte 5 runes for reactivity

## Original Site

The original list of names was hosted at: http://namedb.herokuapp.com (may no longer be active)

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome! Areas for improvement:
- Better name extraction algorithms
- Improved sentiment analysis for Biblical text
- Plural/possessive name normalization
- Classification of people vs places
- Additional Bible translations
