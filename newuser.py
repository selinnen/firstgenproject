import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

class NewUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()
  grade_of_student=ndb.StringProperty()
