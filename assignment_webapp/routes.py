"""
Route management.

This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML templates
to be displayed.

You will have to make 
"""

# Importing the required packages
from modules import *
from flask import *
import database

user_details = {}                   # User details kept for us
session = {}                        # Session information (logged in state)
page = {}                           # Determines the page information

# Initialise the application
app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


#####################################################
#   INDEX
#####################################################

@app.route('/')
def index():
    """
    Provides the main home screen if logged in.
        - Shows user playlists
        - Shows user Podcast subscriptions
        - Shows superUser status
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'User Management'

    # Get a list of user playlists
    user_playlists = None
    user_playlists = database.user_playlists(user_details['username'])
    # Get a list of subscribed podcasts
    user_subscribed_podcasts = None
    user_subscribed_podcasts = database.user_podcast_subscriptions(user_details['username'])
    # Get a list of in-progress items
    user_in_progress_items = None
    user_in_progress_items = database.user_in_progress_items(user_details['username'])
    # Data integrity checks
    if user_playlists == None:
        user_playlists = []
    
    if user_subscribed_podcasts == None:
        user_subscribed_podcasts = []

    if user_in_progress_items == None:
        user_in_progress_items = []

    return render_template('index.html',
                           session=session,
                           page=page,
                           user=user_details,
                           playlists=user_playlists,
                           subpodcasts=user_subscribed_podcasts,
                           usercurrent=user_in_progress_items)

#####################################################
#####################################################
####    User Management
#####################################################
#####################################################

#####################################################
#   LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Provides /login
        - [GET] If they are just viewing the page then render login page.
        - [POST] If submitting login details, check login.
    """
    # Check if they are submitting details, or they are just logging in
    if(request.method == 'POST'):
        # submitting details
        # The form gives back EmployeeID and Password
        login_return_data = database.check_login(
            request.form['username'],
            request.form['password']
        )

        # If it's null, saying they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('index'))

    elif(request.method == 'GET'):
        return(render_template('login.html', session=session, page=page))


#####################################################
#   LOGOUT
#####################################################

