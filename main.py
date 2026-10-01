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

    # Connect to Scratch
    session = sa.login(username, password)
    conn = session.connect_cloud(project_id)
    
    # This works flawlessly in version 1.7.6
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

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    run_scratch_bot()
