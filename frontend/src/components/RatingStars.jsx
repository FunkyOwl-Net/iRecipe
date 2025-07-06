import { useState } from 'react'

function Star({ filled, onClick, onMouseEnter }) {
  return (
    <span
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      className={filled ? 'text-yellow-400' : 'text-gray-300'}
    >
      ★
    </span>
  )
}

function RatingStars({ value = 0, readOnly = false, onChange }) {
  const [hover, setHover] = useState(0)
  const display = hover || value
  return (
    <span onMouseLeave={() => setHover(0)}>
      {[1, 2, 3, 4, 5].map(n => (
        <Star
          key={n}
          filled={n <= display}
          onClick={!readOnly ? () => onChange(n) : undefined}
          onMouseEnter={!readOnly ? () => setHover(n) : undefined}
        />
      ))}
    </span>
  )
}

export default RatingStars
