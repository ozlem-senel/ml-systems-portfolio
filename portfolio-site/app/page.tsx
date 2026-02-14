import Link from 'next/link'
import ProjectCard from '@/components/ProjectCard'

export default function Home() {
  const projects = [
    {
      id: 'player-churn-retention',
      title: 'Player Churn & Retention System',
      status: 'complete' as const,
      description: 'Comprehensive churn prediction with XGBoost, LSTM, and GRU models. Includes A/B testing framework showing 22.8% churn reduction.',
      tags: ['PyTorch', 'XGBoost', 'Feature Engineering', 'A/B Testing'],
      metrics: [
        { label: 'Best Model AUC', value: '0.780' },
        { label: 'Churn Reduction', value: '22.8%' },
        { label: 'Features Engineered', value: '31' },
      ],
      link: '/projects/player-churn-retention',
    },
    {
      id: 'event-analytics-pipeline',
      title: 'Game Event Analytics Pipeline',
      status: 'complete' as const,
      description: 'Production ETL pipeline processing 940K events with comprehensive monitoring, data quality checks, and interactive dashboard.',
      tags: ['Polars', 'ETL', 'Data Engineering', 'Streamlit'],
      metrics: [
        { label: 'Throughput', value: '112K evt/sec' },
        { label: 'Quality Checks', value: '6' },
        { label: 'Events Processed', value: '940K' },
      ],
      link: '/projects/event-analytics-pipeline',
    },
    {
      id: 'support-ticket-rag',
      title: 'Support Ticket RAG System',
      status: 'complete' as const,
      description: 'AI-powered ticket processing with RAG using semantic search and LLM integration. Processes tickets in <1 second with 100% classification accuracy.',
      tags: ['RAG', 'LLMs', 'FastAPI', 'Gemini', 'sentence-transformers'],
      metrics: [
        { label: 'Response Time', value: '<1 sec' },
        { label: 'Classification', value: '100%' },
        { label: 'Similarity Score', value: '0.78' },
      ],
      link: '/projects/support-ticket-rag',
    },
    {
      id: 'ml-experiment-api',
      title: 'ML Experiment Tracking & Model API',
      status: 'planned' as const,
      description: 'Experiment tracking and model serving infrastructure with Docker containerization and AWS deployment.',
      tags: ['MLOps', 'FastAPI', 'Docker', 'AWS'],
      metrics: [],
      link: '/projects/ml-experiment-api',
    },
  ]

  return (
    <div className="container mx-auto px-4 py-16">
      {/* Hero Section */}
      <section className="text-center mb-20">
        <h1 className="text-5xl font-bold mb-4">
          Hi, I'm Özlem Senel
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
          ML Engineer & Data Scientist
        </p>
        <p className="text-lg text-gray-700 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
          Building production ML systems for gaming analytics and AI applications. Specializing in churn prediction, 
          RAG systems, event processing pipelines, and end-to-end data science workflows.
        </p>
        <div className="flex gap-4 justify-center">
          <Link 
            href="/projects" 
            className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
          >
            View Projects
          </Link>
          <Link 
            href="https://github.com/ozlem-senel/ml-systems-portfolio" 
            target="_blank"
            className="border border-primary text-primary px-6 py-3 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-800 transition"
          >
            GitHub
          </Link>
        </div>
      </section>

      {/* Skills Section */}
      <section className="mb-20">
        <h2 className="text-3xl font-bold mb-8 text-center">Technical Skills</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg">
            <h3 className="text-xl font-semibold mb-3">Machine Learning</h3>
            <p className="text-gray-600 dark:text-gray-400">
              PyTorch, XGBoost, scikit-learn, RAG, LLMs, Vector Embeddings, Feature Engineering
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h3 className="text-xl font-semibold mb-3">Data Engineering</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Polars, DuckDB, ETL Pipelines, Data Quality, Performance Optimization
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h3 className="text-xl font-semibold mb-3">MLOps</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Production Monitoring, Testing, Logging, Configuration Management
            </p>
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section>
        <h2 className="text-3xl font-bold mb-8 text-center">Featured Projects</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </section>
    </div>
  )
}
