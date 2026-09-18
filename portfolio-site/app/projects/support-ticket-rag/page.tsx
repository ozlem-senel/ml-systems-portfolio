import Link from 'next/link'
import TicketDemo from './TicketDemo'

export default function SupportTicketRAGPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl">
      <nav className="text-sm text-gray-600 dark:text-gray-400 mb-8">
        <Link href="/" className="hover:text-primary">Home</Link>
        {' > '}
        <Link href="/projects" className="hover:text-primary">Projects</Link>
        {' > '}
        <span>Support Ticket Assistant</span>
      </nav>

      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Support Ticket Assistant</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="px-3 py-1 bg-secondary text-white rounded-full">Complete</span>
          <span className="text-gray-600 dark:text-gray-400">Last Updated: September 2026</span>
        </div>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">The Challenge</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Support teams answer the same kinds of questions every day: failed payments,
          password resets, account access, and app problems. The answer is often already
          documented, but finding the right article and writing a reply still takes time.
        </p>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          I built a small assistant that does the first pass. It reads the ticket, finds the
          most relevant help article, identifies the topic and urgency, and drafts a response
          for a support agent to review.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Project at a Glance</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-primary mb-2">15</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Help Articles</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-secondary mb-2">4</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Support Topics</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-accent mb-2">3/3</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Automated Tests Passing</div>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">What I Built</h2>
        <ul className="space-y-3">
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>A searchable help centre covering payments, bugs, accounts, and feature requests</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>A ticket classifier that suggests a topic and urgency level</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>A response generator that bases its answer on the selected help article</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>A simple API that can be tried from the browser</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Automated tests for the main workflow, health check, and invalid requests</span>
          </li>
        </ul>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">How It Works</h2>
        <div className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg font-mono text-sm">
          <pre className="overflow-x-auto">
{`Customer message → Find a relevant help article → Draft a response
                           ↓
                 Suggest topic and urgency`}
          </pre>
        </div>
        <p className="text-gray-700 dark:text-gray-300 mt-4">
          The generated reply is a suggestion, not an automatic final answer. A support agent
          can review and edit it before sending it to the customer.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Try It</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Choose an example or write your own support message. The form sends it to the
          Python API and displays the generated result below.
        </p>
        <TicketDemo />
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Why I Made These Choices</h2>
        <div className="space-y-2">
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            It runs locally by default, so the project can be tested without an API key or paid account.
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            The search index is created automatically, which keeps setup to two commands.
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            OpenAI and Gemini are optional rather than required, so the basic workflow remains easy to reproduce.
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Run It Locally</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          After cloning the repository, open the project folder and run:
        </p>
        <div className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg font-mono text-sm">
          <pre className="overflow-x-auto"><code>{`make setup
make run`}</code></pre>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-4">
          Then visit <code className="bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">http://127.0.0.1:8000/docs</code> to try a ticket in the browser.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Tech Stack</h2>
        <div className="flex flex-wrap gap-2">
          {['Python', 'FastAPI', 'scikit-learn', 'TF-IDF', 'pytest', 'OpenAI (optional)', 'Gemini (optional)'].map((tech) => (
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
            href="https://github.com/ozlem-senel/ml-systems-portfolio/tree/main/02-support-ticket-rag"
            target="_blank"
            className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-600 transition"
          >
            View on GitHub
          </Link>
          <Link
            href="/projects"
            className="px-4 py-2 border border-primary text-primary rounded hover:bg-blue-50 dark:hover:bg-gray-800 transition"
          >
            All Projects
          </Link>
        </div>
      </section>
    </div>
  )
}
