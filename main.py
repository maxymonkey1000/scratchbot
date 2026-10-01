import os
import threading
from flask import Flask
import scratchattach as sa

app = Flask(__name__)

@app.route("/")
def home():
    return "Scratch Bot is online!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def run_scratch_bot():
    username = os.environ.get("SCRATCH_USER")
    password = os.environ.get("SCRATCH_PASS")
    project_id = os.environ.get("SCRATCH_PROJECT_ID")

    # Connect to Scratch Cloud
    session = sa.login(username, password)
    
    # Use TwocanEvents or WsCloudEvents for cloud monitoring
    events = sa.TwocanEvents(project_id)

    @events.event
    def on_ready():
        print("Scratch Bot connected and listening!")

    @events.event
    def on_set(event):
        # Triggered whenever a cloud variable changes
        print(f"Variable updated: {event.var} = {event.value}")

    events.start()

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    run_scratch_bot()
