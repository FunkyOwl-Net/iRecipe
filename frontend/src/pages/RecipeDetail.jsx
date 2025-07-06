import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../services/api'
import RatingStars from '../components/RatingStars'

function RecipeDetail() {
  const { id } = useParams()
  const [recipe, setRecipe] = useState(null)
  const [score, setScore] = useState(0)

  useEffect(() => {
    api.get(`/recipes/${id}`).then(res => setRecipe(res.data))
  }, [id])

  const rate = () => {
    api.post(`/recipes/${id}/rating`, { score }).then(() => {
      return api.get(`/recipes/${id}`)
    }).then(res => setRecipe(res.data))
  }

  if (!recipe) return <div>Loading...</div>

  return (
    <div>
      <h1 className="text-2xl mb-2">{recipe.title}</h1>
      <p className="mb-2">{recipe.description}</p>
      <div className="mb-2">
        {recipe.images.map(img => (
          <img key={img} src={`http://localhost:5000/uploads/${img}`} alt="" className="w-32 mr-2 inline-block" />
        ))}
      </div>
      <RatingStars value={recipe.ratings.reduce((a,b) => a+b,0)/(recipe.ratings.length||1)} readOnly />
      <div className="mt-2">
        <input type="number" className="border" value={score} onChange={e => setScore(e.target.value)} />
        <button className="ml-2 px-2 py-1 bg-blue-500 text-white" onClick={rate}>Rate</button>
      </div>
      <p className="mt-4"><Link className="text-blue-600" to={`/edit/${id}`}>Edit</Link></p>
    </div>
  )
}

export default RecipeDetail
