import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import RecipeDetail from './pages/RecipeDetail'
import RecipeForm from './pages/RecipeForm'

function App() {
  return (
    <div className="container mx-auto p-4">
      <nav className="mb-4">
        <Link to="/" className="mr-2">Home</Link>
        <Link to="/new">Add Recipe</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recipes/:id" element={<RecipeDetail />} />
        <Route path="/new" element={<RecipeForm />} />
        <Route path="/edit/:id" element={<RecipeForm />} />
      </Routes>
    </div>
  )
}

export default App
