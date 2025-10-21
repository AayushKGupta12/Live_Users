import random
import datetime
from zoneinfo import ZoneInfo  # Use built-in Python module for timezone
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
IST = ZoneInfo("Asia/Kolkata")
A = random.randint(200, 350)
B = A + random.choice([-3, -2, -1, 1, 2, 3])
def refresh_A():
    global A, B
    A = random.randint(200,350)
    B = A + random.choice([-3, -2, -1, 1, 2, 3])
    # print(f"[A REFRESHED] A={A}, B={B}")
def refresh_B():
    global B
    B = A + random.choice([-3, -2, -1, 1, 2, 3])
    # print(f"[B REFRESHED] A={A}, B={B}")
scheduler = BackgroundScheduler(timezone=IST)
scheduler.add_job(refresh_B, 'interval', seconds=3, id='refresh_B_job')
now = datetime.datetime.now(IST)
next_midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
scheduler.add_job(refresh_A, 'interval', hours=4, start_date=next_midnight, id='refresh_A_job')
scheduler.start()
@app.route('/', methods=['GET'])
def live_user():
    return jsonify({'A': A, 'B': B})

if __name__ == '__main__':
    app.run(debug=False)
