'use client'

import { FormEvent, useState } from 'react'

const examples = [
  { label: 'Forgot password', subject: 'I cannot sign in', message: 'I forgot my password and cannot access my account.' },
  { label: 'Payment declined', subject: 'My card was declined', message: 'My credit card was declined even though the details are correct.' },
  { label: 'App crashes', subject: 'The app closes immediately', message: 'The mobile app crashes every time I try to open it.' },
  { label: 'Charged twice', subject: 'Duplicate card charge', message: 'I can see the same payment twice on my bank statement.' },
  { label: 'Slow app', subject: 'The app has become very slow', message: 'Pages take a long time to load and the app often freezes.' },
  { label: 'Feature idea', subject: 'I have a feature suggestion', message: 'Could you add a dark mode to the mobile app?' },
]

type Result = {
  predicted_category: string
  urgency: string
  response: string
  retrieved_documents: { title: string; score: number }[]
}

const apiUrl = process.env.NEXT_PUBLIC_RAG_API_URL || 'https://ml-systems-portfolio.onrender.com'

export default function TicketDemo() {
  const [subject, setSubject] = useState(examples[0].subject)
  const [message, setMessage] = useState(examples[0].message)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function useExample(index: number) {
    setSubject(examples[index].subject)
    setMessage(examples[index].message)
    setResult(null)
    setError('')
  }

  async function submitTicket(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch(`${apiUrl}/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticket_id: `WEB-${Date.now()}`,
          subject,
          description: message,
        }),
      })

      if (!response.ok) throw new Error('The API could not process this ticket.')
      setResult(await response.json())
    } catch {
      setError('The support service could not be reached. It may be waking up; please wait a minute and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="p-5 bg-gray-50 dark:bg-gray-800 border-b dark:border-gray-700">
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">Start with an example or write your own:</p>
        <div className="flex flex-wrap gap-2">
          {examples.map((item, index) => (
            <button
              key={item.label}
              type="button"
              onClick={() => useExample(index)}
              className="px-3 py-2 rounded text-sm font-medium border bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-600 hover:border-primary"
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={submitTicket} className="p-5 space-y-4">
        <div>
          <label htmlFor="ticket-subject" className="block text-sm font-medium mb-2">Subject</label>
          <input
            id="ticket-subject"
            value={subject}
            onChange={(event) => setSubject(event.target.value)}
            required
            className="w-full rounded border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900"
          />
        </div>
        <div>
          <label htmlFor="ticket-message" className="block text-sm font-medium mb-2">Customer message</label>
          <textarea
            id="ticket-message"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            required
            rows={4}
            className="w-full resize-y rounded border border-gray-300 bg-white px-3 py-2 dark:border-gray-600 dark:bg-gray-900"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-600 disabled:cursor-wait disabled:opacity-60"
        >
          {loading ? 'Generating…' : 'Generate response'}
        </button>
      </form>

      {error && (
        <div role="alert" className="mx-5 mb-5 p-4 border-l-4 border-red-500 bg-red-50 text-sm text-red-800 dark:bg-red-900/20 dark:text-red-200">
          {error}
        </div>
      )}

      {result && (
        <div className="p-5 border-t bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
          <h3 className="font-semibold mb-4">Suggested result</h3>
          <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm mb-4">
            <p><span className="text-gray-500">Topic:</span> <span className="font-semibold capitalize">{result.predicted_category}</span></p>
            <p><span className="text-gray-500">Urgency:</span> <span className="font-semibold capitalize">{result.urgency}</span></p>
            {result.retrieved_documents[0] && (
              <p><span className="text-gray-500">Article:</span> <span className="font-semibold">{result.retrieved_documents[0].title}</span></p>
            )}
          </div>
          <p className="text-sm leading-relaxed whitespace-pre-line text-gray-700 dark:text-gray-300">{result.response}</p>
        </div>
      )}
    </div>
  )
}
