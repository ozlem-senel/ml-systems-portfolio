import Link from 'next/link'

export default function Header() {
  return (
    <header className="border-b">
      <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold">
          Özlem Senel
        </Link>
        <div className="flex gap-6">
          <Link href="/projects" className="hover:text-primary transition">
            Projects
          </Link>
          <Link href="/about" className="hover:text-primary transition">
            About
          </Link>
          <Link 
            href="https://github.com/ozlem-senel/ml-systems-portfolio" 
            target="_blank"
            className="hover:text-primary transition"
          >
            GitHub
          </Link>
        </div>
      </nav>
    </header>
  )
}
