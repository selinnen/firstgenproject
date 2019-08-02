# main.py
#
# from __future__ import print_function
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
#
#
# from quickstart import putEvents
#
# import webapp2
# import os
# import jinja2
# from google.appengine.api import users
# from newuser import NewUser
# from google.appengine.ext import ndb
# import requests
# from eventmodel import EventModel
# import time
#
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# from requests_toolbelt.adapters import appengine
# appengine.monkeypatch()
#
# the_jinja_env = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'],
#     autoescape=True)
#
# class HomePage(webapp2.RequestHandler):
#     def get(self):
#          home_template = the_jinja_env.get_template('templates/home.html')
#          signup_url = users.create_login_url("/signup")
#          login_url = users.create_login_url("/dashboard")
#          home_dictionary = {
#             "signup_url" : signup_url,
#             "login_url" : login_url,
#          }
#          self.response.write(home_template.render(home_dictionary))
#
# class SignUpPage(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         if user:
#           signout_link_html = '<a href="%s">sign out</a>' % (
#                     users.create_logout_url('/'))
#           email_address = user.nickname()
#           new_user = NewUser.query().filter(NewUser.email == email_address).get()
#           if new_user:
#               existing_user_template = the_jinja_env.get_template('templates/existing_user.html')
#               existing_user_dictionary = {
#                 "new_user.first_name":new_user.first_name,
#                 "new_user.last_name":new_user.last_name,
#                 "email_address":email_address,
#                 "signout_link_html":signout_link_html,
#               }
#               self.response.write(existing_user_template.render(existing_user_dictionary))
#           else:
#             # Registration form for a first-time visitor:
#             signup_template = the_jinja_env.get_template('templates/signup.html')
#             signup_dictionary ={
#                 "signout_link_html" : signout_link_html,
#                 "email_address" : email_address,
#             }
#             self.response.write(signup_template.render(signup_dictionary))
#         else:
#           # If the user isn't logged in...
#           login_url = users.create_login_url('/signup')
#           login_html_element = '<a href="%s">Sign in</a>' % login_url
#           signin_template = the_jinja_env.get_template('templates/signin.html')
#           signin_dictionary = {
#             "login_html_element":login_html_element,
#           }
#           self.response.write(signin_template.render(signin_dictionary))
#
#     def post(self):
#         first_name = self.request.get("first_name")
#         last_name = self.request.get("last_name")
#         grade_of_student = self.request.get("grade_of_student")
#         email = self.request.get("email")
#         user = NewUser(first_name = first_name, last_name = last_name, grade_of_student =grade_of_student, email = email)
#         user.put()
#         self.redirect('/dashboard')
#
# class LoginPage(webapp2.RequestHandler):
#     def doStuff(self):
#         user = users.get_current_user()
#         if user:
#           signout_link_html = '<a href="%s">sign out</a>' % (
#                     users.create_logout_url('/'))
#           email_address = user.nickname()
#           new_user = NewUser.query().filter(NewUser.email == email_address).get()
#           if new_user:
#               existing_user_template = the_jinja_env.get_template('templates/existing_user.html')
#               existing_user_dictionary = {
#                 "new_user.first_name":new_user.first_name,
#                 "new_user.last_name":new_user.last_name,
#                 "email_address":email_address,
#                 "signout_link_html":signout_link_html,
#               }
#               self.response.write(existing_user_template.render(existing_user_dictionary))
#           else:
#             # Registration form for a first-time visitor:
#             signup_template = the_jinja_env.get_template('templates/signup.html')
#             signup_dictionary ={
#                 "signout_link_html" : signout_link_html,
#                 "email_address" : email_address,
#             }
#             self.response.write(signup_template.render(signup_dictionary))
#         else:
#           # If the user isn't logged in...
#           login_url = users.create_login_url('/signup')
#           login_html_element = '<a href="%s">Sign in</a>' % login_url
#           signin_template = the_jinja_env.get_template('templates/signin.html')
#           signin_dictionary = {
#             "login_html_element":login_html_element,
#           }
#           self.response.write(signin_template.render(signin_dictionary))
#     def get(self):
#         self.doStuff()
#     def post(self):
#         self.doStuff()
#
# class DashboardPage(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         print(user)
#         email_address = user.nickname()
#         print(email_address)
#         ndb.get_context().clear_cache()
#         print("Number of users:" + str(len(NewUser.query().fetch())))
#         new_user = NewUser.query().filter(NewUser.email == email_address).get()
#         print(new_user)
#         # self.response.write("Welcome, "+ email_address)
#         email_dictionary ={
#             "email_address" : email_address,
#         }
#         main_template = the_jinja_env.get_template('templates/main.html')
#         self.response.write(main_template.render(email_dictionary))
#         # signout_link_html = '<button id = "sign_out" style = " position: inheret; left: 1300px; top:12px "href="%s">Sign out</button>' % (
#         #           users.create_logout_url('/'))
#         # self.response.write(signout_link_html)
#
# class AboutUsPage(webapp2.RequestHandler):
#     def get(self):
#         about_us_template = the_jinja_env.get_template('templates/aboutus.html')
#         self.response.write(about_us_template.render())
#
# class CalendarPage(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         new_event = EventModel.query().filter(EventModel.email == user.nickname()).order(EventModel.time).fetch()
#         calendar_template = the_jinja_env.get_template('templates/calendar.html')
#         calendar_dict = {
#             "new_event" : new_event,
#         }
#         self.response.write(calendar_template.render(calendar_dict))
#
# class LoadDataPage(webapp2.RequestHandler):
#     def get(self):
#         # putEvents()
#         flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#             'client_secret.json',
#             scopes=['https://www.googleapis.com/auth/calendar.readonly'],
#             )
#         flow.code_verifier = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
#         flow.redirect_uri = 'https://project-first-gen.appspot.com/cal-redirect'
#         authorization_url, state = flow.authorization_url(
#             # Enable offline access so that you can refresh an access token without
#             # re-prompting the user for permission. Recommended for web server apps.
#             access_type='offline',
#             # Enable incremental authorization. Recommended as a best practice.
#             include_granted_scopes='true',
#             )
#         print(authorization_url.encode('ascii', 'ignore'))
#         print(type(authorization_url.encode('ascii', 'ignore')))
#         self.redirect(authorization_url.encode('ascii', 'ignore'))
#
# class CalRedirectPage(webapp2.RequestHandler):
#     def get(self):
#         flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#             'client_secret.json',
#             scopes=['https://www.googleapis.com/auth/calendar.readonly'],
#             )
#         flow.code_verifier = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
#         flow.redirect_uri = 'https://project-first-gen.appspot.com/cal-redirect'
#
#         flow.fetch_token(code=self.request.get("code"))
#
#         credentials = flow.credentials
#
#         service = build('calendar', 'v3', credentials=credentials)
#
#         # Call the Calendar API
#         now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#         print('Getting the upcoming 10 events')
#         events_result = service.events().list(calendarId='primary', timeMin=now,
#                                             maxResults=10, singleEvents=True,
#                                             orderBy='startTime').execute()
#         events = events_result.get('items', [])
#
#         if not events:
#             print('No upcoming events found.')
#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             newEvent = EventModel(time = start, event_name = event['summary'])
#             newEvent.put()
#             time.sleep(.1)
#         self.redirect("/calendar")
#
# class TimelinePage(webapp2.RequestHandler):
#      def get(self):
#          timeline_template = the_jinja_env.get_template('templates/timeline.html')
#          self.response.write(timeline_template.render())
#
# class BerkeleyTimelinePage(webapp2.RequestHandler):
#     def get(self):
#          berkeley_timeline_template = the_jinja_env.get_template('templates/berkeleytimeline.html')
#          self.response.write(berkeley_timeline_template.render())
#     def post(self):
#         berkeley_timeline_template = the_jinja_env.get_template('templates/berkeleytimeline.html')
#         self.response.write(berkeley_timeline_template.render())
# class UWTimelinePage(webapp2.RequestHandler):
#     def get(self):
#         uw_timeline_template = the_jinja_env.get_template('templates/uwtimeline.html')
#         self.response.write(uw_timeline_template.render())
# class TorontoTimelinePage(webapp2.RequestHandler):
#     def get(self):
#         toronto_timeline_template = the_jinja_env.get_template('templates/torontotimeline.html')
#         self.response.write(toronto_timeline_template.render())
# class CornellTimelinePage(webapp2.RequestHandler):
#     def get(self):
#         cornell_timeline_template = the_jinja_env.get_template('templates/cornelltimeline.html')
#         self.response.write(cornell_timeline_template.render())
# class HarvardTimelinePage(webapp2.RequestHandler):
#     def get(self):
#         harvard_timeline_template = the_jinja_env.get_template('templates/harvardtimeline.html')
#         self.response.write(harvard_timeline_template.render())
#
# app = webapp2.WSGIApplication([
#     ('/', HomePage),
#     ('/login', LoginPage),
#     ('/dashboard', DashboardPage),
#     ('/signup', SignUpPage),
#     ('/timeline', TimelinePage),
#     ('/aboutus', AboutUsPage),
#     ('/berkeleytimeline', BerkeleyTimelinePage),
#     ('/uwtimeline', UWTimelinePage),
#     ('/torontotimeline', TorontoTimelinePage),
#     ('/cornelltimeline', CornellTimelinePage),
#     ('/harvardtimeline', HarvardTimelinePage),
#     ('/calendar', CalendarPage),
#     ('/seed-data', LoadDataPage),
#     ('/cal-redirect', CalRedirectPage),
# ], debug=True)





