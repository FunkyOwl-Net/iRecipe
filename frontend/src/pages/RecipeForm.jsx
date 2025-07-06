import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../services/api'

function RecipeForm() {
  const navigate = useNavigate()
  const { id } = useParams()
  const isEdit = Boolean(id)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [ingredients, setIngredients] = useState('')
  const [image, setImage] = useState(null)

  useEffect(() => {
    if (isEdit) {
      api.get(`/recipes/${id}`).then(res => {
        const r = res.data
        setTitle(r.title)
        setDescription(r.description)
        setIngredients(r.ingredients.join(', '))
      })
    }
  }, [id, isEdit])

  const submit = async e => {
    e.preventDefault()
    const data = { title, description, ingredients: ingredients.split(',').map(i => i.trim()) }
    let resp
    if (isEdit) {
      resp = await api.put(`/recipes/${id}`, data)
    } else {
      resp = await api.post('/recipes', data)
    }
    const recipeId = isEdit ? id : resp.data.id
    if (image) {
      const form = new FormData()
      form.append('image', image)
      await api.post(`/recipes/${recipeId}/images`, form, { headers: { 'Content-Type': 'multipart/form-data' } })
    }
    navigate(`/recipes/${recipeId}`)
  }

  return (
    <form onSubmit={submit} className="max-w-md">
      <div className="mb-2">
        <label className="block">Title</label>
        <input className="border w-full" value={title} onChange={e => setTitle(e.target.value)} />
      </div>
      <div className="mb-2">
        <label className="block">Description</label>
        <textarea className="border w-full" value={description} onChange={e => setDescription(e.target.value)} />
      </div>
      <div className="mb-2">
        <label className="block">Ingredients (comma separated)</label>
        <input className="border w-full" value={ingredients} onChange={e => setIngredients(e.target.value)} />
      </div>
      <div className="mb-2">
        <label className="block">Image</label>
        <input type="file" onChange={e => setImage(e.target.files[0])} />
      </div>
      <button className="px-2 py-1 bg-green-500 text-white">Save</button>
    </form>
  )
}

export default RecipeForm
