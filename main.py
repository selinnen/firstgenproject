import webapp2
import os
import jinja2

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):  # for a get request
    



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
