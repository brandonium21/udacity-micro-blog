from functools import wraps
from google.appengine.api import users
from flask import redirect, request, url_for

def login_needed(view):
	@wraps(view)
	def decorated_view(*args, **kwargs):
	    if not users.get_current_user():
	        return redirect(users.create_login_url(url_for('show_allpost')))
	    return view(*args, **kwargs)
	return decorated_view