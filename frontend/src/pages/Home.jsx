import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import RatingStars from '../components/RatingStars'

function Home() {
  const [recipes, setRecipes] = useState([])
  const [search, setSearch] = useState('')

  useEffect(() => {
    api.get('/recipes').then(res => setRecipes(res.data))
  }, [])

  const filtered = recipes.filter(r => r.title.toLowerCase().includes(search.toLowerCase()))

  return (
    <div>
      <input
        className="border p-1 mb-2"
        placeholder="Search..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <ul>
        {filtered.map(r => (
          <li key={r.id} className="mb-2">
            <Link className="text-blue-600" to={`/recipes/${r.id}`}>{r.title}</Link>
            <RatingStars value={r.ratings.reduce((a, b) => a + b, 0) / (r.ratings.length || 1)} readOnly />
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Home
