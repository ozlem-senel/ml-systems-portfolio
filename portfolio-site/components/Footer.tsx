import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="border-t mt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="font-semibold mb-3">Özlem Senel</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              ML Engineer & Data Scientist specializing in production systems for gaming analytics
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-3">Projects</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/projects/player-churn-retention" className="text-gray-600 dark:text-gray-400 hover:text-primary">
                  Player Churn System
                </Link>
              </li>
              <li>
                <Link href="/projects/event-analytics-pipeline" className="text-gray-600 dark:text-gray-400 hover:text-primary">
                  Event Analytics Pipeline
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-3">Connect</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link 
                  href="https://github.com/ozlem-senel" 
                  target="_blank"
                  className="text-gray-600 dark:text-gray-400 hover:text-primary"
                >
                  GitHub
                </Link>
              </li>
              <li>
                <Link 
                  href="https://linkedin.com/in/ozlem-senel" 
                  target="_blank"
                  className="text-gray-600 dark:text-gray-400 hover:text-primary"
                >
                  LinkedIn
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t text-center text-sm text-gray-600 dark:text-gray-400">
          © 2026 Özlem Senel. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
