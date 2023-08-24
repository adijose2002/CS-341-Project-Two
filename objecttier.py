# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
    def __init__(movie, Movie_ID, Title, Release_Year):
        movie.movieId = Movie_ID
        movie.releaseYear = Release_Year
        movie.title = Title

        @property
        def Movie_ID(movie):
            return movie.movieId

        @property
        def Release_Year(movie):
            return movie.releaseYear

        @property
        def Title(movie):
            return movie.title


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
    def __init__(movie, Movie_ID, Title, Release_Year, Num_Reviews, Avg_Rating):
        movie.movieId = Movie_ID
        movie.title = Title
        movie.releaseYear = Release_Year
        movie.numReviews = Num_Reviews
        movie.avgRating = Avg_Rating

        @property
        def Movie_ID(movie):
            return movie.movieId

        @property
        def Title(movie):
            return movie.title

        @property
        def Release_Year(movie):
            return movie.releaseYear

        @property
        def Num_Reviews(movie):
            return movie.numReviews

        @property
        def Avg_Rating(movie):
            return movie.avgRating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
    def __init__(
        movie,
        Movie_ID,
        Title,
        Release_Date,
        Runtime,
        Original_Language,
        Budget,
        Revenue,
        Num_Reviews,
        Avg_Rating,
        Tagline,
    ):
        movie.movieId = Movie_ID
        movie.title = Title
        movie.releaseDate = Release_Date
        movie.runTime = Runtime
        movie.ogLanguage = Original_Language
        movie.budget = Budget
        movie.revenue = Revenue
        movie.numReviews = Num_Reviews
        movie.avgRating = Avg_Rating
        movie.tagLine = Tagline
        movie.genres = []
        movie.prodCompanies = []

        @property
        def Movie_ID(movie):
            return movie.movieId

        @property
        def Title(movie):
            return movie.title

        @property
        def Release_Date(movie):
            return movie.releaseDate

        @property
        def Runtime(movie):
            return movie.runTime

        @property
        def Original_Language(movie):
            return movie.ogLanguage

        @property
        def Budget(movie):
            return movie.budget

        @property
        def Revenue(movie):
            return movie.revenue

        @property
        def Num_Reviews(movie):
            return movie.numReviews

        @property
        def Avg_Rating(movie):
            return movie.avgRating

        @property
        def Tagline(movie):
            return movie.tagLine

        @property
        def Genres(movie):
            return movie.genres

        @property
        def Production_Companies(movie):
            return movie.prodCompanies


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
    sql = "SELECT count() FROM Movies"
    mov = datatier.select_one_row(dbConn, sql)

    if mov is None:
        return -1

    return mov[0]


##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    sql = "SELECT count() FROM Ratings"
    rev = datatier.select_one_row(dbConn, sql)

    if rev is None:
        return -1

    return rev[0]
  

##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by movie id;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
    sql = "SELECT Movie_Id, Title, strftime('%Y', DATE(Release_Date)) FROM Movies WHERE Title LIKE '" + pattern + "' ORDER BY Title ASC"
    list = []
    if list is None:
        return list

    for i in datatier.select_n_rows(dbConn, sql):
        movie = Movie(i[0], i[1], i[2])
        list.append(movie)

    return list


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
    sql = """Select movies.Movie_ID, title, date(Release_Date), Runtime, Original_Language, Budget, Revenue From Movies where movies.Movie_ID = ?"""

    sqlTwo = """Select movie_ID, count(rating), AVG(Rating) from ratings where movie_ID = ?"""

    sqlThree = """Select movie_ID, Tagline from movie_Taglines where movie_ID = ?"""

    sqlFour = """ select Movie_ID, Genre_Name from Movie_Genres join Genres On Movie_Genres.Genre_ID = Genres.Genre_ID WHERE Movie_ID = ? ORDER BY Genre_Name ASC"""

    sqlFive = """select Movie_ID, Company_Name from Movie_Production_Companies join Companies on Movie_Production_Companies.Company_ID = Companies.Company_ID where Movie_ID = ? order by Company_Name ASC"""

    row = datatier.select_one_row(dbConn, sql, [movie_id])
    rating = datatier.select_one_row(dbConn, sqlTwo, [movie_id])
    tagline = datatier.select_one_row(dbConn, sqlThree, [movie_id])

    if not row:
        return None
    x = rating[1]
    average = rating[2]

    if tagline is None or tagline == ():
        position = ""
    else:
        position = tagline[1]
    if average is None:
        average = 0
    temp = MovieDetails(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        x,
        average,
        position,
        [],
        [],
    )

    genre = datatier.select_n_rows(dbConn, sqlFour, [movie_id])
    if genre is None:
        pass
    else:
        for i in genre:
            temp.genres.append(i[1])

    change = datatier.select_n_rows(dbConn, sqlFive, [movie_id])
    if change is None:
        pass
    else:
        for i in change:
            temp.productionCompanies.append(i[1])

    return temp


##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
    sql = (
        "SELECT Movies.Movie_ID, Title, strftime('%Y',DATE(Release_Date)), COUNT(Rating) as NumReviews, AVG(Rating) FROM Movies INNER JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID GROUP BY Movies.Movie_ID HAVING NumReviews >= "
        + str(min_num_reviews)
        + " ORDER BY AVG(Rating) DESC LIMIT "
        + str(N)
    )
    topN = []
    for i in datatier.select_n_rows(dbConn, sql):
        movie = MovieRating(i[0], i[1], i[2], i[3], i[4])
        topN.append(movie)
    if len(topN) != 0:
        return topN
    else:
        return []

      
##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
    sql = """SELECT Movie_ID
  from Movies
  Where Movie_ID = ?"""

    insert = """INSERT INTO Ratings(Movie_ID, Rating) VALUES (? , ?)"""

    row = datatier.select_one_row(dbConn, sql, [movie_id])

    if not row or row == ():
        return 0
    else:
        pop = datatier.perform_action(dbConn, insert, [movie_id, rating])
    if pop == -1:
        return 0
    else:
        return 1


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    sql = """select Movie_ID from Movies where Movie_ID = ?"""
    check = """select movie_ID, Tagline from Movie_Taglines where Movie_ID = ?"""
    update = """UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_ID = ?"""
    insert = """INSERT INTO Movie_Taglines(Movie_ID, Tagline) VALUES (? , ?)"""

    row = datatier.select_one_row(dbConn, sql, [movie_id])

    if row is None or row == ():
        return 0

    rowOne = datatier.select_one_row(dbConn, check, [movie_id])

    if rowOne:
        success = datatier.perform_action(dbConn, update, [tagline, movie_id])

        if success == -1:
            return 0
        else:
            return 1
    else:
        success = datatier.perform_action(dbConn, insert, [movie_id, tagline])
        if success == -1:
            return 0
        else:
            return 1
