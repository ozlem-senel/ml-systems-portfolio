export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-3xl">
      <h1 className="text-4xl font-bold mb-8">About Me</h1>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Professional Summary</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Master's student at Technical University of Munich (TUM) specializing in AI and Machine Learning with academic and 
          project-based experience in developing and deploying cloud-based and production-oriented AI and data pipelines.
        </p>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          My academic background includes deep learning coursework (CNNs, RNNs, LSTMs, GANs), data mining and 
          fundamentals of artificial intelligence. I completed my bachelor's thesis on early diagnosis of prostate cancer using 
          dynamic modeling and data science tools with research presented at the 2023 System Dynamics Conference. 
          More recently, my master’s thesis explores synthetic data generation methods for financial time series, comparing bootstrapping and GAN-based approaches with a focus on robustness and forecasting performance.
        </p>
        <p className="text-gray-700 dark:text-gray-300">
          This portfolio showcases end-to-end ML implementations using gaming data from my hobby, demonstrating expertise in 
          PyTorch neural networks, RAG systems with LLMs and production-grade data pipelines. I'm actively exploring opportunities 
          in ML engineering, deep learning research and AI system development across various domains.
        </p>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Education</h2>
        <div className="mb-6">
          <div className="flex justify-between items-start mb-2">
            <div>
              <h3 className="text-lg font-semibold">Technical University of Munich (TUM)</h3>
              <p className="text-gray-600 dark:text-gray-400">Master in Management and Technology</p>
            </div>
            <span className="text-sm text-gray-500">2024 - 2026</span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Focus: AI and Machine Learning • Coursework in Deep Learning, Cognitive Systems, Business Analytics
          </p>
        </div>
        <div>
          <div className="flex justify-between items-start mb-2">
            <div>
              <h3 className="text-lg font-semibold">Bogazici University</h3>
              <p className="text-gray-600 dark:text-gray-400">Bachelor's degree in Industrial Engineering</p>
            </div>
            <span className="text-sm text-gray-500">Graduated</span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            • Research in Data Mining, Time Series Analysis, System Simulation
          </p>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Technical Skills</h2>
        
        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Machine Learning & Deep Learning</h3>
          <div className="flex flex-wrap gap-2">
            {['PyTorch', 'TensorFlow', 'XGBoost', 'scikit-learn', 'LSTM', 'GRU', 'GANs', 'LSTMs',
              'GANs', 'Time Series Forecasting', 'ARIMA', 'Prophet', 'Supervised Learning', 
              'Unsupervised Learning', 'Model Evaluation', 'Ensemble Methods'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">LLMs & AI Applications</h3>
          <div className="flex flex-wrap gap-2">
            {['RAG Systems', 'Vector Embeddings', 'sentence-transformers', 'Google Gemini', 
              'Semantic Search', 'LLM Integration', 'Hugging Face'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Data Engineering & Databases</h3>
          <div className="flex flex-wrap gap-2">
            {['Pandas', 'NumPy', 'Polars', 'DuckDB', 'PostgreSQL', 'Snowflake', 'Azure SQL', 'T-SQL',
              'dbt', 'ETL Pipelines', 'Data Quality', 'Feature Engineering'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Cloud & DevOps</h3>
          <div className="flex flex-wrap gap-2">
            {['AWS (Lambda, S3, EC2, IAM)', 'Terraform', 'Docker', 'Git', 'CI/CD',
              'Infrastructure as Code'].map((skill) => (
              <span key={skill} className="px-3 py-1 bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200 text-sm rounded">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-medium mb-3">Tools & Frameworks</h3>
          <div className="flex flex-wrap gap-2">
            {['Python', 'R', 'SQL', 'FastAPI', 'Streamlit', 'Power BI', 'Grafana', 
              'pytest', 'Git', 'Jupyter'].map((skill) => (
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
