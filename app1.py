from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.github_events
collection = db.events

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "push":
        author = data["pusher"]["name"]
        branch = data["ref"].split("/")[-1]

        event = {
            "type": "push",
            "author": author,
            "to_branch": branch,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event)

    elif event_type == "pull_request":
        pr = data["pull_request"]
        event = {
            "type": "pull_request",
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