@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored user data.
    """
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out')
    return redirect(url_for('index'))

#####################################################
#####################################################
####    List All items
#####################################################
#####################################################


#####################################################
#   List Artists
#####################################################
@app.route('/list/artists')
def list_artists():
    """
    Lists all the artists in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Artists'

    # Get a list of all artists from the database
    allartists = None
    allartists = database.get_allartists()

    # Data integrity checks
    if allartists == None:
        allartists = []


    return render_template('listitems/listartists.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allartists=allartists)


#####################################################
#   List Songs
#####################################################
@app.route('/list/songs')
def list_songs():
    """
    Lists all the songs in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Songs'

    # Get a list of all songs from the database
    allsongs = None
    allsongs = database.get_allsongs()


    # Data integrity checks
    if allsongs == None:
        allsongs = []


    return render_template('listitems/listsongs.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allsongs=allsongs)

#####################################################
#   List Podcasts
#####################################################
@app.route('/list/podcasts')
def list_podcasts():
    """
    Lists all the podcasts in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List podcasts'

    # Get a list of all podcasts from the database
    allpodcasts = None
    allpodcasts = database.get_allpodcasts()

    # Data integrity checks
    if allpodcasts == None:
        allpodcasts = []


    return render_template('listitems/listpodcasts.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allpodcasts=allpodcasts)


#####################################################
#   List Movies
#####################################################
@app.route('/list/movies')
def list_movies():
    """
    Lists all the movies in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies from the database
    allmovies = None
    allmovies = database.get_allmovies()


    # Data integrity checks
    if allmovies == None:
        allmovies = []


    return render_template('listitems/listmovies.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allmovies=allmovies)


#####################################################
#   List Albums
#####################################################
@app.route('/list/albums')
def list_albums():
    """
    Lists all the albums in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get a list of all Albums from the database
    allalbums = None
    allalbums = database.get_allalbums()


    # Data integrity checks
    if allalbums == None:
        allalbums = []


    return render_template('listitems/listalbums.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allalbums=allalbums)


#####################################################
#   List TVShows
#####################################################
@app.route('/list/tvshows')
def list_tvshows():
    """
    Lists all the tvshows in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshows from the database
    alltvshows = None
    alltvshows = database.get_alltvshows()


    # Data integrity checks
    if alltvshows == None:
        alltvshows = []


    return render_template('listitems/listtvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           alltvshows=alltvshows)




#####################################################
#####################################################
####    List Individual items
#####################################################
#####################################################

#####################################################
#   Individual Artist
#####################################################
@app.route('/artist/<artist_id>')
def single_artist(artist_id):
    """
    Show a single artist by artist_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Artist ID: '+artist_id

    # Get a list of all artist by artist_id from the database
    artist = None
    artist = database.get_artist(artist_id)

    # Data integrity checks
    if artist == None:
        artist = []

    return render_template('singleitems/artist.html',
                           session=session,
                           page=page,
                           user=user_details,
                           artist=artist)


#####################################################
#   Individual Song
#####################################################
@app.route('/song/<song_id>')
def single_song(song_id):
    """
    Show a single song by song_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))
    print("IN SINGLE SONG")
    page['title'] = 'Song'

    # Get a list of all song by song_id from the database
    song = None
    song = database.get_song(song_id)
    print("GOT SONG")
    songmetadata = None
    songmetadata = database.get_song_metadata(song_id)
    print("GOT METADATA")
    # Data integrity checks
    if song == None:
        song = []

    if songmetadata == None:
        songmetadata = []
    print("PRINTING DATA")
    print(song)
    print(songmetadata)
    return render_template('singleitems/song.html',
                           session=session,
                           page=page,
                           user=user_details,
                           song=song,
                           songmetadata=songmetadata)

#####################################################
#   Query (6)
#   Individual Podcast
#####################################################
@app.route('/podcast/<podcast_id>')
def single_podcast(podcast_id):
    """
    Show a single podcast by podcast_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast     #
    #############################################################################

    page['title'] = 'Podcast' # Add the title

    podcast = None
    podcast = database.get_podcast(podcast_id)

    podcasteps = None
    podcasteps = database.get_all_podcasteps_for_podcast(podcast_id)

    podcast_genre = None
    # podcast_genre = database.get_genre_podcasts(podcast_id)

    # Data integrity checks
    if podcast == None:
        podcast = []

    if podcasteps == None:
        podcasteps = []
    
    if podcast_genre == None:
        podcast_genre = []

    # Set up some variables to manage the returns from the database fucntions
    
    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcast.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcast=podcast,
                           podcasteps=podcasteps,
                           podcast_genre=podcast_genre)

#####################################################
#   Query (7)
#   Individual Podcast Episode
#####################################################
@app.route('/podcastep/<media_id>')
def single_podcastep(media_id):
    """
    Show a single podcast epsiode by media_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast ep  #
    #############################################################################

    page['title'] = 'Postcastep' # Add the title
    podcastep = None
    podcastep = database.get_podcastep(media_id)



    # Data integrity checks
    if podcastep == None:
        podcastep = []

  

    # Set up some variables to manage the returns from the database fucntions
    
    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcastep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcastep=podcastep)


#####################################################
#   Individual Movie
#####################################################
@app.route('/movie/<movie_id>')
def single_movie(movie_id):
    """
    Show a single movie by movie_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies by movie_id from the database
    movie = None
    movie = database.get_movie(movie_id)


    # Data integrity checks
    if movie == None:
        movie = []


    return render_template('singleitems/movie.html',
                           session=session,
                           page=page,
                           user=user_details,
                           movie=movie)


#####################################################
#   Individual Album
#####################################################
@app.route('/album/<album_id>')
def single_album(album_id):
    """
    Show a single album by album_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get the album plus associated metadata from the database
    album = None
    album = database.get_album(album_id)

    album_songs = None
    album_songs = database.get_album_songs(album_id)

    album_genres = None
    album_genres = database.get_album_genres(album_id)

    # Data integrity checks
    if album_songs == None:
        album_songs = []

    if album == None:
        album = []

    if album_genres == None:
        album_genres = []

    return render_template('singleitems/album.html',
                           session=session,
                           page=page,
                           user=user_details,
                           album=album,
                           album_songs=album_songs,
                           album_genres=album_genres)


#####################################################
#   Individual TVShow
#####################################################
@app.route('/tvshow/<tvshow_id>')
def single_tvshow(tvshow_id):
    """
    Show a single tvshows and its eps in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'TV Show'

    # Get a list of all tvshows by tvshow_id from the database
    tvshow = None
    tvshow = database.get_tvshow(tvshow_id)

    tvshoweps = None
    tvshoweps = database.get_all_tvshoweps_for_tvshow(tvshow_id)

    # Data integrity checks
    if tvshow == None:
        tvshow = []

    if tvshoweps == None:
        tvshoweps = []

    return render_template('singleitems/tvshow.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshow=tvshow,
                           tvshoweps=tvshoweps)

#####################################################
#   Individual TVShow Episode
#####################################################
@app.route('/tvshowep/<tvshowep_id>')
def single_tvshowep(tvshowep_id):
    """
    Show a single tvshow episode in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshow eps by media_id from the database
    tvshowep = None
    tvshowep = database.get_tvshowep(tvshowep_id)


    # Data integrity checks
    if tvshowep == None:
        tvshowep = []


    return render_template('singleitems/tvshowep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshowep=tvshowep)

#####################################################
#   Query (10)
#   Individual Genre
#####################################################
@app.route('/genre/<genre_id>')
def single_genre(genre_id):
    """
    Show a single genre in your media server
    First, figure out what type of genre this is
    Then list all items that have that genre:
    1. Song Genre
        a. list all songs
    2. Film Genre
        a. list all tv shows and films
    3. Postcast Genre
        a. list all podcasts
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a genre       #
    #############################################################################

    page['title'] = 'Genre' # Add the title
    songgenre = None
    songgenre = database.get_genre_songs(genre_id)

    film_tvshow_genre = None
    film_tvshow_genre = database.get_genre_movies_and_shows(genre_id)

    podcast_genre = None
    # podcast_genre = database.get_genre_podcasts(genre_id)

    if len(songgenre) != 0:
        page['type'] = 'songgenre'
    elif len(film_tvshow_genre) != 0:
        page['type'] = 'film_tvshow_genre'
    elif len(podcast_genre) != 0:
        page['type'] = 'podcast_genre'
    
        
    if songgenre == None:
        songgenre = []

    if film_tvshow_genre == None:
        film_tvshow_genre = []

    if podcast_genre == None:
        podcast_genre = []

    # Identify the type of genre - you may need to add a new function to database.py to do this

    # Set up some variables to manage the returns from the database functions
    #   There are some function frameworks provided for you to do this.
    
    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/genre.html',
                           session=session,
                           page=page,
                           user=user_details,
                           songgenre=songgenre,
                           film_tvshow_genre=film_tvshow_genre,
                           podcast_genre=podcast_genre)


#####################################################
#####################################################
####    Search Items
#####################################################
#####################################################

#####################################################
#   Search TVShow
#####################################################
@app.route('/search/tvshow', methods=['POST','GET'])
def search_tvshows():
    """
    Search all the tvshows in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'TV Show Search'

    # Get a list of matching tv shows from the database
    tvshows = None
    if(request.method == 'POST'):

        tvshows = database.find_matchingtvshows(request.form['searchterm'])

    # Data integrity checks
    if tvshows == None or tvshows == []:
        tvshows = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found '+str(len(tvshows))+' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_tvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshows=tvshows)

#####################################################
#   Query (9)
#   Search Movie
#####################################################
@app.route('/search/movie', methods=['POST','GET'])
def search_movies():
    """
    Search all the movies in your media server
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for searching for #
    # a movie                                                                   #
    #############################################################################

    page['title'] = 'Movie Search' # Add the title

    movies = None

    if request.method == 'POST':
        # Set up some variables to manage the post returns
        movies = database.find_matchingmovies(request.form['searchterm'])

        # Once retrieved, do some data integrity checks on the data
    if movies == None or movies == []:
        movies = []
        page['bar'] = False
        flash("No matching movies found, please try again")

    else:
        page['bar'] = True
        flash('Found '+str(len(movies))+' results!')
        session['logged_in'] = True

        # Once verified, send the appropriate data to 

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
    return render_template('searchitems/search_movies.html',
                session=session,
                page=page,
                user=user_details,
                movies=movies)
    # else:
    #     # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    #     return render_template('searchitems/search_movies.html',
    #                        session=session,
    #                        page=page,
    #                        user=user_details)


@app.route('/search/multi', methods=['POST','GET'])
def search_multi():
    """
    Search all the multi in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Multi'

    multi = None
    search_term = request.form['searchterm']
    multi_term = search_term.split(",")
    for i in range(len(multi_term)):
        multi_term[i] = multi_term[i].split(":")
    print(multi_term)

    # Do some multi integrity checks
    if multi_term[0][0].lower() == "movie":
        movies = None
        release_year = '=release_year'
        for i in range(len(multi_term)):
            if multi_term[i][0] == 'release_year':
                release_year = multi_term[i][1]
        if request.method == 'POST':
            # Set up some variables to manage the post returns
            movies = database.multi_find_matchingmovies(multi_term[0][1].lower(),release_year)
        # Once retrieved, do some data integrity checks on the data
        if movies == None or movies == []:
            movies = []
            page['bar'] = False
            flash("No matching movies found, please try again")

        else:
            page['bar'] = True
            flash('Found '+str(len(movies))+' results!')
            session['logged_in'] = True

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_movies.html',
                    session=session,
                    page=page,
                    user=user_details,
                    movies=movies)

    elif multi_term[0][0].lower() == "song":
        songs = None
        length = '=length'
        genre = 'md_value=md_value'
        for i in range(len(multi_term)):
            if multi_term[i][0] == 'length':
                length = multi_term[i][1]
            elif multi_term[i][0] == 'genre':
                genre = """md_value='""" + multi_term[i][1] + """'"""

        if request.method == 'POST':
            # Set up some variables to manage the post returns
            songs = database.multi_find_matchingsongs(multi_term[0][1].lower(),length, genre)

        # Once retrieved, do some data integrity checks on the data
        if songs == None or songs == []:
            songs = []
            page['bar'] = False
            flash("No matching song found, please try again")
        
        else:
            page['bar'] = True
            flash('Found '+str(len(songs))+' results!')
            session['logged_in'] = True
        
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_songs.html',
                    session=session,
                    page=page,
                    user=user_details,
                    songs=songs)

    elif multi_term[0][0].lower() == "tvshow":
        tvshows = None
        season = '=season'
        episode = '=episode'
        for i in range(len(multi_term)):
            if multi_term[i][0] == 'season':
                season = multi_term[i][1]
            elif multi_term[i][0] == 'epsiode':
                episode = multi_term[i][1]

        if request.method == 'POST':
            # Set up some variables to manage the post returns
            tvshows = database.multi_find_matchingtvshows(multi_term[0][1].lower(), season, episode)

        # Once retrieved, do some data integrity checks on the data
        if tvshows == None or tvshows == []:
            tvshows = []
            page['bar'] = False
            flash("No matching song found, please try again")
        
        else:
            page['bar'] = True
            flash('Found '+str(len(tvshows))+' results!')
            session['logged_in'] = True

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_tvshows.html',
                    session=session,
                    page=page,
                    user=user_details,
                    tvshows=tvshows)


    elif multi_term[0][0].lower() == "podcast":
        podcasts = None
        podcast_last_updated = '=podcast_last_updated'

        for i in range(len(multi_term)):
            if multi_term[i][0] == 'podcast_last_updated':
                podcast_last_updated = multi_term[i][1]

        if request.method == 'POST':
            # Set up some variables to manage the post returns
            podcasts = database.multi_find_matchingpodcasts(multi_term[0][1].lower(), podcast_last_updated)

        # Once retrieved, do some data integrity checks on the data
        if podcasts == None or podcasts == []:
            podcasts = []
            page['bar'] = False
            flash("No matching song found, please try again")
        else:
            page['bar'] = True
            flash('Found '+str(len(podcasts))+' results!')
            session['logged_in'] = True

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_podcasts.html',
                    session=session,
                    page=page,
                    user=user_details,
                    podcasts=podcasts)


    return render_template('searchitems/search_multi.html',
                           session=session,
                           page=page,
                           user=user_details)


#####################################################
#   Add Movie
#####################################################
@app.route('/add/movie', methods=['POST','GET'])
def add_movie():
    """
    Add a new movie
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Movie Creation'

    movies = None
    print("request form is:")
    newdict = {}
    print(request.form)

    # Check your incoming parameters
    if(request.method == 'POST'):

        # verify that the values are available:
        if ('movie_title' not in request.form):
            newdict['movie_title'] = 'Empty Film Value'
        else:
            newdict['movie_title'] = request.form['movie_title']
            print("We have a value: ",newdict['movie_title'])

        if ('release_year' not in request.form):
            newdict['release_year'] = '0'
        else:
            newdict['release_year'] = request.form['release_year']
            print("We have a value: ",newdict['release_year'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ",newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ",newdict['storage_location'])

        if ('film_genre' not in request.form):
            newdict['film_genre'] = 'drama'
        else:
            newdict['film_genre'] = request.form['film_genre']
            print("We have a value: ",newdict['film_genre'])

        if ('artwork' not in request.form):
            newdict['artwork'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
        else:
            newdict['artwork'] = request.form['artwork']
            print("We have a value: ",newdict['artwork'])
        
        print('newdict is:')
        print(newdict)

        #forward to the database to manage insert
        movies = database.add_movie_to_db(newdict['movie_title'],newdict['release_year'],newdict['description'],newdict['storage_location'],newdict['film_genre'])


        max_movie_id = database.get_last_movie()[0]['movie_id']
        print(movies)
        if movies is not None:
            max_movie_id = movies[0]

        # ideally this would redirect to your newly added movie
        return single_movie(max_movie_id)
    else:
        return render_template('createitems/createmovie.html',
                           session=session,
                           page=page,
                           user=user_details)


#####################################################
#   Query (8)
#   Add song
#####################################################
@app.route('/add/song', methods=['POST','GET'])
def add_song():
    """
    Add a new Song
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for adding a song #
    #############################################################################

    page['title'] = 'Song Creation' # Add the title

    songs = None
    print("request form is:")
    newdict = {}
    print(request.form)

    if request.method == 'POST':
        # Set up some variables to manage the post returns

        # Once retrieved, do some data integrity checks on the data

        # Once verified, send the appropriate data to the database for insertion

        if ('song_title' not in request.form):
            newdict['song_title'] = 'Empty Song Value'
        else:
            newdict['song_title'] = request.form['song_title']
            print("We have a value: ",newdict['song_title'])

        if ('length' not in request.form):
            newdict['length'] = '0'
        else:
            newdict['length'] = request.form['length']
            print("We have a value: ",newdict['length'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ",newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ",newdict['storage_location'])

        if ('song_genre' not in request.form):
            newdict['song_genre'] = 'rock'
        else:
            newdict['song_genre'] = request.form['song_genre']
            print("We have a value: ",newdict['song_genre'])

        if ('artist_id' not in request.form):
            newdict['artist_id'] = '1'
        else:
            newdict['artist_id'] = request.form['artist_id']
            print("We have a value: ",newdict['artist_id'])

        print('newdict is:')
        print(newdict)

        #forward to the database to manage insert
        songs = database.add_song_to_db(newdict['song_title'],newdict['length'],newdict['description'],newdict['storage_location'],newdict['song_genre'], newdict['artist_id'])


        max_song_id = database.get_last_song()[0]['song_id']
        print(songs)
        if songs is not None:
            max_song_id = songs[0]
            print("SET")

        # ideally this would redirect to your newly added song
        return single_song(max_song_id)

    else:
        return render_template('createitems/createsong.html',
                           session=session,
                           page=page,
                           user=user_details)