# main.html
# <!DOCTYPE html>
# <html lang="en" dir="ltr">
#   <head>
#     <meta charset="utf-8">
#     <title>Home</title>
#     <link rel="stylesheet" href="/stylesheets/main.css">
#     <link href="https://fonts.googleapis.com/css?family=Righteous&display=swap" rel="stylesheet">
#   </head>
#   <body>
#     <div class="intro">
#       <ul>
#       <li> <h4 id="email">Welcome, {{email_address}}</h4></li>
#         <li> <h2 id="introductory">The Ultimate Guide for High School Students</h2> </li>
#       <li> <button id="signout" onclick="window.location.href='/'">Sign Out</button></li>
#       </ul>
#     </div>
#     <img src="https://media2.giphy.com/media/fBPHYTN8wmEyiAUvTV/source.gif" alt="">
#     <button id="timeline" onclick="window.location.href='/timeline'">Timeline for You</button>
#     <button id="aboutus" onclick="window.location.href='/aboutus'">About Us</button>
#     <img src="https://media2.giphy.com/media/fBPHYTN8wmEyiAUvTV/source.gif" alt="">
#     <button id="seed-data" onclick="window.location.href='/seed-data'">Load your data</button>
#     <button id="calendar" onclick="window.location.href='/calendar'">Calendar</button>
#
#     <div class="bottom_bar"></div>
#   </body>
# </html>

