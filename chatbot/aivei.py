import requests
import os

GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY")
query = "funny cat"  # Example search term
giphy_url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=1"

response = requests.get(giphy_url)
data = response.json()

if "data" in data and len(data["data"]) > 0:
    gif_url = data["data"][0]["images"]["original"]["url"]
    print("GIF URL:", gif_url)  # Should print a valid GIF link
else:
    print("No GIFs found!")
