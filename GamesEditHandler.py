from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from models import *
import os
import logging

class GamesEditHandler(webapp.RequestHandler):
	
	@login_required
	def get(self):
		if not users.is_current_user_admin():
			self.redirect('/')
		else:
			gameID = self.request.get("gameID")
			game = db.get(db.Key(gameID))
			template_stuff = {'gameID': gameID , 'game': game}
			path = os.path.join(os.path.dirname(__file__), 'editgame.html')
			self.response.out.write(template.render(path, template_stuff))
		
	def post(self):
		user = users.get_current_user()
		if not user:
			self.error(401)
		else:
			try:
				gameID = self.request.get("gameID")
				homeGoals = int(self.request.get("homeGoals"))
				awayGoals = int(self.request.get("awayGoals"))
				game = db.get(db.Key(gameID))
				game.homeGoals = homeGoals
				game.awayGoals = awayGoals
				game.played = True
				game.put()
				
				self.redirect("/")
			except (TypeError, ValueError):
				path = os.path.join(os.path.dirname(__file__), 'editgame.html')
				self.response.out.write(template.render(path, template_stuff))