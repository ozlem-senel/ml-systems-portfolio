import Link from 'next/link'

export default function EventAnalyticsPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl">
      <nav className="text-sm text-gray-600 dark:text-gray-400 mb-8">
        <Link href="/" className="hover:text-primary">Home</Link>
        {' > '}
        <Link href="/projects" className="hover:text-primary">Projects</Link>
        {' > '}
        <span>Event Analytics Pipeline</span>
      </nav>

      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Game Event Analytics Pipeline</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="px-3 py-1 bg-secondary text-white rounded-full">Complete</span>
          <span className="text-gray-600 dark:text-gray-400">Last Updated: February 2026</span>
        </div>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Overview</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          High-performance ETL pipeline for processing game event streams with production-grade monitoring, 
          error handling, and data quality validation. Processes 940K events in 8.4 seconds with comprehensive testing.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Key Metrics</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-primary mb-2">112K</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Events/Second Throughput</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-secondary mb-2">940K</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Events Processed</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-accent mb-2">6</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Quality Checks</div>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">What I Built</h2>
        <ul className="space-y-3">
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Event data generator: 5K players, 30 days, 8 event types across 5 behavioral segments</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Production ETL pipeline with 112K events/sec throughput using Polars lazy evaluation</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Data quality framework: 6 validation checks with configurable thresholds and strict mode</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Interactive Streamlit dashboard: DAU, revenue, retention metrics with date filtering</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Unit tests: 4 passing tests covering core ETL functionality with pytest</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>YAML-based configuration system with environment-specific settings</span>
          </li>
        </ul>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Architecture</h2>
        <div className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg font-mono text-sm">
          <pre className="overflow-x-auto">
{`Raw Events (JSONL) → Load & Validate → Clean & Enrich → Aggregate → Output (Parquet)
                           ↓                ↓               ↓
                    Quality Checks    Add Features    Metrics Calc
                    Error Handling      Logging      Retention Cohorts`}
          </pre>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Data Quality Framework</h2>
        <div className="space-y-2">
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Minimum event count validation (1,000 threshold)
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Required event type verification (session_start, session_end)
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Null percentage monitoring (10% threshold per column)
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Duplicate event detection
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Future timestamp detection (1 day threshold)
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Outlier detection (max revenue $1,000)
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Performance</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3">Metric</th>
                <th className="text-left p-3">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="p-3">Events Processed</td>
                <td className="p-3 font-semibold">940,324</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">Processing Time</td>
                <td className="p-3 font-semibold">8.4 seconds</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">Throughput</td>
                <td className="p-3 font-semibold">112,000 events/sec</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">Memory Usage</td>
                <td className="p-3 font-semibold">~500MB peak</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Tech Stack</h2>
        <div className="flex flex-wrap gap-2">
          {['Python', 'Polars', 'DuckDB', 'Streamlit', 'Plotly', 'PyYAML', 'pytest'].map((tech) => (
            <span key={tech} className="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-full text-sm">
              {tech}
            </span>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Links</h2>
        <div className="flex gap-4">
          <Link 
            href="https://github.com/ozlem-senel/ml-systems-portfolio/tree/main/03-event-analytics-pipeline"
            target="_blank"
            className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-600 transition"
          >
            View on GitHub
          </Link>
          <Link 
            href="https://github.com/ozlem-senel/ml-systems-portfolio/blob/main/03-event-analytics-pipeline/PRODUCTION.md"
            target="_blank"
            className="px-4 py-2 border border-primary text-primary rounded hover:bg-blue-50 dark:hover:bg-gray-800 transition"
          >
            Production Guide
          </Link>
        </div>
      </section>
    </div>
  )
}
