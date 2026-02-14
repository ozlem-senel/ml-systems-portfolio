import Link from 'next/link'

export default function SupportTicketRAGPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl">
      <nav className="text-sm text-gray-600 dark:text-gray-400 mb-8">
        <Link href="/" className="hover:text-primary">Home</Link>
        {' > '}
        <Link href="/projects" className="hover:text-primary">Projects</Link>
        {' > '}
        <span>Support Ticket RAG</span>
      </nav>

      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Support Ticket RAG System</h1>
        <div className="flex items-center gap-4 text-sm">
          <span className="px-3 py-1 bg-secondary text-white rounded-full">Complete</span>
          <span className="text-gray-600 dark:text-gray-400">Last Updated: February 2026</span>
        </div>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Overview</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          AI-powered support ticket processing using Retrieval-Augmented Generation with semantic search and LLM integration. 
          The system automatically classifies tickets, retrieves relevant knowledge base articles, and generates context-aware responses.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Key Metrics</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-primary mb-2">&lt;1 sec</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Processing Time per Ticket</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-secondary mb-2">100%</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Classification Accuracy</div>
          </div>
          <div className="p-6 border rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-3xl font-bold text-accent mb-2">0.78</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Avg Similarity Score</div>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">What I Built</h2>
        <ul className="space-y-3">
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>500 synthetic support tickets across 4 categories: payment, bugs, features, accounts</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>15 curated knowledge base documents with solutions and best practices</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Vector embeddings with sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>RAG pipeline with 3 LLM options: Mock templates, OpenAI GPT, Google Gemini</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>FastAPI endpoint with automatic OpenAPI documentation</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Real-time AI response generation using Gemini 2.5 Flash (free tier)</span>
          </li>
        </ul>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Architecture</h2>
        <div className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg font-mono text-sm">
          <pre className="overflow-x-auto">
{`Support Ticket → Embeddings → Vector Search → Top-K Docs → LLM → Response
                    ↓                           ↓
              Knowledge Base              Classification`}
          </pre>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Features</h2>
        <div className="space-y-2">
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Semantic search using sentence-transformers for vector embeddings
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Multiple LLM support: Mock (templates), OpenAI GPT, Google Gemini
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            RESTful API with FastAPI for easy integration
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            High performance: processes tickets in under 1 second
          </div>
          <div className="p-3 border-l-4 border-secondary bg-gray-50 dark:bg-gray-800">
            Free tier option with Gemini API (1500 requests/day)
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Dataset Distribution</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3">Category</th>
                <th className="text-left p-3">Tickets</th>
                <th className="text-left p-3">Percentage</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="p-3">Payment Issues</td>
                <td className="p-3">130</td>
                <td className="p-3">26.0%</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">Bug Reports</td>
                <td className="p-3">129</td>
                <td className="p-3">25.8%</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">Feature Requests</td>
                <td className="p-3">132</td>
                <td className="p-3">26.4%</td>
              </tr>
              <tr className="border-b">
                <td className="p-3">Account Management</td>
                <td className="p-3">109</td>
                <td className="p-3">21.8%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Technical Stack</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">Embeddings</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">sentence-transformers (all-MiniLM-L6-v2)</p>
          </div>
          <div className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">Vector Store</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">scikit-learn NearestNeighbors</p>
          </div>
          <div className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">LLM</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">Google Gemini 2.5 Flash (free tier)</p>
          </div>
          <div className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">API Framework</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">FastAPI + uvicorn</p>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Skills Demonstrated</h2>
        <div className="flex flex-wrap gap-2">
          {['RAG', 'LLMs', 'Semantic Search', 'Vector Embeddings', 'FastAPI', 'NLP', 
            'API Design', 'Google Gemini', 'sentence-transformers'].map((skill) => (
            <span key={skill} className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded">
              {skill}
            </span>
          ))}
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">How to Run & Test</h2>
        <div className="space-y-4">
          <div className="p-4 border-l-4 border-primary bg-gray-50 dark:bg-gray-800 rounded">
            <h3 className="font-semibold mb-2">1. Clone the Repository</h3>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block">
              git clone https://github.com/ozlem-senel/ml-systems-portfolio.git
            </code>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block mt-1">
              cd ml-systems-portfolio/02-support-ticket-rag
            </code>
          </div>
          
          <div className="p-4 border-l-4 border-primary bg-gray-50 dark:bg-gray-800 rounded">
            <h3 className="font-semibold mb-2">2. Install Dependencies</h3>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block">
              pip install -r requirements.txt
            </code>
          </div>

          <div className="p-4 border-l-4 border-primary bg-gray-50 dark:bg-gray-800 rounded">
            <h3 className="font-semibold mb-2">3. Configure LLM Provider (Optional)</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              The system works with mock responses by default. For AI-powered responses, create a .env file:
            </p>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block">
              LLM_PROVIDER=gemini
            </code>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block mt-1">
              GOOGLE_API_KEY=your-api-key-here
            </code>
          </div>

          <div className="p-4 border-l-4 border-primary bg-gray-50 dark:bg-gray-800 rounded">
            <h3 className="font-semibold mb-2">4. Start the API Server</h3>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block">
              python src/api.py
            </code>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
              Or with uvicorn:
            </p>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block mt-1">
              uvicorn src.api:app --reload --port 8000
            </code>
          </div>

          <div className="p-4 border-l-4 border-primary bg-gray-50 dark:bg-gray-800 rounded">
            <h3 className="font-semibold mb-2">5. Access the API</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Once running, visit:
            </p>
            <ul className="text-sm space-y-1">
              <li>• Interactive docs: <code className="bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded">http://localhost:8000/docs</code></li>
              <li>• Alternative docs: <code className="bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded">http://localhost:8000/redoc</code></li>
              <li>• Health check: <code className="bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded">http://localhost:8000/health</code></li>
            </ul>
          </div>

          <div className="p-4 border-l-4 border-primary bg-gray-50 dark:bg-gray-800 rounded">
            <h3 className="font-semibold mb-2">6. Test with cURL</h3>
            <code className="text-sm bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded block whitespace-pre-wrap">
              {`curl -X POST "http://localhost:8000/process" \\
  -H "Content-Type: application/json" \\
  -d '{
    "ticket_id": "TEST-001",
    "subject": "Payment failed",
    "description": "My credit card was declined"
  }'`}
            </code>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">API Endpoints</h2>
        <div className="space-y-4">
          <div className="p-4 border rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2 py-1 bg-green-600 text-white text-xs rounded">POST</span>
              <code className="text-sm">/process</code>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Process a support ticket and get AI-generated response</p>
          </div>
          <div className="p-4 border rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2 py-1 bg-blue-600 text-white text-xs rounded">GET</span>
              <code className="text-sm">/health</code>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Check API health status</p>
          </div>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Links</h2>
        <div className="flex gap-4">
          <a 
            href="https://github.com/ozlem-senel/ml-systems-portfolio/tree/main/02-support-ticket-rag"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-gray-800 text-white rounded hover:bg-gray-700 transition"
          >
            View on GitHub
          </a>
          <Link 
            href="/projects"
            className="px-6 py-3 border border-gray-300 rounded hover:bg-gray-50 dark:hover:bg-gray-800 transition"
          >
            All Projects
          </Link>
        </div>
      </section>
    </div>
  )
}
