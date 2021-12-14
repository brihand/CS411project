# CS411project

A3 Group 4 Members: Brian Sohn, Kunlin Song, Ana Souza, Melissa Sun, Danny Xu




## Spotify Playlist Generator

We attempted to create a web application primarily based on Flask that would retrive weather conditions and genearate a Spotify playlist 
based on the data. 

### History

We first wanted to follow our ideas on the project pitch but we unfortunately found it difficult to fully implement in given our timeframe.
The app required more technology stack than what we initially thought and we found it challenging to develop as we learned.
So we changed our plan to make an app that was more accessible and easier to implement.

### APIs used

We used two APIs for this project, OpenWeatherMap API and Spotify API. We also used Spotify for the OAuth 2.0 authentication. 
OpenWeatherMap API took user input (zip code) and retrieved data based on the current weather of the zip code.
Spotify API was used to connect to the user's spotify and user data. The app looked at the top songs based on the user profile and 
generated a new playlist based on the weather. 

### What we were able to do

We were able to create a first half of the app: a page where a user would login or register.
This data would be saved in the SQLlite database we used. We used SQLAlechemy to easily work with Flask.
Another part of the web application would be the actual page where a user would type a zip code to retrieve data. 
This page would then redirect for a user to sign in to Spotify using OAuth 2.0 authentication.
Then, there would be a callback to the page where it would you the generated playlist based on the weather.

### What we weren't able to do

We weren't able to connect two pages together. The idea is after the user logs in, it would redirect to the main page where
the user can send a zip code. However, we weren't able to connect these parts.
We also weren't able to use decoupled architecture; meaning we didn't really use frontend and backend for this simple web app.
We planned on using Vue JS for the frontend but because none of us were experienced enough using Vue JS, we had to drop it for this project.
Instead, the website was simply created using html files and render_template in the flask.



