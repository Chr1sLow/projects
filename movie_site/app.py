import requests
import sqlite3
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

OMDB_API_KEY = "dc8fb52a"
TMDB_API_KEY = "66e114071f5c4a81880dd803bb115b1e"

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# function to create db on sqlite3
def get_db_connection():
    """Create db connection."""
    conn = sqlite3.connect('movie.db')
    conn.row_factory = sqlite3.Row
    return conn

# profile page
@app.route("/", methods=["GET", "POST"])
def index():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    detailed_movies = []

    for movie in data["results"]:
        tmdb_id = movie["id"]

        details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()
        
        detailed_movies.append(details_data)

    return render_template("index.html", movies=detailed_movies)


@app.route("/list", methods=["GET", "POST"])
def list():
    if session.get("user_id") is None:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"], ))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM movie_ratings WHERE user_id = ?", (session["user_id"], ))
    user_ratings = cursor.fetchall()

    conn.close()

    return render_template("list.html", user=user["username"], list=user_ratings)


# register page
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        cursor = conn.cursor()

        # checks if and password is not empty
        if not username:
            return render_template("register.html", error="username")
        if not password:
            return render_template("register.html", error="password")
        
        cursor.execute("SELECT username FROM users WHERE username = ?", (username, ))
        
        if cursor.fetchone():
            return render_template("register.html", taken_name=True)

        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, generate_password_hash(password)))
        conn.commit()

        conn.close()

        return redirect("/login")

    return render_template("register.html")

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Page"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("login.html", error="username")
        if not password:
            return render_template("login.html", error="password")
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username, ))
        user = cursor.fetchone()

        conn.close()

        if not user or not check_password_hash(user["hash"], password):
            return render_template("login.html", wrong_login="True")
        
        session["user_id"] = user["id"]
        return redirect("/")

    return render_template("login.html")

# search bar for movies/shows
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        movie_index = []
        movie_title = request.form.get("title")

        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={movie_title}&page=1"
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            movie_index.extend(data["Search"])
        else:
            return render_template("search.html", error=True)

        return render_template("search.html", movies=movie_index)

    return render_template("search.html")

# movie page showing data on movie/show
@app.route("/movie_page", methods=["GET", "POST"])
def movie_page():
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        movie_rating = request.form.get("rating")

        print(movie_id)

        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie_id}"
        response = requests.get(url)
        data = response.json()

        if not data["Response"]:
            return render_template("search.html", error=True)
        
        if movie_rating:
            conn = get_db_connection()
            cursor = conn.cursor()
            title = data["Title"]
            id = data["imdbID"]

            cursor.execute("SELECT movie_title FROM movie_ratings WHERE movie_title = ? and user_id = ?", (title, session["user_id"], ))

            if cursor.fetchone():
                cursor.execute("UPDATE movie_ratings SET rating = ? WHERE imdb_id = ? and user_id = ?", (movie_rating, id, session["user_id"], ))
            else:
                cursor.execute("INSERT INTO movie_ratings (user_id, movie_title, imdb_id, rating, poster) VALUES (?, ?, ?, ?, ?)", (session["user_id"], title, id, movie_rating, data["Poster"], ))
            conn.commit()
            conn.close()
            
            redirect("/")
            
        return render_template("movie_page.html", movie=data)