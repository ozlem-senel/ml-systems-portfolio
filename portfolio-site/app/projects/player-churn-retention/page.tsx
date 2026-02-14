import Link from 'next/link'

export default function ChurnRetentionPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl">
      <nav className="text-sm text-gray-600 dark:text-gray-400 mb-8">
        <Link href="/" className="hover:text-primary">Home</Link>
        {' > '}
        <Link href="/projects" className="hover:text-primary">Projects</Link>
        {' > '}
        <span>Player Churn & Retention</span>
      </nav>

      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Player Churn & Retention System</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="px-3 py-1 bg-secondary text-white rounded-full">Complete</span>
          <span className="text-gray-600 dark:text-gray-400">Last Updated: February 2026</span>
        </div>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Overview</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Comprehensive churn prediction system comparing traditional ML (XGBoost) with deep learning approaches (LSTM, GRU). 
          Includes an experimental framework for testing retention interventions through A/B testing simulation.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Key Metrics</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-primary mb-2">0.780</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Best Model AUC (GRU)</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-secondary mb-2">22.8%</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Churn Reduction (A/B Test)</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-accent mb-2">31</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Engineered Features</div>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">What I Built</h2>
        <ul className="space-y-3">
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Realistic player behavior data generator: 10K players, 135K observations, 63.6% churn rate</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>31 engineered features including aggregations, recency metrics, and behavioral trends</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Three trained models: XGBoost (0.773 AUC), LSTM (0.780 AUC), GRU (0.780 AUC - selected)</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>A/B testing simulator with 6 retention interventions tested</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Comprehensive model comparison framework with ROC/PR curves</span>
          </li>
        </ul>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Model Comparison</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3">Model</th>
                <th className="text-left p-3">AUC</th>
                <th className="text-left p-3">Precision</th>
                <th className="text-left p-3">Recall</th>
                <th className="text-left p-3">F1</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="p-3">XGBoost</td>
                <td className="p-3">0.773</td>
                <td className="p-3">0.719</td>
                <td className="p-3">0.719</td>
                <td className="p-3">0.719</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">LSTM</td>
                <td className="p-3">0.780</td>
                <td className="p-3">0.731</td>
                <td className="p-3">0.706</td>
                <td className="p-3">0.718</td>
              </tr>
              <tr className="border-b bg-green-50 dark:bg-green-900/20">
                <td className="p-3 font-semibold">GRU (Selected)</td>
                <td className="p-3 font-semibold">0.780</td>
                <td className="p-3">0.732</td>
                <td className="p-3">0.702</td>
                <td className="p-3">0.717</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-4">
          GRU selected as best model: matches LSTM performance with 24% fewer parameters (1.4M vs 1.8M)
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">A/B Testing Results</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Tested 6 retention interventions. Most effective: Tutorial improvements showing 22.8% churn reduction (p &lt; 0.001).
        </p>
        <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Implementation Priority</h3>
          <ol className="list-decimal list-inside space-y-1 text-sm">
            <li>Tutorial improvements (22.8% reduction)</li>
            <li>Loyalty rewards (16.2% reduction)</li>
            <li>Push notifications (12.5% reduction)</li>
          </ol>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Tech Stack</h2>
        <div className="flex flex-wrap gap-2">
          {['Python', 'PyTorch', 'XGBoost', 'scikit-learn', 'Polars', 'Matplotlib', 'Seaborn'].map((tech) => (
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
            href="https://github.com/ozlem-senel/ml-systems-portfolio/tree/main/01-player-churn-retention"
            target="_blank"
            className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-600 transition"
          >
            View on GitHub
          </Link>
          <Link 
            href="https://github.com/ozlem-senel/ml-systems-portfolio/blob/main/01-player-churn-retention/AB_TESTING_SUMMARY.md"
            target="_blank"
            className="px-4 py-2 border border-primary text-primary rounded hover:bg-blue-50 dark:hover:bg-gray-800 transition"
          >
            A/B Testing Report
          </Link>
        </div>
      </section>
    </div>
  )
}
