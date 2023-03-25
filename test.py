import requests
import json

base_url = "http://localhost:5002"  # Replace with your server's URL if needed
username = "test_user"  # Replace with the desired username
auth_key = "TEST"  # Replace with the correct service auth key if needed

# Add some todos for testing
todos = ["Buy groceries", "Finish the report", "Call mom"]

headers = {"Authorization": f"Bearer {auth_key}"}

for todo in todos:
    response = requests.post(
        f"{base_url}/todos/{username}",
        json={"todo": todo},
        headers=headers,
    )
    print(f"Added todo: {todo}, status: {response.status_code}")

# Get all todos
response = requests.get(f"{base_url}/todos/{username}", headers=headers)

if response.status_code == 200:
    todos = json.loads(response.text)
    print("All todos:")
    for idx, todo in enumerate(todos):
        print(f"{idx}: {todo['title']}, completed: {todo['completed']}")
else:
    print(f"Error: {response.status_code}")
