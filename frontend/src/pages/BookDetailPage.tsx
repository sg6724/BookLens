import React, { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { addToLibrary, createSummary, getBook, getRecommendations } from '../api/client'

const BookDetailPage: React.FC = () => {
  const { bookId } = useParams()
  const id = useMemo(() => Number(bookId), [bookId])
  const [book, setBook] = useState<any>(null)
  const [summary, setSummary] = useState<any>(null)
  const [tone, setTone] = useState('casual')
  const [length, setLength] = useState('medium')
  const [audience, setAudience] = useState('adults')
  const [loading, setLoading] = useState(false)
  const [recs, setRecs] = useState<any[]>([])

  useEffect(() => {
    if (!id) return
    getBook(id).then(setBook)
  }, [id])

  useEffect(() => {
    if (!id) return
    getRecommendations(id).then(setRecs).catch(() => setRecs([]))
  }, [id])

  const onGenerate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await createSummary({ book_id: id, tone, length, audience })
      setSummary(res)
    } finally {
      setLoading(false)
    }
  }

  if (!book) return <p>Loading…</p>

  const audioUrl = summary?.audio_path ? summary.audio_path.replace('./data/audio', '/audio') : null

  return (
    <div>
      <h1>{book.title}</h1>
      <p>by {book.author}</p>
      {book.cover_url && <img src={book.cover_url} alt={book.title} style={{ maxWidth: 200 }} />}
      <p style={{ whiteSpace: 'pre-wrap' }}>{book.description}</p>

      <form onSubmit={onGenerate} style={{ marginTop: 16 }}>
        <label> Tone: </label>
        <select value={tone} onChange={(e) => setTone(e.target.value)}>
          <option value="casual">casual</option>
          <option value="academic">academic</option>
          <option value="thriller">thriller</option>
          <option value="poetic">poetic</option>
        </select>
        <label style={{ marginLeft: 8 }}> Length: </label>
        <select value={length} onChange={(e) => setLength(e.target.value)}>
          <option value="short">short</option>
          <option value="medium">medium</option>
          <option value="detailed">detailed</option>
        </select>
        <label style={{ marginLeft: 8 }}> Audience: </label>
        <select value={audience} onChange={(e) => setAudience(e.target.value)}>
          <option value="kids">kids</option>
          <option value="teens">teens</option>
          <option value="adults">adults</option>
        </select>
        <button type="submit" disabled={loading} style={{ marginLeft: 8 }}>
          {loading ? 'Generating…' : 'Generate Summary'}
        </button>
      </form>

      {summary && (
        <div style={{ marginTop: 16 }}>
          <h2>Summary</h2>
          <p style={{ whiteSpace: 'pre-wrap' }}>{summary.content}</p>
          {audioUrl && (
            <div style={{ marginTop: 8 }}>
              <audio controls src={audioUrl}></audio>
              <div>
                <a href={audioUrl} download>
                  Download MP3
                </a>
              </div>
            </div>
          )}
          <button onClick={() => addToLibrary(id, true)} style={{ marginTop: 8 }}>
            Save to My Library
          </button>
        </div>
      )}

      {recs?.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3>Recommendations</h3>
          <ul style={{ display: 'flex', gap: 12, listStyle: 'none', padding: 0 }}>
            {recs.map((b) => (
              <li key={b.id} style={{ width: 150 }}>
                {b.cover_url && <img src={b.cover_url} alt={b.title} style={{ width: '100%' }} />}
                <div style={{ fontWeight: 600 }}>{b.title}</div>
                <div style={{ fontSize: 12 }}>{b.author}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default BookDetailPage
