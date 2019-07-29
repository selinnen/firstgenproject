import webapp2
import os
import jinja2
from google.appengine.api import users
from newuser import NewUser

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePage(webapp2.RequestHandler):
    def get(self):
         home_template = the_jinja_env.get_template('home.html')
         self.response.write(home_template.render())

class SignUpPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            # You shouldn't be able to get here without being logged in
            self.redirect('/')
        else:
            # Create a new CSSI user.
            user = users.get_current_user()
            new_user = NewUser(
                first_name=self.request.get('first_name'),
                last_name=self.request.get('last_name'),
                email=user.nickname())
            # Store that Entity in Datastore.
            new_user.put()
            # Show confirmation to the user. Include a link back to the index.
            self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %new_user.first_name)
    def post(self):
        user = users.get_current_user()
        if not user:
            # You shouldn't be able to get here without being logged in
            self.redirect('/')
        else:
            # Create a new CSSI user.
            user = users.get_current_user()
            new_user = NewUser(
                first_name=self.request.get('first_name'),
                last_name=self.request.get('last_name'),
                email=user.nickname())
            # Store that Entity in Datastore.
            new_user.put()
            # Show confirmation to the user. Include a link back to the index.
            self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %new_user.first_name)


class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
          signout_link_html = '<a href="%s">sign out</a>' % (
                    users.create_logout_url('/'))
          email_address = user.nickname()
          new_user = NewUser.query().filter(NewUser.email == email_address).get()
          if new_user:
              self.response.write('''
                Welcome %s %s (%s)! <br> %s <br> ''' % (
                new_user.first_name,
                new_user.last_name,
                email_address,
                signout_link_html))
          else:
            # Registration form for a first-time visitor:
            self.response.write('''
                Welcome to our site, %s!  Please sign up! <br>
                <form method="post" action="/signup">
                <input type="text" name="first_name">
                <input type="text" name="last_name">
                <input type="number" name="grade_of_students">
                <input type="submit">
                </form><br> %s <br>
                ''' % (email_address, signout_link_html))

        else:
          # If the user isn't logged in...
          login_url = users.create_login_url('/signup')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          self.response.write('Please log in.<br>' + login_html_element)








class MainPage(webapp2.RequestHandler):
    def get(self):
        main_template = the_jinja_env.get_template('main.html')
        # home_dictionary ={
        #
        # }
        self.response.write(main_template.render())
    def post(self):
        main_template = the_jinja_env.get_template('main.html')
        # home_dictionary ={
        #
        # }
        self.response.write(main_template.render())





app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', LoginPage),
    ('/main', MainPage),
    ('/signup', SignUpPage),
], debug=True)
