import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { identifyBook } from '../api/client'

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const res = await identifyBook(file)
      const bookId = res.book?.id
      if (bookId) {
        navigate(`/books/${bookId}`)
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to identify book')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Upload Book Cover</h1>
      <form onSubmit={onSubmit}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button type="submit" disabled={!file || loading} style={{ marginLeft: 8 }}>
          {loading ? 'Identifying…' : 'Identify Book'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}

export default UploadPage
