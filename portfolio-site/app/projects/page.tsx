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
      title: 'Support Ticket RAG Assistant',
      status: 'complete' as const,
      description: 'Reads a customer question, finds the most useful help article, and prepares a reply for a support agent to review.',
      tags: ['Customer Support', 'Knowledge Search', 'Python', 'FastAPI'],
      metrics: [
        { label: 'Help Articles', value: '15' },
        { label: 'Topics', value: '4' },
        { label: 'Tests', value: '3/3' },
      ],
      link: '/projects/support-ticket-rag',
    },
    {
      id: 'level-progression-analysis',
      title: 'Level Progression & Difficulty Analysis',
      status: 'in-progress' as const,
      description: 'Explore where players struggle across levels using attempt-level synthetic telemetry, progression metrics, and an interactive dashboard.',
      tags: ['Game Analytics', 'Python', 'Polars', 'Streamlit', 'Product Analytics'],
      metrics: [],
      link: '/projects/level-progression-analysis',
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
