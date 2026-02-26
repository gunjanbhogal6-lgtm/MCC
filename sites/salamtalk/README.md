# SalamTalk Frontend

SalamTalk business communication platform website built with Astro.

## Tech Stack

- **Framework**: Astro 5
- **Styling**: Tailwind CSS 4
- **Deployment**: Docker + Nginx

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
salamtalk/
├── src/
│   ├── components/     # Astro components
│   ├── pages/          # Route pages
│   ├── layouts/        # Page layouts
│   ├── data/           # SEO data (seo.json)
│   └── styles/         # Global styles
├── public/             # Static assets
├── Dockerfile          # Docker configuration
└── nginx.conf          # Nginx config for production
```

## Pages

| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/about` | About page |
| `/features` | Features page |
| `/pricing` | Pricing page |
| `/contact` | Contact page |

## SEO Data

SEO metadata is stored in `src/data/seo.json` and is automatically updated by the AutoSEO pipeline.

## Deployment

Deployed as a separate service in Coolify with the following configuration:

- Build Pack: Dockerfile
- Port: 80
- Watch Paths: `sites/salamtalk/**`

## Contributing

See root README.md for project-wide contribution guidelines.
