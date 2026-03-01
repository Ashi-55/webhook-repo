from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://techuser:Tech1234@cluster0.6ktxk2w.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["webhookDB"]
collection = db["events"]


# ------------------------------------
# Webhook endpoint
# ------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    # Common fields
    request_id = None
    author = None
    action = None
    from_branch = None
    to_branch = None

    # PUSH event
    if event_type == "push":
        request_id = data.get("after")
        author = data.get("pusher", {}).get("name")
        action = "PUSH"
        to_branch = data.get("ref").split("/")[-1]

    # PULL REQUEST event
    elif event_type == "pull_request":

        pr = data.get("pull_request")

        request_id = pr.get("id")
        author = pr.get("user", {}).get("login")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")

        # check if merged
        if data.get("action") == "closed" and pr.get("merged"):
            action = "MERGE"
        else:
            action = "PULL_REQUEST"

    else:
        return jsonify({"message": "Event ignored"}), 200

    timestamp = datetime.utcnow()

    event_data = {
        "request_id": request_id,
        "author": author,
        "action": action,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

    collection.insert_one(event_data)

    return jsonify({"message": "Event stored"}), 200


# ------------------------------------
# Get events (last X minutes)
# ------------------------------------
@app.route("/events")
def get_events():

    minutes = int(request.args.get("minutes", 10))
    time_limit = datetime.utcnow() - timedelta(minutes=minutes)

    events = collection.find(
        {"timestamp": {"$gte": time_limit}}
    ).sort("timestamp", -1)

    result = []

    for event in events:

        formatted_time = event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")

        if event["action"] == "PUSH":
            message = f'{event["author"]} pushed to {event["to_branch"]} on {formatted_time}'

        elif event["action"] == "PULL_REQUEST":
            message = f'{event["author"]} submitted a pull request from {event["from_branch"]} to {event["to_branch"]} on {formatted_time}'

        elif event["action"] == "MERGE":
            message = f'{event["author"]} merged branch {event["from_branch"]} to {event["to_branch"]} on {formatted_time}'

        result.append(message)

    return jsonify(result)


# ------------------------------------
# Home page
# ------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
