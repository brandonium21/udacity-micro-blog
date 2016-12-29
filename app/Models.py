from google.appengine.ext import ndb

class Author(ndb.Model):
  	"""A sub model for representing an individual Author."""
	username = ndb.StringProperty(indexed=True)
	password = ndb.StringProperty(indexed=True)
	is_active = ndb.BooleanProperty(indexed=True)
	is_authenticated = ndb.BooleanProperty(indexed=True)
	is_anonymous = ndb.BooleanProperty(indexed=True)


class Post(ndb.Model):
	"""A main model for representing an individual Post."""
	author = ndb.UserProperty(required = True)
	content = ndb.StringProperty(indexed=True)
	title = ndb.StringProperty(indexed=True)
	updated_on = ndb.DateTimeProperty(auto_now_add = True)