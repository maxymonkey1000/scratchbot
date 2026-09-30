import os
import scratchattach as sa

# Load credentials from Render Environment Variables
username = os.environ.get("SCRATCH_USER")
password = os.environ.get("SCRATCH_PASS")
project_id = os.environ.get("SCRATCH_PROJECT_ID")

# Connect to Scratch
session = sa.login(username, password)
conn = session.connect_cloud(project_id=project_id)
client = sa.CloudRequests(conn)


@client.request
def save_game(player_name, coins, level):
    print(f"Saved stats for {player_name}: Coins={coins}, Level={level}")
    # You can output or manage save logs here
    return "SUCCESS"


@client.request
def load_game(player_name):
    # Example load logic
    return "100-1"


print("Render Cloud Bot is online and listening for requests...")
client.run()
