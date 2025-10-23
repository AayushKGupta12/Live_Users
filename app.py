from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5175",
    "http://localhost:5174",
    "http://localhost:5173",
    "https://resume-analysis-dash-3g0x.bolt.host",
    "https://edstack.netlify.app"
]}})

# Set timezone to IST
IST = ZoneInfo("Asia/Kolkata")

# Initialize global variables
A = random.randint(200, 400)
B = A + random.choice([-3, -2, -1, 1, 2, 3])

# Refresh A and B every 4 hours
def refresh_A():
    global A, B
    A = random.randint(200, 400)
    B = A + random.choice([-3, -2, -1, 1, 2, 3])
    # print(f"[A REFRESHED] A={A}, B={B}")

# Refresh B every 3 seconds
def refresh_B():
    global B
    B = A + random.choice([-3, -2, -1, 1, 2, 3])
    # print(f"[B REFRESHED] A={A}, B={B}")

# Schedule jobs
scheduler = BackgroundScheduler(timezone=IST)
scheduler.add_job(refresh_B, 'interval', seconds=3, id='refresh_B_job')

now = datetime.now(IST)
next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
scheduler.add_job(refresh_A, 'interval', hours=4, start_date=next_midnight, id='refresh_A_job')

scheduler.start()

# API route
@app.route('/', methods=['GET'])
def live_user():
    return jsonify({'A': A, 'B': B})

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
