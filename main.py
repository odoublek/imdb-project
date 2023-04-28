import requests
from bs4 import BeautifulSoup

headers = {
    "Accept-Language": "en-US,en;q=0.5"
}

year = input("Enter a year to filter movies: ")

# Make request to IMDb
url = f"https://www.imdb.com/search/title?title_type=feature&release_date={year}-01-01,{year}-12-31&user_rating=8.0,10.0&num_votes=5000,&sort=user_rating,desc&start=1&ref_=adv_nxt"
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the section containing the movie information
section = soup.find("div", {"class": "lister-list"})

# Extract the movie information and store it in a list of dictionaries
movies = []
for movie in section.find_all("div", {"class": "lister-item mode-advanced"}):
    title = movie.find("h3", {"class": "lister-item-header"}).find("a").text
    year = movie.find("span", {"class": "lister-item-year"}).text.strip("()")
    rating = movie.find("div", {"class": "ratings-bar"}).find("strong").text
    genre_list = [genre.strip() for genre in movie.find(
        "span", {"class": "genre"}).text.split(",")]
    genres = ", ".join(genre_list[:2])
    movies.append({"title": title, "year": year, "rating": rating, "genres": genres})

# Sort the movies in descending order
movies = sorted(movies, key=lambda x: float(x["rating"]), reverse=True)

# Print
for movie in movies[:20]:
    print(f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']} Genres: {movie['genres']}")
