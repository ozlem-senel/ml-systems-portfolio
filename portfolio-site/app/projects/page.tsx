import ProjectCard from '@/components/ProjectCard'

export default function ProjectsPage() {
  const projects = [
    {
      id: 'player-churn-retention',
      title: 'Player Churn & Retention System',
      status: 'complete' as const,
      description: 'Comprehensive churn prediction with XGBoost, LSTM, and GRU models. Includes A/B testing framework showing 22.8% churn reduction through tutorial improvements.',
      tags: ['PyTorch', 'XGBoost', 'scikit-learn', 'Polars', 'Feature Engineering', 'A/B Testing'],
      metrics: [
        { label: 'Best Model AUC', value: '0.780' },
        { label: 'Churn Reduction', value: '22.8%' },
        { label: 'Features', value: '31' },
      ],
      link: '/projects/player-churn-retention',
    },
    {
      id: 'event-analytics-pipeline',
      title: 'Game Event Analytics Pipeline',
      status: 'complete' as const,
      description: 'Production ETL pipeline processing 940K events with comprehensive monitoring, 6 data quality checks, and interactive Streamlit dashboard.',
      tags: ['Polars', 'DuckDB', 'ETL', 'Streamlit', 'Data Engineering', 'pytest'],
      metrics: [
        { label: 'Throughput', value: '112K evt/sec' },
        { label: 'Quality Checks', value: '6' },
        { label: 'Events', value: '940K' },
      ],
      link: '/projects/event-analytics-pipeline',
    },
    {
      id: 'support-ticket-rag',
      title: 'Support Ticket RAG System',
      status: 'complete' as const,
      description: 'AI-powered support ticket processing using Retrieval-Augmented Generation with semantic search and LLM integration. Processes 500 tickets with multiple LLM options.',
      tags: ['RAG', 'LLMs', 'sentence-transformers', 'FastAPI', 'Gemini', 'Vector Search'],
      metrics: [
        { label: 'Response Time', value: '<1 sec' },
        { label: 'Classification', value: '100%' },
        { label: 'Tickets', value: '500' },
      ],
      link: '/projects/support-ticket-rag',
    },
    {
      id: 'ml-experiment-api',
      title: 'ML Experiment Tracking & Model API',
      status: 'planned' as const,
      description: 'Experiment tracking and model serving infrastructure with Docker containerization and AWS deployment for production MLOps.',
      tags: ['MLOps', 'FastAPI', 'Docker', 'AWS', 'Experiment Tracking'],
      metrics: [],
      link: '/projects/ml-experiment-api',
    },
  ]

  return (
    <div className="container mx-auto px-4 py-16">
      <h1 className="text-4xl font-bold mb-4">All Projects</h1>
      <p className="text-gray-600 dark:text-gray-400 mb-12 max-w-2xl">
        End-to-end machine learning and data engineering projects demonstrating production-ready systems.
      </p>

      <div className="grid md:grid-cols-2 gap-6">
        {projects.map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>
    </div>
  )
}
