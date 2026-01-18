from broker.login import get_authenticated_client
client = get_authenticated_client()


# ---- STEP 3: READ-ONLY CALLS ----
print("Fetching positions...")
positions = client.positions()
assert isinstance(positions, dict)
assert "200" in str(positions.get("stCode", ""))

print("Fetching limits...")
limits = client.limits()
assert "200" in str(limits.get("stCode", ""))

print("Limits response type:", type(limits))

# ---- STEP 4: LOGOUT ----
client.logout()
print("Logout successful")