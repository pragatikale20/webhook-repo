import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
events = db["events"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    events.insert_one(data)
    return jsonify({"status": "success"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    latest_events = list(events.find().sort([('_id', -1)]).limit(10))
    for event in latest_events:
        event["_id"] = str(event["_id"])
    return jsonify(latest_events)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
