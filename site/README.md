# Biblical Names Database - Static Site

A modern, fast, and accessible static website for exploring Biblical names with sentiment analysis.

## Features

- **Search**: Real-time search through all Biblical names
- **Filter by Sentiment**: View names with positive, negative, or neutral sentiment
- **Sort Options**: Sort by name (A-Z), frequency, or sentiment score
- **Detailed Views**: Click any name to see all verses where it appears
- **Dark/Light Mode**: Toggle between themes with preference persistence
- **Mobile Responsive**: Fully responsive design works on all devices
- **Static Generation**: No backend required, fast loading times
- **Lazy Loading**: Individual name data loads only when needed

## Tech Stack

- **SvelteKit** with static adapter for SSG
- **Tailwind CSS** for styling
- **TypeScript** for type safety
- **Svelte 5 Runes** for reactive state management

## Development

### Prerequisites

- Node.js 18+ and npm

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:5173
```

### Building for Production

```bash
# Build static site
npm run build

# Preview production build
npm run preview
```

The built site will be in the `build/` directory, ready to deploy to any static hosting service.

## Deployment

This static site can be deployed to:

- **GitHub Pages**: Push the `build` folder
- **Netlify**: Connect your repo and deploy
- **Vercel**: Import your project
- **Any static host**: Upload the `build` folder

## Data Structure

### Summary Data (`/data/names-summary.json`)
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

### Individual Name Data (`/data/names/{name}.json`)
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

## Project Structure

```
site/
├── src/
│   ├── lib/
│   │   ├── stores/
│   │   │   └── theme.ts          # Dark/light mode store
│   │   └── types.ts               # TypeScript interfaces
│   ├── routes/
│   │   ├── +layout.svelte         # Root layout
│   │   ├── +layout.ts             # Prerender config
│   │   ├── +page.svelte           # Homepage with listing
│   │   ├── +page.ts               # Load names summary
│   │   └── name/
│   │       └── [slug]/
│   │           ├── +page.svelte   # Individual name page
│   │           └── +page.ts       # Load name details
│   └── app.css                    # Tailwind directives
├── static/
│   └── data/                      # JSON data files
└── svelte.config.js               # SvelteKit config
```

## License

MIT
