import requests
import json

if __name__ == "__main__":

    URL = 'http://localhost:5000/name_pronunciation'

    names = ['Aoife', 'Caoimhe', 'Siobhan']

    for name in names:

        data = {'name': name}
        
        response = requests.post(URL, json=data)
        
        print(f"Name: {name}")
        # print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            pronunciation = response.json()['pronunciation']
            print(f"Pronunciation: {pronunciation}")
        else:
            print("Error getting pronunciation")
            
        print()