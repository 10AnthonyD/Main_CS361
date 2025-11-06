import requests
import os

# Store your API key securely (e.g., environment variables)
RAWG_API_KEY = "your_rawg_api_key"

def get_game_image_url(game_title):
    url = f"https://api.rawg.io/api/games?search={game_title}&key={RAWG_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['results']:
            # Return the URL of the first game found
            return data['results'][0].get('Header image', '')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
    return ''

