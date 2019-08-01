from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from quickstart import putEvents

import webapp2
import os
import jinja2
from google.appengine.api import users
from newuser import NewUser
from google.appengine.ext import ndb
import requests
from eventmodel import EventModel
import time


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePage(webapp2.RequestHandler):
    def get(self):
         home_template = the_jinja_env.get_template('templates/home.html')
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
              existing_user_template = the_jinja_env.get_template('templates/existing_user.html')
              existing_user_dictionary = {
                "new_user.first_name":new_user.first_name,
                "new_user.last_name":new_user.last_name,
                "email_address":email_address,
                "signout_link_html":signout_link_html,
              }
              self.response.write(existing_user_template.render(existing_user_dictionary))
          else:
            # Registration form for a first-time visitor:
            signup_template = the_jinja_env.get_template('templates/signup.html')
            signup_dictionary ={
                "signout_link_html" : signout_link_html,
                "email_address" : email_address,
            }
            self.response.write(signup_template.render(signup_dictionary))
        else:
          # If the user isn't logged in...
          login_url = users.create_login_url('/signup')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          signin_template = the_jinja_env.get_template('templates/signin.html')
          signin_dictionary = {
            "login_html_element":login_html_element,
          }
          self.response.write(signin_template.render(signin_dictionary))

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
              existing_user_template = the_jinja_env.get_template('templates/existing_user.html')
              existing_user_dictionary = {
                "new_user.first_name":new_user.first_name,
                "new_user.last_name":new_user.last_name,
                "email_address":email_address,
                "signout_link_html":signout_link_html,
              }
              self.response.write(existing_user_template.render(existing_user_dictionary))
          else:
            # Registration form for a first-time visitor:
            signup_template = the_jinja_env.get_template('templates/signup.html')
            signup_dictionary ={
                "signout_link_html" : signout_link_html,
                "email_address" : email_address,
            }
            self.response.write(signup_template.render(signup_dictionary))
        else:
          # If the user isn't logged in...
          login_url = users.create_login_url('/signup')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          signin_template = the_jinja_env.get_template('templates/signin.html')
          signin_dictionary = {
            "login_html_element":login_html_element,
          }
          self.response.write(signin_template.render(signin_dictionary))
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
        # self.response.write("Welcome, "+ email_address)
        email_dictionary ={
            "email_address" : email_address,
        }
        main_template = the_jinja_env.get_template('templates/main.html')
        self.response.write(main_template.render(email_dictionary))
        # signout_link_html = '<button id = "sign_out" style = " position: inheret; left: 1300px; top:12px "href="%s">Sign out</button>' % (
        #           users.create_logout_url('/'))
        # self.response.write(signout_link_html)

class AboutUsPage(webapp2.RequestHandler):
    def get(self):
        about_us_template = the_jinja_env.get_template('templates/aboutus.html')
        self.response.write(about_us_template.render())
        putEvents()
        new_event = EventModel.query().fetch()
        self.response.write(new_event)



class TimelinePage(webapp2.RequestHandler):
     def get(self):
         timeline_template = the_jinja_env.get_template('templates/timeline.html')
         self.response.write(timeline_template.render())

class BerkeleyTimelinePage(webapp2.RequestHandler):
    def get(self):
         berkeley_timeline_template = the_jinja_env.get_template('templates/berkeleytimeline.html')
         self.response.write(berkeley_timeline_template.render())
    def post(self):
        berkeley_timeline_template = the_jinja_env.get_template('templates/berkeleytimeline.html')
        self.response.write(berkeley_timeline_template.render())
class UWTimelinePage(webapp2.RequestHandler):
    def get(self):
        uw_timeline_template = the_jinja_env.get_template('templates/uwtimeline.html')
        self.response.write(uw_timeline_template.render())
class TorontoTimelinePage(webapp2.RequestHandler):
    def get(self):
        toronto_timeline_template = the_jinja_env.get_template('templates/torontotimeline.html')
        self.response.write(toronto_timeline_template.render())
class CornellTimelinePage(webapp2.RequestHandler):
    def get(self):
        cornell_timeline_template = the_jinja_env.get_template('templates/cornelltimeline.html')
        self.response.write(cornell_timeline_template.render())
class HarvardTimelinePage(webapp2.RequestHandler):
    def get(self):
        harvard_timeline_template = the_jinja_env.get_template('templates/harvardtimeline.html')
        self.response.write(harvard_timeline_template.render())

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/login', LoginPage),
    ('/dashboard', DashboardPage),
    ('/signup', SignUpPage),
    ('/timeline', TimelinePage),
    ('/aboutus', AboutUsPage),
    ('/berkeleytimeline', BerkeleyTimelinePage),
    ('/uwtimeline', UWTimelinePage),
    ('/torontotimeline', TorontoTimelinePage),
    ('/cornelltimeline', CornellTimelinePage),
    ('/harvardtimeline', HarvardTimelinePage),
], debug=True)
