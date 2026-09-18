import Link from 'next/link'

const steps = [
  {
    number: '1',
    title: 'A customer asks for help',
    text: 'The system receives a short support message, such as “I forgot my password.”',
  },
  {
    number: '2',
    title: 'It finds the best instructions',
    text: 'It searches the company help articles and selects the information most related to the question.',
  },
  {
    number: '3',
    title: 'It prepares a useful reply',
    text: 'It labels the topic and urgency, then creates a reply based on the selected help article.',
  },
]

export default function SupportTicketRAGPage() {
  return (
    <main className="container mx-auto max-w-5xl px-4 py-12 md:py-16">
      <nav className="mb-10 text-sm text-gray-500 dark:text-gray-400" aria-label="Breadcrumb">
        <Link href="/projects" className="hover:text-primary">Projects</Link>
        <span className="mx-2" aria-hidden="true">/</span>
        <span>Support Assistant</span>
      </nav>

      <section className="mb-16 grid items-center gap-10 md:grid-cols-5">
        <div className="md:col-span-3">
          <div className="mb-5 flex flex-wrap gap-2">
            <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800 dark:bg-green-900/40 dark:text-green-200">
              Working project
            </span>
            <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800 dark:bg-blue-900/40 dark:text-blue-200">
              Runs locally for free
            </span>
          </div>
          <h1 className="mb-5 text-4xl font-bold leading-tight md:text-5xl">
            A faster first response for customer support
          </h1>
          <p className="mb-7 text-xl leading-relaxed text-gray-600 dark:text-gray-300">
            This assistant reads a customer&apos;s problem, finds the most useful help article,
            and prepares a clear reply for the support team.
          </p>
          <div className="flex flex-wrap gap-3">
            <a
              href="#example"
              className="rounded-lg bg-primary px-5 py-3 font-semibold text-white hover:opacity-90"
            >
              See an example
            </a>
            <a
              href="https://github.com/ozlem-senel/ml-systems-portfolio/tree/main/02-support-ticket-rag"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-lg border border-gray-300 px-5 py-3 font-semibold hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800"
            >
              View the code
            </a>
          </div>
        </div>

        <div className="md:col-span-2 rounded-2xl border border-blue-200 bg-blue-50 p-6 dark:border-blue-900 dark:bg-blue-950/30">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wide text-blue-700 dark:text-blue-300">
            In one sentence
          </p>
          <p className="text-lg leading-relaxed">
            It helps support agents answer common questions faster without searching through help documents by hand.
          </p>
        </div>
      </section>

      <section className="mb-16">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-primary">How it works</p>
        <h2 className="mb-8 text-3xl font-bold">Three simple steps</h2>
        <div className="grid gap-5 md:grid-cols-3">
          {steps.map((step) => (
            <article key={step.number} className="rounded-2xl border border-gray-200 p-6 dark:border-gray-700">
              <div className="mb-5 flex h-10 w-10 items-center justify-center rounded-full bg-primary font-bold text-white">
                {step.number}
              </div>
              <h3 className="mb-2 text-xl font-semibold">{step.title}</h3>
              <p className="leading-relaxed text-gray-600 dark:text-gray-400">{step.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="example" className="mb-16 scroll-mt-8">
        <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-primary">Example</p>
        <h2 className="mb-8 text-3xl font-bold">From customer message to suggested reply</h2>
        <div className="grid gap-5 md:grid-cols-2">
          <article className="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-900">
            <div className="mb-4 flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-full bg-orange-100 text-lg dark:bg-orange-900/40" aria-hidden="true">👤</span>
              <div>
                <p className="font-semibold">Customer message</p>
                <p className="text-sm text-gray-500">Incoming support ticket</p>
              </div>
            </div>
            <p className="rounded-xl bg-gray-100 p-4 text-lg dark:bg-gray-800">
              “I forgot my password and cannot sign in. What should I do?”
            </p>
          </article>

          <article className="rounded-2xl border border-green-200 bg-green-50 p-6 dark:border-green-900 dark:bg-green-950/30">
            <div className="mb-4 flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-full bg-green-200 text-lg dark:bg-green-900/60" aria-hidden="true">✓</span>
              <div>
                <p className="font-semibold">Suggested result</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Ready for an agent to review</p>
              </div>
            </div>
            <dl className="mb-4 grid grid-cols-2 gap-3 text-sm">
              <div><dt className="text-gray-500">Topic</dt><dd className="font-semibold">Account access</dd></div>
              <div><dt className="text-gray-500">Urgency</dt><dd className="font-semibold">Medium</dd></div>
            </dl>
            <p className="rounded-xl bg-white/80 p-4 leading-relaxed dark:bg-gray-900/60">
              Use “Forgot Password” on the sign-in page, enter your email, and follow the reset link. Check your spam folder if it does not arrive within ten minutes.
            </p>
          </article>
        </div>
      </section>

      <section className="mb-16 rounded-2xl bg-gray-100 p-7 dark:bg-gray-800 md:p-9">
        <h2 className="mb-6 text-3xl font-bold">What the project demonstrates</h2>
        <div className="grid gap-6 md:grid-cols-3">
          <div>
            <p className="mb-1 text-2xl font-bold text-primary">15</p>
            <p className="font-semibold">Help articles</p>
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">Used as the trusted source for answers.</p>
          </div>
          <div>
            <p className="mb-1 text-2xl font-bold text-primary">4</p>
            <p className="font-semibold">Support topics</p>
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">Payments, bugs, accounts, and feature requests.</p>
          </div>
          <div>
            <p className="mb-1 text-2xl font-bold text-primary">3</p>
            <p className="font-semibold">Automated checks</p>
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">Confirm the main workflow and input validation work.</p>
          </div>
        </div>
      </section>

      <section className="mb-16">
        <h2 className="mb-6 text-3xl font-bold">Try it on your computer</h2>
        <p className="mb-6 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
          No paid account or API key is needed. After downloading the repository, open a terminal in the project folder and run:
        </p>
        <div className="overflow-x-auto rounded-2xl bg-gray-950 p-6 text-gray-100">
          <pre className="text-sm leading-7"><code>{`make setup
make run`}</code></pre>
        </div>
        <p className="mt-4 text-gray-600 dark:text-gray-400">
          Then open <code className="rounded bg-gray-100 px-2 py-1 dark:bg-gray-800">http://127.0.0.1:8000/docs</code> in your browser.
        </p>
      </section>

      <details className="mb-14 rounded-2xl border border-gray-200 p-6 dark:border-gray-700">
        <summary className="cursor-pointer text-xl font-semibold">Technical details for developers</summary>
        <div className="mt-5 space-y-4 text-gray-600 dark:text-gray-300">
          <p><strong className="text-gray-900 dark:text-white">Search:</strong> TF-IDF similarity finds relevant knowledge-base articles without downloading a large model.</p>
          <p><strong className="text-gray-900 dark:text-white">API:</strong> FastAPI provides the ticket-processing and health-check routes.</p>
          <p><strong className="text-gray-900 dark:text-white">Responses:</strong> Local templates work by default. OpenAI and Gemini are optional integrations.</p>
          <p><strong className="text-gray-900 dark:text-white">Tests:</strong> Pytest and FastAPI&apos;s test client validate the API without starting a separate server.</p>
        </div>
      </details>

      <Link href="/projects" className="font-semibold text-primary hover:underline">
        ← Back to all projects
      </Link>
    </main>
  )
}
