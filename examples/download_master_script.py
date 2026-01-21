from broker.login import get_authenticated_client

client = get_authenticated_client()

x = client.scrip_master("nse_fo")

import requests
from pathlib import Path
from urllib.parse import urlparse

url = x

response = requests.get(url, timeout=30)
response.raise_for_status()

# Extract filename exactly like browser
filename = Path(urlparse(url).path).name
file_path = Path(filename)

# Delete old file if exists
if file_path.exists():
    file_path.unlink()
    print(f"🗑 Deleted old file: {file_path.name}")

with open(filename, "wb") as f:
    f.write(response.content)

print("✅ Downloaded:", filename)

exit_message = client.logout()
print(exit_message)
