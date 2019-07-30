import webapp2
import os
import jinja2
from google.appengine.api import users
from newuser import NewUser
from google.appengine.ext import ndb

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePage(webapp2.RequestHandler):
    def get(self):
         home_template = the_jinja_env.get_template('home.html')
         signup_url = users.create_login_url("/signup")
         login_url = users.create_login_url("/dashboard")
         home_dictionary = {
            "signup_url" : signup_url,
            "login_url" : login_url,
         }
         self.response.write(home_template.render(home_dictionary))

class SignUpPage(webapp2.RequestHandler):
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
                <input type="number" name="grade_of_student">
                <input type="hidden" name="email" value ="%s">
                <input type="submit">
                </form><br> %s <br>
                ''' % (email_address, email_address, signout_link_html))
        else:
          # If the user isn't logged in...
          login_url = users.create_login_url('/signup')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          self.response.write('Please log in.<br>' + login_html_element)

    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        grade_of_student = self.request.get("grade_of_student")
        email = self.request.get("email")
        user = NewUser(first_name = first_name, last_name = last_name, grade_of_student =grade_of_student, email = email)
        user.put()
        self.redirect('/dashboard')

class LoginPage(webapp2.RequestHandler):
    def doStuff(self):
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
    def get(self):
        self.doStuff()
    def post(self):
        self.doStuff()

class DashboardPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        print(user)
        email_address = user.nickname()
        print(email_address)
        ndb.get_context().clear_cache()
        print("Number of users:" + str(len(NewUser.query().fetch())))
        new_user = NewUser.query().filter(NewUser.email == email_address).get(use_cache=False, use_memcache=False)
        print(new_user)
        self.response.write("Welcome, "+ email_address)

        main_template = the_jinja_env.get_template('main.html')
        # home_dictionary ={
        #
        # }
        self.response.write(main_template.render())
        signout_link_html = '<a href="%s">sign out</a>' % (
                  users.create_logout_url('/'))
        self.response.write(signout_link_html)
    def post(self):
        user.put()
        # user = users.get_current_user()
        # email_address = user.nickname()
        # new_user = NewUser.query().filter(NewUser.email == email_address).get()
        main_template = the_jinja_env.get_template('main.html')
        # home_dictionary ={
        #
        # }
        self.response.write(main_template.render())
        signout_link_html = '<a href="%s">sign out</a>' % (
                  users.create_logout_url('/'))

        self.response.write(signout_link_html)

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', LoginPage),
    ('/dashboard', DashboardPage),
    ('/signup', SignUpPage),
], debug=True)
