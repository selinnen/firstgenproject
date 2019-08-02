# import webapp2


from google.appengine.ext import ndb

class EventModel(ndb.Model):
    email = ndb.StringProperty()
    time = ndb.StringProperty()
    event_name = ndb.StringProperty()
