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
        <h2 className="text-2xl font-semibold mb-4">The Challenge</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Gaming companies lose players constantly. With a baseline churn rate of 63.6%, understanding who will leave 
          and why is crucial. But which model architecture works best for sequential player behavior? And once you can 
          predict churn, which interventions actually work?
        </p>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          I built a complete system to answer both questions: a model comparison framework to find the best predictor, 
          and an A/B testing simulator to validate retention strategies with statistical rigor.
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
        <h2 className="text-2xl font-semibold mb-4">Model Comparison: Finding the Best Architecture</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          I tested three different approaches to see what works best for predicting player churn:
        </p>
        
        <div className="space-y-4 mb-6">
          <div className="p-4 border-l-4 border-blue-500 bg-gray-50 dark:bg-gray-800">
            <h3 className="font-semibold mb-2">XGBoost: The Traditional Powerhouse</h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              Started with gradient boosting on 31 engineered features. Fast to train, easy to interpret, but treats each 
              player observation independently. AUC: 0.773.
            </p>
          </div>
          
          <div className="p-4 border-l-4 border-purple-500 bg-gray-50 dark:bg-gray-800">
            <h3 className="font-semibold mb-2">LSTM: Capturing Sequential Patterns</h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              Long Short-Term Memory networks can learn from 14-day behavior sequences. Better at capturing temporal 
              dependencies with 1.8M parameters. AUC: 0.780, but more complex.
            </p>
          </div>
          
          <div className="p-4 border-l-4 border-green-500 bg-green-50 dark:bg-green-900/20">
            <h3 className="font-semibold mb-2">🏆 GRU: The Winner</h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              Gated Recurrent Units matched LSTM performance (AUC: 0.780) with 24% fewer parameters (1.4M vs 1.8M). 
              Simpler architecture, faster training, same accuracy. This is the one I deployed.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3">Model</th>
                <th className="text-left p-3">AUC</th>
                <th className="text-left p-3">Precision</th>
                <th className="text-left p-3">Recall</th>
                <th className="text-left p-3">F1</th>
                <th className="text-left p-3">Parameters</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="p-3">XGBoost</td>
                <td className="p-3">0.773</td>
                <td className="p-3">0.770</td>
                <td className="p-3">0.969</td>
                <td className="p-3">0.858</td>
                <td className="p-3">-</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">LSTM</td>
                <td className="p-3">0.780</td>
                <td className="p-3">0.767</td>
                <td className="p-3">0.987</td>
                <td className="p-3">0.863</td>
                <td className="p-3">1.8M</td>
              </tr>
              <tr className="border-b bg-green-50 dark:bg-green-900/20">
                <td className="p-3 font-semibold">GRU (Selected)</td>
                <td className="p-3 font-semibold">0.780</td>
                <td className="p-3">0.765</td>
                <td className="p-3">0.988</td>
                <td className="p-3">0.863</td>
                <td className="p-3 font-semibold">1.4M</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <p className="text-sm">
            <span className="font-semibold">Key Insight:</span> Deep learning barely edges out XGBoost (+0.7% AUC), 
            but the recurrent models' ability to capture temporal patterns makes them more robust for sequential player behavior. 
            GRU wins on efficiency.
          </p>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">A/B Testing: What Actually Works?</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Predicting churn is one thing. Reducing it is another. I built a simulation framework to test 6 different 
          retention interventions with proper statistical methodology (chi-squared tests, 95% confidence, power analysis).
        </p>
        
        <div className="mb-6">
          <h3 className="font-semibold text-lg mb-4">The Experiments</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-lg border-2 border-green-500">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold text-green-800 dark:text-green-300">🏆 Tutorial Improvements</h4>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                    Enhanced onboarding with interactive elements
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-700 dark:text-green-400">-22.8%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">churn</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                p &lt; 0.0001 • 3,000 players • Most impactful
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold">Social Features</h4>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                    Friend invites with rewards
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-secondary">-16.2%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">churn</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                p &lt; 0.0001 • 1,800 players
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold">In-Game Rewards</h4>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                    Free items for returning players
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-secondary">-12.5%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">churn</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                p &lt; 0.0001 • 2,500 players
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold">Daily Login Bonus</h4>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                    Streak-based rewards
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-secondary">-10.8%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">churn</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                p = 0.0039 • 2,000 players
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold">Push Notifications</h4>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                    Day 3 re-engagement message
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-secondary">-9.7%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">churn</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                p = 0.0073 • 2,000 players
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border opacity-60">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold">Discount Offer</h4>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                    20% off in-game purchases
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold">-8.4%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">churn</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                p = 0.0529 • Not significant
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg border-2 border-blue-300 dark:border-blue-700">
          <h3 className="font-bold text-lg mb-3">The Story in the Data</h3>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">→</span>
              <span><strong>Onboarding matters most:</strong> Tutorial improvements had nearly double the impact of any other intervention. First impressions are everything.</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">→</span>
              <span><strong>Social beats monetary:</strong> Friend invites (-16.2%) outperformed discounts (-8.4%, not even significant). Players stay for community, not savings.</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 dark:text-blue-400 mr-2">→</span>
              <span><strong>Statistical rigor matters:</strong> 5 out of 6 tests were significant (p &lt; 0.05), but one wasn't. Power analysis ensured reliable results.</span>
            </li>
          </ul>
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
