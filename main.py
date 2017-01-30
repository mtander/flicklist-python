# https://cloud.google.com/appengine/docs/python/getting-started/handling-user-input-form
        
        #validation for add--check 3 things:
        #   1) includes html tags.  use cgi.escape
        #   2) no movie included.  Display "Please specify the name of the movie you want to add"
        #        , also reject form submission and redirect back to home page
        #   3) trying to add a movie that sucks. Redirect to homepage, display
        #       "Trust me, you don't want to add 'moviename' to your Watchlist"

import webapp2
import cgi

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">FlickList</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

terrible_movies = ['Texas Chainsaw Massacre','Paul Blart: Mall Cop', 
            'The Legend of Tarzan', 'The Last Airbender', 'Requiem for a Dream']

def getCurrentWatchlist():
    """ Returns the user's current watchlist """
    myList = [
        "Jurassic Park", "American Beauty", "The Curious Case of Benjamin Button",
        "Star Wars", "Aladdin"
        ]
    #won't be able to save this until we work on databases.  For now, just return hardcoded list.
    return myList
    
class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):

        edit_header = "<h3>Edit My Watchlist</h3>"

        # a form for adding new movies
        add_form = """
        <form action="/add" method="post">
            <label>
                I want to add
                <input type="text" name="new-movie"/>
                to my watchlist.
            </label>
            <input type="submit" value="Add It"/>
        </form>
        """
  
        #build dropdown for crossoff_form
        # the "{0}" is an indicator to the format method that you want it replaced
        # by the first (index 0) parameter of format
        # http://stackoverflow.com/questions/6682806/what-does-0-mean-in-this-python-string
        crossoff_options = ""
        for movie in getCurrentWatchlist():
            crossoff_options += '<option value="{0}">{0}</option>'.format(movie)
        
        # a form for crossing off movies
        crossoff_form = """
        <form action="/cross-off" method="post">
            <label>
                I want to cross off
                <select name="crossed-off-movie"/>
                    {0}
                </select>
                from my watchlist.
            </label>
            <input type="submit" value="Cross It Off"/>
        </form>
        """.format(crossoff_options)
        
        # if error, display it
        # even though we build error, still escape it w/ cgi so a malicious user
        # can't pass in something that will break the html
        error = self.request.get("error") # Gets error from query parameter (/?error="blahblah")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = "<p class='error'>" + error_esc + "</p>"
        else:
            error_element = ''

        page_content = edit_header + add_form + crossoff_form + error_element
        content = page_header + page_content + page_footer
        self.response.write(content)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):   
        # look inside the request to figure out what the user typed
        new_movie = self.request.get("new-movie")
        new_movie = cgi.escape(new_movie, quote=True)
        
        #if user typed nothing, redirect & yell at them
        if isBlank(new_movie):
            #error
            error = "Please specify the name of the movie you want to add"
            #redirect
            self.redirect("/?error=" + error)
        elif new_movie in terrible_movies:
            error = "Trust me, you don't want to add {} to your Watchlist".format(new_movie)
            self.redirect("/?error=" + error)
            
        # build response content
        new_movie_element = "<strong>" + new_movie + "</strong>"
        sentence = new_movie_element + " has been added to your Watchlist!"

        content = page_header + "<p>" + sentence + "</p>" + page_footer
        self.response.write(content)



class CrossOffMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/cross-off'
        e.g. www.flicklist.com/cross-off
    """

    def post(self):
        # look inside the request to figure out what the user typed
        crossed_off_movie = self.request.get("crossed-off-movie")

        if(crossed_off_movie in getCurrentWatchlist()) == False:
            #User tried to enter movie that isn't in list, so redirect them
            #back to front page and display error
            
            #create error message
            error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)
        
            #redirect to homepage, and include error as query parameter in URL
            self.redirect("/?error=" + error)
        
        # build response content (will not reach this point if already redirected)
        crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
        confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."

        content = page_header + "<p>" + confirmation + "</p>" + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/cross-off', CrossOffMovie)
], debug=True)
