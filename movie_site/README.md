# Movie Rating Site
#### Video Demo:  <https://youtu.be/h59yNYAy7SQ>
#### Description:

This is a movie site that allows users to log in and track what movies/shows that they have watched. They can rate it on a scale of 1-10 to remember their taste in movies in the future. The site was made using HTML and CSS and Python with Flask.
## Features

- Rating movies on a scale of 1-10
- Getting info on the most recent movies
- Stores data in a database so that info saves
- Password is hashed so only user knows their own password

## App.py
### Index
The home page for the website. It shows the most recent movies that have come out and allows users to easily click on them to get to their respective page quickly.

### Register
Allows the user to register for an account. The user still has access to specific features such as searching and finding info on movies. You can only rate movies if you have already registered. If the username is already taken, they you will not be able to use that name. The user is saved into a database that to make sure that the user is remembered.

### Login
Allows the user to access an account that they know the info of. Once the user is logged in, they will be able to rate and save movies into their list. If the user types in the wrong password, they will not be able to log in to that account until they get it correct. It does this by checking if the username is in the SQL databse and check if the password matches.

### Search
The user can search up the title of any movie/show that they want and they will get results that have what they typed in the title. If there is a typo, then the result may not pop up. The results only show a limited result instead of all the movies with that title in its name. This is to limit the amount of titles to prevent the page from getting too long. Made using Flask and the OMDB api, it takes all the movies with what the user input and prints them all out. If the movie does not exist in the api, then it will show an error telling the user that the movie does not exist. 

### Movie_page
Shows the info of the movie such as the title, poster, synopsis, and ratings. All the info is taken from the OMDB and TMDB movie api. The api's give info on the poster, synopsis, and ratings. On the bottom, the user can input a number from 1-10 and it will send that rating and movie to their list.

### Home
The home page shows the most recent movies to come out in theatres. This is done using the TMDB api as it has access to the recent movies. We are able to connect the TMDB and OMDB api's because they both share the same IMDB id's for each movie. As time goes, the recent movies should change to fit the time the user is on the page.

### List
Shows the data of what the user has rated. Clicking on the poster or the title will send the user to the movie page in the case they want to change their rating. Changing the rating will update the rating on the list to the new rating that they have input. The list is different for each person as each user has watched different shows. It does this by saving the user id when the user rates the show and putting it in the database. When the user goes into the list page, the program will grab the list of movies and ratings based on the user id. This makes it so that the users list is unique.
## HTML & CSS

HTML and CSS were used to design the front end of the program. Bootstrap was also used alongisde CSS to design the site. The site uses Flask to connect the functionality with Python.
## Future Features

- Order list of ratings based on how high they are
- Show some movies even if there is a typo in search
- Add feature to show if user is watching or plan to watch a movie/show
- Most popular section on Home page
