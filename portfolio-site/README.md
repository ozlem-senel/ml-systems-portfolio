# Portfolio Website

Next.js website showcasing ML Systems Portfolio projects.

## Getting Started

```bash
# Install dependencies (requires npm permissions to be fixed)
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view.

## Features

- Home page with hero section and project cards
- Individual project detail pages
- About page with skills and background
- Responsive design with Tailwind CSS
- Dark mode support

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Recharts (for future visualizations)
- Framer Motion (for animations)

## Deployment

Deploy to Vercel:

```bash
# Connect to Vercel
vercel

# Deploy
vercel --prod
```

## Note

Due to npm permission issues, dependencies need to be installed manually. Run:

```bash
sudo chown -R $(whoami) ~/.npm
npm install
```
