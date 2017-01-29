import webapp2

class Index(webapp2.RequestHandler):
    def get(self):
        #self.response.write('Hello, Summer of Code!')
        
        movie = self.getRandomMovie()
        
        content  = "<h1>Movie of the Day</h1>"
        content += "<p>" + movie + "</p>"
        
        self.response.write(content)
        
    def getRandomMovie(self):
        #return a hardcoded string of a movie title
        return "The Big Lebowski"
    
app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
