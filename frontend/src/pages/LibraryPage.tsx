import React, { useEffect, useState } from 'react'
import { listLibrary, toggleLike } from '../api/client'

const LibraryPage: React.FC = () => {
  const [items, setItems] = useState<any[]>([])

  const load = () => listLibrary().then(setItems)

  useEffect(() => {
    load()
  }, [])

  return (
    <div>
      <h1>My Library</h1>
      <ul>
        {items.map((it) => (
          <li key={it.id} style={{ marginBottom: 8 }}>
            Book #{it.book_id} — liked: {String(it.is_liked)}{' '}
            <button onClick={() => toggleLike(it.book_id).then(load)} style={{ marginLeft: 8 }}>
              Toggle Like
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default LibraryPage
