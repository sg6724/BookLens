import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({ baseURL })

export async function identifyBook(file: File) {
  const form = new FormData()
  form.append('image', file)
  const { data } = await api.post('/books/identify', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function getBook(bookId: number) {
  const { data } = await api.get(`/books/${bookId}`)
  return data
}

export async function createSummary(input: { book_id: number; tone: string; length: string; audience: string }) {
  const { data } = await api.post('/summaries', input)
  return data
}

export async function getRecommendations(bookId: number, top_k = 5) {
  const { data } = await api.get(`/recommendations/books/${bookId}`, { params: { top_k } })
  return data
}

export async function listLibrary() {
  const { data } = await api.get('/library')
  return data
}

export async function addToLibrary(book_id: number, is_liked = true) {
  const { data } = await api.post('/library', { book_id, is_liked })
  return data
}

export async function toggleLike(book_id: number) {
  const { data } = await api.patch(`/library/${book_id}`)
  return data
}
