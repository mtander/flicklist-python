import webapp2
import random

class Index(webapp2.RequestHandler):
    def getRandomMovie(self):
        myList = [
        "Jurassic Park", "American Beauty", "The Curious Case of Benjamin Button",
        "Star Wars", "Aladdin"
        ]
        randint = random.randint(0,len(myList)-1)
        movie = myList[randint]
        return movie     
    def get(self):
        #self.response.write('Hello, Summer of Code!')
        
        movie = self.getRandomMovie()
        
        content = "<h1>My Favorite Movie</h1>"
        content += "<p>" + movie + "</p>"
        
        self.response.write(content)
    
app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
