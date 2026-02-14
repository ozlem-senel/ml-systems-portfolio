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
    <div className="container mx-auto px-4 py-20">
      {/* Hero Section */}
      <section className="text-center mb-32 animate-fade-in">
        <h1 className="text-6xl md:text-7xl font-bold mb-6 mt-16 animate-slide-up">
          <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-green-600 bg-clip-text text-transparent">
            Özlem Senel
          </span>
        </h1>
        <p className="text-2xl text-gray-600 dark:text-gray-300 mb-4 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          ML Engineer & Data Scientist
        </p>
        <p className="text-lg text-gray-700 dark:text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '0.2s' }}>
          Specializing in machine learning, deep learning and LLM applications. Building production systems including 
          machine learning models, RAG systems and data pipelines. Using gaming data from my hobby to showcase 
          end-to-end ML workflows.
        </p>
        <div className="flex gap-4 justify-center animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <Link 
            href="/projects" 
            className="group relative px-8 py-4 bg-primary text-white rounded-xl font-medium overflow-hidden"
          >
            <span className="relative z-10">View Projects</span>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300" />
          </Link>
          <Link 
            href="https://github.com/ozlem-senel/ml-systems-portfolio" 
            target="_blank"
            className="group px-8 py-4 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-xl font-medium hover:border-primary hover:text-primary dark:hover:text-primary transition-all duration-300"
          >
            <span className="flex items-center gap-2">
              GitHub
              <svg className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </span>
          </Link>
        </div>
      </section>

      {/* About Me Section */}
      <section className="mb-32">
        <div className="max-w-4xl mx-auto">
          <div className="relative p-10 rounded-3xl border-2 border-gray-200 dark:border-gray-700 bg-gradient-to-br from-blue-50/50 via-purple-50/30 to-green-50/50 dark:from-gray-800/50 dark:via-gray-800/30 dark:to-gray-800/50 backdrop-blur-sm animate-fade-in">
            <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
              <div className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full text-sm font-semibold shadow-lg">
                About Me
              </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8 mt-4">
              <div>
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </span>
                  Education
                </h3>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <span className="font-semibold">TUM</span> - Master's in Management & Technology (AI/ML focus)
                </p>
                <p className="text-gray-700 dark:text-gray-300">
                  <span className="font-semibold">ITU</span> - B.S. Industrial Engineering
                </p>
              </div>

              <div>
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-500 to-blue-500 flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </span>
                  Experience
                </h3>
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  <span className="font-semibold">Siemens</span> - Data Analyst (ML & Cloud)
                </p>
                <p className="text-gray-700 dark:text-gray-300">
                  <span className="font-semibold">Otto Management</span> - Data Scientist
                </p>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-300 dark:border-gray-600">
              <p className="text-gray-700 dark:text-gray-300 text-center mb-6 leading-relaxed">
                Currently expanding expertise in <span className="font-semibold text-primary">deep learning</span> and <span className="font-semibold text-primary">LLM applications</span>, 
                with experience in PyTorch, AWS infrastructure, and production ML systems. Published research on AI in healthcare at System Dynamics Conference.
              </p>
              <div className="flex justify-center">
                <Link 
                  href="/about"
                  className="group inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-300"
                >
                  Learn More About Me
                  <svg className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section className="mb-32">
        <h2 className="text-4xl font-bold mb-12 text-center animate-slide-up">
          <span className="inline-block relative">
            Technical Skills
            <div className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-green-500 rounded-full" />
          </span>
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="group p-8 border-2 border-gray-200 dark:border-gray-700 rounded-2xl hover-lift hover:border-primary/50 transition-all duration-300 animate-slide-in-right" style={{ animationDelay: '0.1s' }}>
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-2xl font-semibold mb-4">Machine Learning</h3>
            <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
              PyTorch, XGBoost, scikit-learn, RAG, LLMs, Vector Embeddings, Feature Engineering
            </p>
          </div>
          <div className="group p-8 border-2 border-gray-200 dark:border-gray-700 rounded-2xl hover-lift hover:border-secondary/50 transition-all duration-300 animate-slide-in-right" style={{ animationDelay: '0.2s' }}>
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-blue-500 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
              </svg>
            </div>
            <h3 className="text-2xl font-semibold mb-4">Data Engineering</h3>
            <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
              Polars, DuckDB, ETL Pipelines, Data Quality, Performance Optimization
            </p>
          </div>
          <div className="group p-8 border-2 border-gray-200 dark:border-gray-700 rounded-2xl hover-lift hover:border-accent/50 transition-all duration-300 animate-slide-in-right" style={{ animationDelay: '0.3s' }}>
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-2xl font-semibold mb-4">MLOps</h3>
            <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
              Production Monitoring, Testing, Logging, Configuration Management
            </p>
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section>
        <h2 className="text-4xl font-bold mb-12 text-center animate-slide-up">
          <span className="inline-block relative">
            Featured Projects
            <div className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-green-500 rounded-full" />
          </span>
        </h2>
        <div className="grid md:grid-cols-2 gap-8">
          {projects.map((project, index) => (
            <div key={project.id} className="animate-scale-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <ProjectCard project={project} />
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
