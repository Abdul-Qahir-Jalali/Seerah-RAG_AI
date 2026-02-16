import { useState } from 'react'
import { Book, ChevronDown, ChevronUp } from 'lucide-react'

function SourceCard({ source, index }) {
  const [isExpanded, setIsExpanded] = useState(false)
  const { content, metadata } = source

  const isHadith = metadata.source_type === 'hadith'
  const isQuran = metadata.source_type === 'quran'

  // Extract Arabic and English text
  const parts = content.split('\n\n')
  const englishPart = parts.find(p => p.startsWith('English:'))?.replace('English: ', '') || ''
  const arabicPart = parts.find(p => p.startsWith('Arabic:'))?.replace('Arabic: ', '') || ''

  return (
    <div className="source-card">
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center">
            <Book className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            {isHadith && (
              <>
                <p className="font-semibold text-emerald-400">
                  {metadata.collection}
                </p>
                <p className="text-xs text-gray-500">
                  {metadata.chapter}
                </p>
              </>
            )}
            {isQuran && (
              <>
                <p className="font-semibold text-emerald-400">
                  {metadata.reference}
                </p>
                <p className="text-xs text-gray-500">
                  Quran
                </p>
              </>
            )}
          </div>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-gray-400 hover:text-emerald-400 transition-colors"
        >
          {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
      </div>

      {isExpanded && (
        <div className="mt-3 pt-3 border-t border-white/10 space-y-3">
          {/* English Text */}
          {englishPart && (
            <div>
              <p className="text-xs text-gray-500 mb-1">English Translation:</p>
              <p className="text-gray-300 text-sm leading-relaxed">
                {englishPart}
              </p>
            </div>
          )}

          {/* Arabic Text */}
          {arabicPart && (
            <div>
              <p className="text-xs text-gray-500 mb-1">Arabic Text:</p>
              <p className="text-gray-300 text-sm leading-relaxed text-right" dir="rtl" lang="ar">
                {arabicPart}
              </p>
            </div>
          )}

          {/* Metadata */}
          {isHadith && metadata.narrator && (
            <div className="text-xs text-gray-500">
              <span className="font-semibold">Narrator:</span> {metadata.narrator}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SourceCard
