# Portfolio Website Plan

## Overview
Create a professional Next.js website to showcase ML Systems Portfolio projects with interactive visualizations, code snippets, and live demos.

## Tech Stack

**Framework**: Next.js 14 (App Router)
- Server-side rendering for SEO
- Static generation for performance
- Built-in image optimization
- TypeScript support

**Styling**: Tailwind CSS + shadcn/ui
- Modern, responsive design
- Consistent component library
- Dark mode support
- Professional aesthetics

**Visualizations**: 
- Recharts for data viz
- React syntax highlighter for code
- Framer Motion for animations

**Deployment**: Vercel
- Free hosting for Next.js
- Automatic deployments from GitHub
- Global CDN
- Custom domain support

## Site Structure

```
Portfolio Site
├── Home Page
│   ├── Hero section (name, tagline, CTA)
│   ├── Skills overview (ML, Data Eng, Tools)
│   ├── Projects showcase (cards with status badges)
│   └── Contact/Links
│
├── Projects Page
│   ├── Project grid/list view
│   ├── Filter by status/tech/category
│   └── Search functionality
│
├── Project Detail Pages (Dynamic routes)
│   ├── /projects/player-churn-retention
│   │   ├── Overview & objectives
│   │   ├── Technical approach
│   │   ├── Key visualizations (model comparison, A/B tests)
│   │   ├── Code snippets (feature engineering, model training)
│   │   ├── Results & metrics
│   │   ├── Lessons learned
│   │   └── GitHub link
│   │
│   ├── /projects/event-analytics-pipeline
│   │   ├── Architecture diagram
│   │   ├── Performance benchmarks
│   │   ├── Dashboard screenshots
│   │   ├── Data quality framework
│   │   ├── Code highlights (ETL, quality checks)
│   │   └── Production deployment
│   │
│   └── /projects/[more projects]
│
├── About Page
│   ├── Professional summary
│   ├── Education & background
│   ├── Technical skills detailed
│   └── Career interests
```

## Page Designs

### Home Page
```
+------------------------------------------+
|  HEADER [Logo] [Projects] [About] [Contact] |
+------------------------------------------+
|                                          |
|  Hi, I'm Özlem Senel                     |
|  ML Engineer & Data Scientist             |
|  Building production ML systems           |
|                                          |
|  [View Projects] [Download Resume]       |
|                                          |
+------------------------------------------+
|                                          |
|  SKILLS                                  |
|  [ML] [Data Engineering] [MLOps]         |
|  Python • PyTorch • Polars • AWS         |
|                                          |
+------------------------------------------+
|                                          |
|  FEATURED PROJECTS                       |
|                                          |
|  +----------------+  +----------------+  |
|  | Churn System   |  | ETL Pipeline   |  |
|  | Complete       |  | Complete       |  |
|  | 0.780 AUC      |  | 112K evt/sec   |  |
|  +----------------+  +----------------+  |
|                                          |
+------------------------------------------+
```

### Project Detail Page
```
+------------------------------------------+
|  BREADCRUMB: Home > Projects > Churn     |
+------------------------------------------+
|                                          |
|  Player Churn & Retention System         |
|  Status: Complete | Feb 2026             |
|                                          |
|  [Overview] [Tech] [Results] [Code]      |
|                                          |
+------------------------------------------+
|                                          |
|  OVERVIEW                                |
|  Comprehensive churn prediction with...  |
|                                          |
|  KEY METRICS                             |
|  • 0.780 AUC (GRU model)                 |
|  • 22.8% churn reduction (A/B test)      |
|  • 31 engineered features                |
|                                          |
+------------------------------------------+
|                                          |
|  MODEL COMPARISON                        |
|  [Interactive ROC Curve Chart]           |
|                                          |
+------------------------------------------+
|                                          |
|  CODE HIGHLIGHT                          |
|  ```python                               |
|  class GRUChurnModel(nn.Module):         |
|      def __init__(self):                 |
|          ...                             |
|  ```                                     |
|                                          |
+------------------------------------------+
```


