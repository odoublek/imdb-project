import requests
from bs4 import BeautifulSoup


def get_top_rated_movies(year=None, genre=None):
    base_url = "https://www.imdb.com/search/title"
    params = {
        "title_type": "feature",
        "user_rating": "8.0,10.0",
        "num_votes": "5000,",
        "sort": "user_rating,desc",
        "start": 1,
        "ref_": "adv_nxt",
    }

    if year:
        params["release_date"] = f"{year}-01-01,{year}-12-31"

    if genre:
        params["genres"] = genre

    headers = {
        "Accept-Language": "en-US,en;q=0.5"
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    section = soup.find("div", class_="lister-list")

    movies = []
    for movie in section.find_all("div", class_="lister-item mode-advanced"):
        title = movie.find("h3", class_="lister-item-header").find("a").text
        year = movie.find("span", class_="lister-item-year").text.strip("()")
        rating = movie.find("div", class_="ratings-bar").find("strong").text
        genre_list = [genre.strip() for genre in movie.find(
            "span", class_="genre").text.split(",")]
        genres = ", ".join(genre_list[:2])
        movies.append({"title": title, "year": year,
                      "rating": rating, "genres": genres})

    movies = sorted(movies, key=lambda x: float(x["rating"]), reverse=True)

    return movies


def main():
    print("Options:")
    print("1. View current top 20 list")
    print("2. Filter by year")
    print("3. Filter by genre")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        movies = get_top_rated_movies()
        if not movies:
            print("No top-rated movies found.")
        else:
            print("Top-rated movies:")
            for movie in movies[:20]:
                print(
                    f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']} Genres: {movie['genres']}")

    elif choice == "2":
        year = input("Enter a year to filter movies: ")
        try:
            year = int(year)
        except ValueError:
            print("Invalid year format. Please enter a valid year.")
            return
        movies = get_top_rated_movies(year)
        if not movies:
            print(f"No top-rated movies found for the year {year}")
        else:
            print(f"Top-rated movies for the year {year}:")
            for movie in movies[:20]:
                print(
                    f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']} Genres: {movie['genres']}")

    elif choice == "3":
        genre = input("Enter a genre to filter movies: ")
        movies = get_top_rated_movies(genre=genre)
        if not movies:
            print(f"No top-rated movies found for the genre {genre}")
        else:
            print(f"Top-rated movies for the genre {genre}:")
            for movie in movies[:20]:
                print(
                    f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']} Genres: {movie['genres']}")

    else:
        print("Invalid choice. Please enter a valid option (1/2/3).")


if __name__ == "__main__":
    main()
