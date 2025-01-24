import requests
import json

def test_chat():
    url = "http://localhost:8000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer Ollama"
    }
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a test assistant."
            },
            {
                "role": "user",
                "content": "Testing. Just say hi and nothing else."
            }
        ],
        "model": "deepseek-r1:14b"
    }
    
    try:
        print("Sending request to:", url)
        print("Request data:", json.dumps(data, indent=2))
        
        response = requests.post(url, headers=headers, json=data)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running.")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_health():
    url = "http://localhost:8000/health"
    try:
        response = requests.get(url)
        print(f"\nHealth Check Status Code: {response.status_code}")
        print(f"Health Check Response: {response.json()}")
    except Exception as e:
        print(f"Health Check Error: {str(e)}")

if __name__ == "__main__":
    print("Testing Ollama API...")
    test_health()
    test_chat() 