### Code Snippets to Highlight

**Project 1**
```python
# Feature engineering example
def create_aggregated_features(df):
    return df.group_by('player_id').agg([
        pl.col('session_duration').mean().alias('avg_session'),
        pl.col('levels_completed').sum().alias('total_levels'),
        # ... more features
    ])

# GRU model architecture
class GRUChurnModel(nn.Module):
    def __init__(self, input_size=10, hidden_size=64, num_layers=2):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        # ...
```

**Project 3**
```python
# Data quality check
def run_quality_checks(df: pl.DataFrame) -> List[str]:
    issues = []
    if len(df) < config['min_events']:
        issues.append(f"Only {len(df)} events (minimum: {config['min_events']})")
    # ... more checks
    return issues

# High-performance aggregation with Polars
daily_metrics = (
    df.group_by('date')
    .agg([
        pl.col('player_id').n_unique().alias('dau'),
        pl.col('prop_price_usd').sum().alias('revenue')
    ])
)
```

## Deployment Steps

1. **Create Next.js Project**
   ```bash
   npx create-next-app@latest portfolio-site --typescript --tailwind --app
   cd portfolio-site
   npm install
   ```

2. **Install Dependencies**
   ```bash
   npm install @shadcn/ui recharts framer-motion
   npm install react-syntax-highlighter @types/react-syntax-highlighter
   ```

3. **Set Up GitHub Repo**
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio site"
   git remote add origin https://github.com/ozlem-senel/portfolio-site
   git push -u origin main
   ```

4. **Deploy to Vercel**
   - Connect GitHub repo to Vercel
   - Configure build settings
   - Deploy with one click
   - Get URL: `https://ozlem-senel.vercel.app`

5. **Custom Domain** (Optional)
   - Purchase domain (e.g., ozlemsenel.com)
   - Configure DNS in Vercel
   - Enable SSL certificate

## Design Inspiration

**Color Palette** (Professional + Tech)
- Primary: #3B82F6 (Blue)
- Secondary: #10B981 (Green for success badges)
- Accent: #8B5CF6 (Purple for highlights)
- Background: #F9FAFB (Light) / #1F2937 (Dark)
- Text: #111827 (Light mode) / #F9FAFB (Dark mode)

**Typography**
- Headings: Inter (clean, modern)
- Body: System fonts for readability
- Code: JetBrains Mono

**Component Style**
- Cards with subtle shadows
- Rounded corners (8px)
- Smooth hover transitions
- Status badges with icons
- Gradient backgrounds for hero sections

## Example Component Structures

### Project Card Component
```typescript
interface Project {
  id: string;
  title: string;
  status: 'complete' | 'in-progress' | 'planned';
  description: string;
  tags: string[];
  metrics: { label: string; value: string }[];
  image: string;
  link: string;
}

export function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="card">
      <img src={project.image} alt={project.title} />
      <Badge status={project.status} />
      <h3>{project.title}</h3>
      <p>{project.description}</p>
      <div className="metrics">
        {project.metrics.map(m => (
          <span>{m.label}: {m.value}</span>
        ))}
      </div>
      <div className="tags">
        {project.tags.map(tag => <Tag>{tag}</Tag>)}
      </div>
      <Link href={project.link}>View Project →</Link>
    </div>
  );
}
```

### Interactive Chart Component
```typescript
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export function ROCCurve({ data }: { data: any[] }) {
  return (
    <LineChart data={data}>
      <XAxis dataKey="fpr" label="False Positive Rate" />
      <YAxis dataKey="tpr" label="True Positive Rate" />
      <Line type="monotone" dataKey="xgboost" stroke="#EF4444" />
      <Line type="monotone" dataKey="lstm" stroke="#3B82F6" />
      <Line type="monotone" dataKey="gru" stroke="#10B981" />
      <Tooltip />
    </LineChart>
  );
}
```