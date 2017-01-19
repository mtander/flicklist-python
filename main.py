import webapp2
import random

class Index(webapp2.RequestHandler):

    def getRandomMovie(self):

        # TODO: make a list with at least 5 movie titles
        oscarMovies = ["La La Land", "Nocturnal Animals", "Jackie", "Arrival", "The Blind Christ"]
        # TODO: randomly choose one of the movies, and return it

        return random.choice(oscarMovies)

    def get(self):
        # choose a movie by invoking our new function
        movie = self.getRandomMovie()

        # build the response string
        content = "<h1>Movie of the Day</h1>"
        content += "<p>" + movie + "</p>"

        # choose another movie
        movie = self.getRandomMovie()

        content += "<h1>Tomorrow's Movie</h1>"
        content += "<p>" + movie + "</p>"

        # TODO: pick a different random movie, and display it under
        # the heading "<h1>Tommorrow's Movie</h1>"

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
