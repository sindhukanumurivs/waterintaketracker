from flask import Flask, render_template, request, jsonify
from notifypy import Notify
import threading
import time
import os

app = Flask(__name__)

# Initial values
drinked_water = 0
target_intake = 3200  # Default target intake
send_notifications = False  # Flag to control notification sending

# Create a Notify object
notification = Notify()

@app.route('/')
def index():
    return render_template('index.html', drinked_water=drinked_water, target_intake=target_intake)

@app.route('/update_intake', methods=['POST'])
def update_intake():
    global drinked_water, target_intake, send_notifications
    intake = int(request.json['intake'])
    drinked_water += intake
    
    # Check if target intake is reached
    if drinked_water >= target_intake:
        send_notifications = False  # Stop notifications
    
    return jsonify({'status': 'success', 'water_intake': drinked_water, 'target_intake': target_intake})

@app.route('/update_target', methods=['POST'])
def update_target():
    global target_intake
    target_intake = int(request.json['target_intake'])
    return jsonify({'status': 'success', 'target_intake': target_intake})

def send_reminder_notifications(name, interval):
    global send_notifications
    while send_notifications:
        # Send notification
        notification.title = 'Water Reminder'
        notification.message = f"Hey, don't forget to drink water!"
        icon_path = os.path.join( "water-drop.png")
        
        if os.path.exists(icon_path):
            notification.icon = icon_path
        else:
            print(f"Icon file {icon_path} does not exist")
            notification.icon = None  # Or set a default icon
        
    
        print(f"Notification sent with icon: {icon_path}")

        # Wait for the given interval (converted from minutes to seconds)
        time.sleep(interval * 10)
        notification.send()

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    global send_notifications
    send_notifications = True
    name = 'praisy'
    interval = 1  # Interval in minutes

    # Start the reminder notifications in a separate thread
    reminder_thread = threading.Thread(target=send_reminder_notifications, args=(name, interval))
    reminder_thread.start()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True,port=5001)
