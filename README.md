# iRecipe

This repository contains a simple recipe manager split into two parts:

- **backend/** – Flask REST API with SQLite.
- **frontend/** – React application built with Vite and TailwindCSS.

To see the application in action you need to run **both** parts:

1. Start the API:
   ```bash
   cd backend
   python app.py
   ```

2. In a separate terminal run the React dev server:
   ```bash
   cd frontend
   npm run dev
   ```

Open `http://localhost:5173` in your browser. The API is available on
`http://localhost:5000` and shows a short message at `/`.
