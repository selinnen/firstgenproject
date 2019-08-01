import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

class EventModel(ndb.Model):
  time = ndb.StringProperty()
  event_name = ndb.StringProperty()
