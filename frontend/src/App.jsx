import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, BookOpen, Loader2, AlertCircle, Sparkles } from 'lucide-react'
import ChatMessage from './components/ChatMessage'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!input.trim() || isLoading) return

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post('/api/query', {
        question: input
      })

      const aiMessage = {
        type: 'ai',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get response. Please try again.')
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen islamic-pattern flex flex-col">
      {/* Header */}
      <header className="glass-card m-4 p-6 sticky top-4 z-10">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold gradient-text">Seerah RAG System</h1>
            <p className="text-gray-400 text-sm">Ask questions about Islamic texts</p>
          </div>
        </div>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto px-4 pb-32 scrollbar-thin">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 && (
            <div className="text-center mt-20">
              <div className="inline-block p-6 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-full mb-6">
                <Sparkles className="w-16 h-16 text-emerald-400" />
              </div>
              <h2 className="text-3xl font-bold mb-4 glow-text">Welcome to Seerah RAG</h2>
              <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
                Ask any question about Islamic texts including Hadith collections and the Quran. 
                Get accurate answers with authentic source citations.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                {[
                  "What are the pillars of Islam?",
                  "Tell me about the Night Journey",
                  "What does Surah Al-Fatiha say?",
                  "Describe the Battle of Badr"
                ].map((question, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(question)}
                    className="glass-card-hover p-4 text-left text-sm hover:scale-105 transition-transform"
                  >
                    <span className="text-emerald-400">→</span> {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}

          {isLoading && (
            <div className="chat-message flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin text-emerald-400" />
              <span className="text-gray-400">Searching through Islamic texts...</span>
            </div>
          )}

          {error && (
            <div className="glass-card p-4 border-red-500/30 bg-red-500/10 mb-4">
              <div className="flex items-center gap-2 text-red-400">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 p-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="glass-card p-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question about Islamic texts..."
                className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed px-6 py-3 rounded-xl font-semibold flex items-center gap-2 transition-all hover:scale-105 active:scale-95 shadow-lg"
              >
                <Send className="w-5 h-5" />
                Send
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
