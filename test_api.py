import requests

try:
    response = requests.get('http://127.0.0.1:5000/quiz/easy')
    if response.status_code == 200:
        print("API works")
    else:
        print("API not responding")
except Exception as e:
    print(f"Error: {e}")