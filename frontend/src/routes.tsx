import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import UploadPage from './pages/UploadPage'
import BookDetailPage from './pages/BookDetailPage'
import LibraryPage from './pages/LibraryPage'

export const AppRoutes: React.FC = () => {
  return (
    <div className="min-h-screen font-sans">
      <header style={{ padding: '12px', borderBottom: '1px solid #eee', marginBottom: 16 }}>
        <nav style={{ display: 'flex', gap: 12 }}>
          <Link to="/">Upload</Link>
          <Link to="/library">Library</Link>
        </nav>
      </header>
      <main style={{ maxWidth: 960, margin: '0 auto', padding: 16 }}>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/books/:bookId" element={<BookDetailPage />} />
          <Route path="/library" element={<LibraryPage />} />
        </Routes>
      </main>
    </div>
  )
}
