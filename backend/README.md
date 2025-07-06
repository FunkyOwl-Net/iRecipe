# Backend

This Flask backend provides a REST API for managing recipes. It stores data in a local SQLite database.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

Uploaded images are stored in the `uploads/` folder.

Access `http://localhost:5000/` in your browser to verify the API is running; it
returns a short JSON message.

## Tests
Run `pytest` to execute the unit tests.
