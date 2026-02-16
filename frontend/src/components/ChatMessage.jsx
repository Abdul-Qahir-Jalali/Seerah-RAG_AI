import { User, Bot } from 'lucide-react'
import SourceCard from './SourceCard'

function ChatMessage({ message }) {
  const isUser = message.type === 'user'

  return (
    <div className={`chat-message ${isUser ? 'ml-8' : 'mr-8'}`}>
      <div className="flex gap-3">
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser 
            ? 'bg-gradient-to-br from-blue-500 to-purple-500' 
            : 'bg-gradient-to-br from-emerald-500 to-teal-500'
        }`}>
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </div>

        {/* Content */}
        <div className="flex-1 space-y-3">
          <div className="flex items-center gap-2">
            <span className="font-semibold">
              {isUser ? 'You' : 'AI Assistant'}
            </span>
            <span className="text-xs text-gray-500">
              {message.timestamp.toLocaleTimeString()}
            </span>
          </div>

          {/* Message Text */}
          <div className="prose prose-invert max-w-none">
            <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
          </div>

          {/* Sources */}
          {message.sources && message.sources.length > 0 && (
            <div className="space-y-2 mt-4">
              <p className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
                <span className="w-1 h-1 bg-emerald-400 rounded-full"></span>
                Sources ({message.sources.length})
              </p>
              <div className="grid grid-cols-1 gap-3">
                {message.sources.map((source, index) => (
                  <SourceCard key={index} source={source} index={index} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
