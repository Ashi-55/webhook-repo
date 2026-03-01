from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = "events.db"


# Create database table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            repo_name TEXT,
            branch TEXT,
            author TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    repo_name = data.get("repository", {}).get("full_name")
    branch = data.get("ref")
    author = data.get("sender", {}).get("login")

    # Check for merged pull request
    if event_type == "pull_request":
        action = data.get("action")
        merged = data.get("pull_request", {}).get("merged")

        if action == "closed" and merged:
            event_type = "merge"

    timestamp = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (event_type, repo_name, branch, author, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (event_type, repo_name, branch, author, timestamp))

    conn.commit()
    conn.close()

    return jsonify({"status": "event stored"}), 200


# Get events with time filtering
@app.route("/events")
def get_events():
    minutes = request.args.get("minutes", 2000)
    minutes = int(minutes)

    current_time = datetime.utcnow()
    time_limit = current_time - timedelta(minutes=minutes)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_type, repo_name, branch, author, timestamp
        FROM events
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (time_limit.isoformat(),))

    rows = cursor.fetchall()
    conn.close()

    events = []

    for row in rows:
        events.append({
            "event_type": row[0],
            "repo": row[1],
            "branch": row[2],
            "author": row[3],
            "timestamp": row[4]
        })

    return jsonify(events)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
