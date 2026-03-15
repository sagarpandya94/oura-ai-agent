from api.oura_client import OuraClient

client = OuraClient()

print("--- Sleep Data ---")
print(client.get_sleep())

print("--- Readiness Data ---")
print(client.get_daily_readiness())

print("--- Activity Data ---")
print(client.get_daily_activity())