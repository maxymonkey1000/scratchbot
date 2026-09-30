import os
import threading
from flask import Flask
import scratchattach as sa

# 1. Start a simple Flask web server so Render sees an active Web Service
app = Flask(__name__)


@app.route("/")
def home():
    return "Scratch Bot is online!"


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# 2. Function to run the Scratch bot
def run_scratch_bot():
    username = os.environ.get("SCRATCH_USER")
    password = os.environ.get("SCRATCH_PASS")
    project_id = os.environ.get("SCRATCH_PROJECT_ID")

    session = sa.login(username, password)
    conn = session.connect_cloud(project_id=project_id)
    client = sa.CloudRequests(conn)

    @client.request
    def save_game(player_name, coins, level):
        print(f"Saved stats for {player_name}: Coins={coins}, Level={level}")
        return "SUCCESS"

    @client.request
    def load_game(player_name):
        return "100-1"

    print("Scratch Bot connected and listening!")
    client.run()


# 3. Launch both simultaneously
if __name__ == "__main__":
    # Run Flask in a separate thread
    threading.Thread(target=run_web_server, daemon=True).start()
    # Run Scratch Bot on the main thread
    run_scratch_bot()
