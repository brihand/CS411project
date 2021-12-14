from flask import Flask, request, redirect, g, render_template
import requests
import urllib
import urllib.parse
import json
import iframe
import spotify
import weather
import config


app = Flask(__name__)

# Weather Data
weather_id = 0
weather_word = " "


# Weather App Id
WEATHER_APP_ID = config.WEATHER_APP_ID

# OpenWeatherMap URLS
WEATHER_API_BASE_URL = "http://api.openweathermap.org/data"
WEATHER_API_VERSION = "2.5"
WEATHER_API_URL = "{}/{}/weather".format(WEATHER_API_BASE_URL, WEATHER_API_VERSION)

# Port number
PORT = spotify.PORT

@app.route("/")
def weather():
    return render_template('weather.html')

@app.route('/', methods=['POST'])
def weather_post():
    global weather_id
    global weather_word

    zipcode = request.form['text']
    state = 'us'
    weather_api_endpoint = "{}?zip={},{}&appid={}".format(WEATHER_API_URL,zipcode,state,WEATHER_APP_ID)
    weather_response = requests.get(weather_api_endpoint)
    weather_data = json.loads(weather_response.text)
    raw_weather_data_from_zipcode = weather_data
    loose_weather_data = raw_weather_data_from_zipcode.get("weather")[0]
    global_weather = loose_weather_data.get("id")
    weather_word = loose_weather_data.get("main")

    global_weather_parse = global_weather // 100
    if global_weather == 800:
        weather_id = 0
        weather_word = "sunny"
    elif global_weather_parse == 8:
        weather_id = 1
        weather_word = "cloudy"
    elif global_weather_parse == 2 or global_weather_parse == 3 or  global_weather_parse == 5:
        weather_id = 2
        weather_word = "rainy"
    elif global_weather_parse == 6:
        weather_id = 3
        weather_word = "snowy"

    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in spotify.auth_query_parameters.items()])
    auth_url = "{}/?{}".format(spotify.SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    global weather_id
    global weather_word

    authorization_header = spotify.getAuthorizationHeader()

    profile_data = spotify.getProfileData(authorization_header)


    top_track_playlist_list = [track.get('id') for track in spotify.getTopTrack(authorization_header).get('items')]

    audio_feature_list = [(x, spotify.getAudioFeatureFromTrack(authorization_header, x)) for x in top_track_playlist_list]
    sort_variable_list = [(x[0], x[1].get('valence'), x[1].get('instrumentalness'), x[1].get('energy'),
                           x[1].get('danceability'), x[1].get('acousticness'))
                          for x in audio_feature_list]

    vw = 0 # vw = valence weight
    iw = 0 # iw = instrumentalness weight
    ew = 0 # ew = energy weight
    dw = 0 # dw = danceability weight
    aw = 0 # aw = acousticness weight

    if weather_id == 0:
        # Sunny
        vw = 1.6
        iw = -1.05
        ew = 1.7
        dw = 1.3
        aw = -1.3
    elif weather_id == 1:
        # Cloudy
        vw = -1.3
        iw = 1.5
        ew = -1.6
        dw = -1.2
        aw = 1.1
    elif weather_id == 2:
        # Rain
        vw = -1.5
        iw = 1.2
        ew = -1.7
        dw = -1.3
        aw = 1.8
    elif weather_id == 3:
        # snow
        vw = -1.15
        iw = 1.5
        ew = -1.5
        dw = -1.03
        aw = 1.2

    calculated_sort_variable_list = sorted([(track_data[0],
                                             ((track_data[1] * vw) + (track_data[2] * iw) + (track_data[3] * ew) + (
                                                     track_data[4] * dw) + (track_data[5] * aw))
                                             )
                                            for track_data in sort_variable_list], key=lambda sort_key: sort_key[1],
                                           reverse=True)

    recommendation_tracks = spotify.getRecommendationThroughTracks(authorization_header, [x[0] for x in calculated_sort_variable_list[:5]], []).get("tracks")

    create_playlist = spotify.postBlankPlaylist(authorization_header, weather_word, profile_data.get('id'))
    post_tracks_playlist = spotify.postTrackToPlaylist(authorization_header,[x.get('id') for x in recommendation_tracks],create_playlist[1])

    return render_template("index.html",sorted_array=iframe.getIframePlaylist(create_playlist[1]) ,weather_word=weather_word)

if __name__ == "__main__":
    app.run(debug=True,port=PORT)