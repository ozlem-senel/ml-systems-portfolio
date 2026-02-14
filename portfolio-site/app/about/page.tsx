export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-3xl">
      <h1 className="text-4xl font-bold mb-8">About Me</h1>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Professional Summary</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          ML Engineer and Data Scientist specializing in machine learning, deep learning, and LLM applications. 
          I build production-ready systems from data engineering and model development through deployment and monitoring.
        </p>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          My portfolio showcases practical implementations using gaming data, which comes from my passion for gaming as a hobby. 
          These projects demonstrate technical depth in PyTorch neural networks, RAG systems, and scalable data pipelines.
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          I'm actively expanding my expertise in LLMs and exploring opportunities in ML engineering, deep learning research, 
          and production AI systems across various domains.
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
            <span>Machine Learning Engineering with focus on deep learning and neural networks</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>LLM applications and RAG systems development</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Production ML systems and MLOps roles</span>
          </li>
          <li className="flex items-start">
            <span className="text-primary mr-2">•</span>
            <span>Applied research in deep learning across various domains</span>
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
