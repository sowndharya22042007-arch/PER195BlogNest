# AI BlogNest API – AI Augmented Backend Development

A simple educational full-stack blog management project developed for the Naan Mudhalvan team project.

## Technologies
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- REST API

## Features
- Create, read, update and delete blogs
- Search blogs
- AI-assisted title and category suggestions using lightweight keyword analysis
- SQLite data storage
- REST API endpoints
- Responsive web dashboard

## Project Structure
```text
ai-blognest-api/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## How to Run

1. Install Python 3.
2. Open Command Prompt inside this project folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `python app.py`
5. Open:
   `http://127.0.0.1:5000`

The SQLite database `blog.db` is created automatically when the application starts.

## API Endpoints

- `GET /api/health` – check API status
- `GET /api/blogs` – list blogs
- `POST /api/blogs` – create a blog
- `PUT /api/blogs/<id>` – update a blog
- `DELETE /api/blogs/<id>` – delete a blog
- `POST /api/ai/suggest` – generate title/category suggestions

## Note on the AI Feature
The project uses a lightweight, explainable keyword-analysis module for AI-assisted suggestions. It does not require an external paid AI API or API key, making it easy to run for a student project.
