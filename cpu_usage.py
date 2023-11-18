import psutil
from twilio.rest import Client
from getpass import getpass
import cv2
import numpy as np

# Twilio account SID, auth token, and phone numbers
twilio_account_sid = "Your Twilio Account SID"
twilio_auth_token = "Your Twilio auth code"
twilio_phone_number = "Twilio Phone Number"
recipient_phone_number = "Receiver Number"

# Set the CPU usage threshold for alerting (adjust as needed)
cpu_threshold = 90.0

# Set the exit password
exit_password = "exit987"

# Function to send SMS alert
def send_sms_alert(body):
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

# Function to check CPU usage and send alert if it exceeds the threshold
def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

# Main loop for continuous monitoring and displaying CPU usage
while True:
    cpu_usage = check_cpu_usage()

    # Display CPU usage in a frame
    frame = np.ones((100, 400, 3), np.uint8) * 255
    cv2.putText(frame, f'CPU Usage: {cpu_usage}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("CPU Usage Monitor", frame)

    # Check for key press to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        password = getpass("You will be at risk. Enter exit password to quit: ").strip()
        if password == exit_password:
            print("Exiting the program.")
            break
        else:
            print("Incorrect password. Please try again.")
    
    # Send SMS alert if CPU usage exceeds the threshold
    if cpu_usage > cpu_threshold:
        body = f"High CPU Usage Detected at your Server: {cpu_usage}%"
        send_sms_alert(body)

# Release the OpenCV window
cv2.destroyAllWindows()
