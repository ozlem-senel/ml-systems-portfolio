import Link from 'next/link'
import Image from 'next/image'

const metrics = [
  { title: 'Progression', text: 'Track how many observed players reach and complete each level.' },
  { title: 'Difficulty', text: 'Compare first-attempt wins, retry counts, and uncertainty across levels.' },
  { title: 'Abandonment', text: 'Identify players who do not complete a level after a defined observation window.' },
]

export default function LevelProgressionPage() {
  return (
    <main className="container mx-auto px-4 py-16 max-w-5xl">
      <nav aria-label="Breadcrumb" className="text-sm text-gray-600 dark:text-gray-400 mb-8">
        <Link href="/projects" className="hover:text-primary">Projects</Link>
        <span className="mx-2">/</span>
        <span>Level Progression</span>
      </nav>

      <header className="mb-14">
        <span className="inline-block rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 px-4 py-1.5 text-sm font-semibold mb-5">In Progress</span>
        <h1 className="text-4xl md:text-5xl font-bold mb-5">Level Progression &amp; Difficulty Analysis</h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed max-w-3xl">
          Analyzing player journeys to find where a game&apos;s levels may create friction.
        </p>
      </header>

      <section className="mb-14">
        <h2 className="text-2xl font-bold mb-4">The question</h2>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          Which levels do players reach, where do they need more attempts, and which levels deserve a closer look?
          This project turns game events into player-level metrics that can support a game design investigation.
        </p>
      </section>

      <section className="mb-14">
        <h2 className="text-2xl font-bold mb-6">What the analysis covers</h2>
        <div className="grid md:grid-cols-3 gap-5">
          {metrics.map((item) => (
            <article key={item.title} className="rounded-2xl border border-gray-200 dark:border-gray-700 p-6 bg-gray-50 dark:bg-gray-800/40">
              <h3 className="font-semibold text-lg mb-3">{item.title}</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="mb-14">
        <h2 className="text-2xl font-bold mb-4">From events to insight</h2>
        <ol className="space-y-4 text-gray-700 dark:text-gray-300 leading-relaxed list-decimal pl-6">
          <li>Generate synthetic game events with matching IDs for level starts and outcomes.</li>
          <li>Clean and prepare the events with the game analytics pipeline.</li>
          <li>Calculate reach, completion, first-attempt wins, retries, and seven-day level abandonment.</li>
          <li>Explore selected dates and levels in the shared Streamlit dashboard, with player counts and confidence intervals for first-attempt wins.</li>
        </ol>
      </section>

      <section className="mb-14">
        <h2 className="text-3xl font-bold mb-3">A simulated player journey</h2>
        <p className="text-gray-600 dark:text-gray-300 leading-relaxed mb-8">
          One 70-day sample contains 1,200 observed players and 373,656 events. These figures describe simulated data, not live game outcomes.
        </p>
        <div className="space-y-10">
          <figure>
            <Image src="/projects/level-progression/difficulty-curve.png" alt="First-attempt win rate across levels 1 to 50, with visible drops at simulated levels 12, 25 and 40" width={1500} height={630} className="rounded-xl border border-gray-200 w-full h-auto" />
            <figcaption className="mt-3 text-gray-600 dark:text-gray-400 leading-relaxed">The generator deliberately makes levels 12, 25 and 40 harder. A first-win gap relative to nearby levels puts all three in the top 10 levels to investigate in this sample. This is an in-sample sanity check, not independent validation.</figcaption>
          </figure>
          <figure>
            <Image src="/projects/level-progression/level-12-funnel.png" alt="Level 12 progression: 967 started, 954 completed, and 932 started level 13" width={1200} height={600} className="rounded-xl border border-gray-200 w-full h-auto" />
            <figcaption className="mt-3 text-gray-600 dark:text-gray-400 leading-relaxed">Of 967 players who started level 12, 954 completed it and 932 then started level 13 before the observation cutoff. These counts do not impose a fixed completion window.</figcaption>
          </figure>
          <figure>
            <Image src="/projects/level-progression/retry-rate.png" alt="Percentage of players with a mature first failure who retried within seven days for levels 12, 25 and 40" width={1200} height={600} className="rounded-xl border border-gray-200 w-full h-auto" />
            <figcaption className="mt-3 text-gray-600 dark:text-gray-400 leading-relaxed">At level 12, 403 of 413 eligible players retried within seven days. Retry rates are high in this generator; they should not be interpreted as real-world behavior.</figcaption>
          </figure>
        </div>
      </section>

      <section className="mb-14">
        <h2 className="text-2xl font-bold mb-4">From finding to experiment</h2>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">Level 12 is a candidate for investigation: its first-attempt win rate is 54.2%, compared with 77.8% across nearby eligible levels. One hypothesis is that players need a clearer hint. A proposed player-randomized test would compare the current level with a hint, using completion within 24 hours as the primary metric and later progression as a guardrail. This is a test plan, not an observed treatment effect.</p>
      </section>

      <section className="mb-14 rounded-2xl border border-blue-200 dark:border-blue-900 bg-blue-50 dark:bg-blue-950/30 p-6">
        <h2 className="text-xl font-semibold mb-3">How to interpret the results</h2>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          The data is simulated, including designed difficulty spikes. The charts demonstrate the analytical workflow rather than real player behavior.
          Completion rates depend on the observation window, and an association between difficulty and abandonment does not establish causation.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Technology</h2>
        <div className="flex flex-wrap gap-2">
          {['Python', 'Pandas', 'Polars', 'Streamlit', 'Plotly', 'pytest'].map((tag) => (
            <span key={tag} className="px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300">{tag}</span>
          ))}
        </div>
      </section>

      <div className="flex flex-wrap gap-4">
        <a href="https://github.com/ozlem-senel/ml-systems-portfolio/tree/main/04-level-progression-analysis" target="_blank" rel="noreferrer" className="px-6 py-3 rounded-xl bg-primary text-white font-medium">View project on GitHub</a>
        <a href="https://github.com/ozlem-senel/ml-systems-portfolio/blob/main/04-level-progression-analysis/ANALYSIS_REPORT.md" target="_blank" rel="noreferrer" className="px-6 py-3 rounded-xl border border-gray-300 dark:border-gray-600 font-medium hover:border-primary">Read analysis report</a>
        <Link href="/projects/event-analytics-pipeline" className="px-6 py-3 rounded-xl border border-gray-300 dark:border-gray-600 font-medium hover:border-primary">Explore the event pipeline</Link>
      </div>
    </main>
  )
}
