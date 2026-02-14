export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-3xl">
      <h1 className="text-4xl font-bold mb-8">About Me</h1>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Professional Summary</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          ML Engineer and Data Scientist specializing in production machine learning systems for gaming analytics and AI applications. 
          I build end-to-end solutions from data generation and feature engineering through model deployment and monitoring.
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          My work focuses on practical, production-ready implementations that demonstrate both technical depth and 
          business impact. I'm particularly interested in churn prediction, RAG systems, LLM integration, event processing pipelines, and MLOps best practices.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Technical Skills</h2>
        
        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Machine Learning</h3>
          <div className="flex flex-wrap gap-2">
            {['PyTorch', 'XGBoost', 'scikit-learn', 'LSTM', 'GRU', 'RAG', 'LLMs', 'Vector Embeddings',
              'Feature Engineering', 'Model Evaluation', 'A/B Testing'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Data Engineering</h3>
          <div className="flex flex-wrap gap-2">
            {['Polars', 'DuckDB', 'ETL Pipelines', 'Data Quality', 'Performance Optimization', 
              'YAML Configuration'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">MLOps & Production</h3>
          <div className="flex flex-wrap gap-2">
            {['Production Monitoring', 'Error Handling', 'Logging', 'pytest', 'Unit Testing', 
              'Configuration Management'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Tools & Frameworks</h3>
          <div className="flex flex-wrap gap-2">
            {['Python', 'Git', 'Streamlit', 'FastAPI', 'sentence-transformers', 'Google Gemini', 'Docker', 'AWS'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Career Interests</h2>
        <ul className="space-y-2 text-gray-700 dark:text-gray-300">
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Data Science roles in Germany</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Gaming analytics positions in Turkey</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>ML Engineering roles with production system focus</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>MLOps and data engineering positions</span>
          </li>
        </ul>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Connect</h2>
        <div className="flex gap-4">
          <a 
            href="https://github.com/ozlem-senel"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-gray-800 text-white rounded hover:bg-gray-700 transition"
          >
            GitHub
          </a>
          <a 
            href="https://linkedin.com/in/ozlem-senel"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            LinkedIn
          </a>
        </div>
      </section>
    </div>
  )
}
