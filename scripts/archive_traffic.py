import os
import json
import requests
from datetime import datetime

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPOSITORY = os.getenv("REPOSITORY")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def fetch_traffic_data(endpoint):
    url = f"https://api.github.com/repos/{REPOSITORY}/traffic/{endpoint}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch {endpoint}: Status {response.status_code}, Response: {response.text}")

try:
    clones = fetch_traffic_data("clones")
    views = fetch_traffic_data("views")

    date_str = datetime.utcnow().strftime("%Y-%m-%d")

    with open(f"data/clones_{date_str}.json", "w") as f:
        json.dump(clones, f, indent=2)

    with open(f"data/views_{date_str}.json", "w") as f:
        json.dump(views, f, indent=2)

    print("Successfully archived traffic data.")
except Exception as e:
    print(f"Error archiving traffic: {e}")
    raise e