#
# main.css
# body{
#   background-color: ivory;
#
# }
# h4{
#   color: black;
#   text-shadow: 1px 1px beige;
#   font-family: 'Righteous', cursive;
#   font-size: 17px;
#
# }
# h2{
#   color: black;
#   text-shadow: 1px 1px beige;
#   font-family: 'Righteous', cursive;
#   font-size: 40px;
#
# }
# button{
#   /* display: inline-block; */
#
#   padding: 8px 20px;
#   font-size: 22px;
#   cursor: pointer;
#   text-align: center;
#   outline: none;
#   box-shadow: 0 10px azure;
# }
# img{
#   padding-top:80px;
#   height:5%;
#   width:8%;
#   max-width: 100%;
#   height: auto;
#   margin-left:20px;
#   margin-top: 50px;
#   margin-right:20px;
# }
# #signout{
#   border: none;
#   color: lightblue;
#   background-color: ivory;
#   text-shadow: 2px 1px white;
#   border-radius: 15px;
#   margin-top:25px;
#
# }
# #timeline{
#   height:300px;
#   width:400px;
#   margin-top: 50px;
#   margin-left: 80px;
#   margin-right: 100px;
#   color: white;
#   background-color: lightblue;
#   text-shadow: 2px 1px #D3D3D3;
#   border-radius: 30px;
#   font-family: 'Righteous', cursive;
#   font-size: 40px;
# }
#
# #aboutus{
#   height:300px;
#   width:400px;
#   margin-top: 100px;
#   margin-left: 50px;
#   margin-right: 50px;
#   color: white;
#   background-color: lightblue;
#   text-shadow: 2px 1px #D3D3D3;
#   border-radius: 30px;
#   font-family: 'Righteous', cursive;
#   font-size: 40px;
# }
#
# #seed-data{
#   height:300px;
#   width:400px;
#   margin-top: 50px;
#   margin-left: 240px;
#   margin-right: 100px;
#   color: white;
#   background-color: lightblue;
#   text-shadow: 2px 1px #D3D3D3;
#   border-radius: 30px;
#   font-family: 'Righteous', cursive;
#   font-size: 40px;
# }
#
# #calendar{
#   height:300px;
#   width:400px;
#   margin-top: 100px;
#   margin-left: 50px;
#   margin-right: 50px;
#   color: white;
#   background-color: lightblue;
#   text-shadow: 2px 1px #D3D3D3;
#   border-radius: 30px;
#   font-family: 'Righteous', cursive;
#   font-size: 40px;
# }
#
# button:hover {background-color: aliceblue}
#
# button:active {
#   background-color: beige;
#   box-shadow: 0 5px #666;
#   transform: translateY(4px);
# }
# li{
# float: left;
#
# }
# li h2 {
#   display: block;
#   text-align: center;
#
#
# }
# li h4 {
#   display: block;
#   text-align: center;
#   position: relative;
#   top: 4px;
#
# }
# li button {
#   display: block;
#   text-align: center;
#   position: relative;
#   top: 9px;
# }
# ul {
#   list-style-type: none;
#   margin: 0;
#   padding: 0;
#   justify-content: space-between;
#   display: flex;
#   overflow: hidden;
#   border: 5px solid powderblue;
#   margin-top: 0;
#   border-style: solid;
#   border-radius: 10px;
#   padding: 5px;
#   background-color: lightblue;
# }
#
# .bottom_bar{
#   border: 5px solid powderblue;
#   border-style: solid;
#   position: absolute;
#   bottom: -400px;
#   width: 95.8%;
#   border-radius: 10px;
#   padding: 18px;
#   background-color: lightblue;
#
# }
#
#
#
#
# app.yaml
#
# runtime: python27
# api_version: 1
# threadsafe: true
#
# handlers:
# - url: /stylesheets
#   static_dir: stylesheets
# - url: /photos
#   static_dir: photos
#
# - url: /.*
#   script: main.app
#
# libraries:
# - name: webapp2
#   version: latest
# - name: jinja2
#   version: latest
# - name: ssl
#   version: latest
