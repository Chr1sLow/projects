import requests

api_key = "66e114071f5c4a81880dd803bb115b1e"

url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}"
response = requests.get(url)
data = response.json()

for movie in data["results"]:
    print(f"Title: {movie['title']}")
    print(f"Release Date: {movie['release_date']}")
    print(f"Overview: {movie['overview']}\n")
    print(f"Backdrop: {movie['backdrop_path']}")
