import ArtGalleryPage from './pages/ArtGalleryPage'
import { useState } from 'React'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <ArtGalleryPage />
    </>
  )
}

export default App
