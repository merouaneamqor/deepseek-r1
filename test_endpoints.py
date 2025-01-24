import requests
import json

def test_chat_endpoint(prompt):
    url = "http://localhost:8000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\nPrompt: {prompt}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_prompts = [
        "Hello! How are you?",
        "What is the capital of France?",
        "Write a simple Python function to add two numbers",
        "Tell me a short joke"
    ]
    
    for prompt in test_prompts:
        test_chat_endpoint(prompt) 