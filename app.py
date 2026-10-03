from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "blog.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def suggest_category(text):
    text = text.lower()
    rules = {
        "Technology": ["python", "ai", "artificial intelligence", "software", "computer", "api", "coding", "technology"],
        "Education": ["student", "college", "school", "exam", "learning", "education", "course"],
        "Environment": ["environment", "waste", "recycle", "recycling", "climate", "pollution", "green"],
        "Health": ["health", "fitness", "exercise", "food", "medicine", "wellness"],
        "Travel": ["travel", "trip", "tour", "place", "hotel", "vacation"],
        "Entertainment": ["movie", "music", "game", "entertainment", "actor", "song"]
    }
    for category, keywords in rules.items():
        if any(word in text for word in keywords):
            return category
    return "General"

def suggest_title(content):
    words = [w.strip(".,!?;:()[]{}").capitalize() for w in content.split() if w.strip()]
    if not words:
        return "My New Blog"
    return " ".join(words[:6])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/blogs", methods=["GET"])
def get_blogs():
    conn = get_db()
    rows = conn.execute("SELECT * FROM blogs ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/blogs", methods=["POST"])
def create_blog():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    category = data.get("category", "").strip()

    if not content:
        return jsonify({"error": "Content is required"}), 400

    if not title:
        title = suggest_title(content)
    if not category:
        category = suggest_category(title + " " + content)

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO blogs (title, content, category) VALUES (?, ?, ?)",
        (title, content, category)
    )
    conn.commit()
    blog_id = cur.lastrowid
    row = conn.execute("SELECT * FROM blogs WHERE id = ?", (blog_id,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201

@app.route("/api/blogs/<int:blog_id>", methods=["PUT"])
def update_blog(blog_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    category = data.get("category", "").strip()

    if not content:
        return jsonify({"error": "Content is required"}), 400
    if not title:
        title = suggest_title(content)
    if not category:
        category = suggest_category(title + " " + content)

    conn = get_db()
    cur = conn.execute(
        "UPDATE blogs SET title=?, content=?, category=? WHERE id=?",
        (title, content, category, blog_id)
    )
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": "Blog not found"}), 404
    row = conn.execute("SELECT * FROM blogs WHERE id=?", (blog_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))

@app.route("/api/blogs/<int:blog_id>", methods=["DELETE"])
def delete_blog(blog_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM blogs WHERE id=?", (blog_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "Blog not found"}), 404
    return jsonify({"message": "Blog deleted successfully"})

@app.route("/api/ai/suggest", methods=["POST"])
def ai_suggest():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()
    title = data.get("title", "").strip()
    combined = title + " " + content

    return jsonify({
        "suggested_title": title or suggest_title(content),
        "suggested_category": suggest_category(combined),
        "message": "Suggestion generated using the project's lightweight AI-assisted keyword analysis."
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "running", "service": "AI BlogNest API"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
