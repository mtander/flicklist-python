import webapp2
import random

#html for top of page (note-end html tag, end body tag not included)
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):
        
        header = "<h3>Edit My Watchlist</h3>"
        
        #Form for adding new movies
        #   action: where to send the form-data to (URL)
        #   method: tells whether in /add, will be using def get(self) or def post(self)
        #           (for submitting information, should generally be post?)
        #   label: caption for an item in a user interface
        #   inputs, 2 types: 1) blank space to add movie; 2) submit button for form
        #
        add_form = """
        <form action="/add" method="post">
            <label>
                I want to add <input type="text" name="new-movie" />
                to my watchlist.
            </label>
            <input type="submit" value="Add It" />
        </form>
        """

        cross_off_form = """
        <form action="/cross_off" method="post">
            <label>
                I want to cross off <input type="text" name="cross-off-movie" />
                from my watchlist.
            </label>
            <input type="submit" value="Cross Off" />
        </form>
        """
        
        content = page_header + header + add_form + cross_off_form + page_footer

        self.response.write(content)

class CrossOffMovie(webapp2.RequestHandler):
    """ Handles request coming in to '/cross_off'
        e.g. www.flicklist.com/cross_off
    """
    
    def post(self):
        #get movie to cross off from user input (based on input name "cross-off-movie")
        cross_off_movie = self.request.get("cross-off-movie")
        
        #build response
        par = "<p><strike>" + cross_off_movie + "</strike>" + " has been crossed off your Watchlist.</p>"
        content = page_header + par + page_footer
        
        self.response.write(content)
        
class AddMovie(webapp2.RequestHandler):
    """ Handles request coming in to '/add'
        e.g. www.flicklist.com/add
    """
    
    def post(self):
        #get movie from user input (based on name of input, in this case "new-movie")
        new_movie = self.request.get("new-movie")
        
        #build response content
        msg = "<strong>" + new_movie + "</strong>"
        msg += " has been added to your Watchlist!"
        
        #builds message into paragraph; surrounds w/ header & footer (contain body and html tags)
        content = page_header + "<p>" + msg + "</p>" + page_footer
        
        self.response.write(content)
        
app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/cross_off', CrossOffMovie)
], debug=True)
