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
  complete: 'bg-gradient-to-r from-green-500 to-emerald-500 text-white',
  'in-progress': 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white',
  planned: 'bg-gradient-to-r from-gray-400 to-gray-500 text-white',
}

const statusLabels = {
  complete: 'Complete',
  'in-progress': 'In Progress',
  planned: 'Planned',
}

export default function ProjectCard({ project }: { project: Project }) {
  return (
    <Link href={project.link}>
      <div className="group relative h-full border-2 border-gray-200 dark:border-gray-700 rounded-2xl p-8 hover-lift hover:border-primary/50 transition-all duration-300 cursor-pointer overflow-hidden">
        {/* Gradient background effect on hover */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-purple-50 to-green-50 dark:from-gray-800 dark:via-gray-800 dark:to-gray-800 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10" />
        
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-2xl font-bold group-hover:text-primary transition-colors duration-300">{project.title}</h3>
          <span className={`px-4 py-1.5 rounded-full text-xs font-semibold shadow-sm ${statusColors[project.status]}`}>
            {statusLabels[project.status]}
          </span>
        </div>
        
        <p className="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
          {project.description}
        </p>
        
        {project.metrics.length > 0 && (
          <div className="grid grid-cols-3 gap-4 mb-6 p-4 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
            {project.metrics.map((metric, index) => (
              <div key={index} className="text-center">
                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">{metric.label}</div>
                <div className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">{metric.value}</div>
              </div>
            ))}
          </div>
        )}
        
        <div className="flex flex-wrap gap-2 mb-6">
          {project.tags.map((tag) => (
            <span 
              key={tag} 
              className="px-3 py-1.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-medium rounded-lg border border-blue-200 dark:border-blue-800"
            >
              {tag}
            </span>
          ))}
        </div>
        
        <div className="flex items-center text-primary font-semibold group-hover:gap-2 transition-all">
          <span>View Project</span>
          <svg className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
    </Link>
  )
}
