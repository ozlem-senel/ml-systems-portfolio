import Link from 'next/link'

type ProjectStatus = 'complete' | 'in-progress' | 'planned'

interface Project {
  id: string
  title: string
  status: ProjectStatus
  description: string
  tags: string[]
  metrics: { label: string; value: string }[]
  link: string
}

const statusColors = {
  complete: 'bg-secondary text-white',
  'in-progress': 'bg-yellow-500 text-white',
  planned: 'bg-gray-400 text-white',
}

const statusLabels = {
  complete: 'Complete',
  'in-progress': 'In Progress',
  planned: 'Planned',
}

export default function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="border rounded-lg p-6 hover:shadow-lg transition">
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-xl font-semibold">{project.title}</h3>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[project.status]}`}>
          {statusLabels[project.status]}
        </span>
      </div>
      
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        {project.description}
      </p>
      
      {project.metrics.length > 0 && (
        <div className="grid grid-cols-3 gap-3 mb-4 p-3 bg-gray-50 dark:bg-gray-800 rounded">
          {project.metrics.map((metric, index) => (
            <div key={index}>
              <div className="text-xs text-gray-500 dark:text-gray-400">{metric.label}</div>
              <div className="text-lg font-semibold">{metric.value}</div>
            </div>
          ))}
        </div>
      )}
      
      <div className="flex flex-wrap gap-2 mb-4">
        {project.tags.map((tag) => (
          <span 
            key={tag} 
            className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded"
          >
            {tag}
          </span>
        ))}
      </div>
      
      <Link 
        href={project.link}
        className="text-primary hover:underline font-medium"
      >
        View Project →
      </Link>
    </div>
  )
}
