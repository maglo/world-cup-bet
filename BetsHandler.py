from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import *
import os
import logging

class BetsHandler(webapp.RequestHandler):
	def get(self):
		punterID = self.request.get('punterID')
		gameID = self.request.get('gameID')
		
		punter = PunterModel()
		game = GameModel()
		bets = []
		template_stuff = {}
		
		user = users.get_current_user()
		if user:
			loginurl = users.create_logout_url(self.request.uri)
			loginurl_text = "Logout..."
		else:
			loginurl = users.create_login_url(self.request.uri)
			loginurl_text = "Login"
		
		if punterID and gameID:
			#sluta haxor, borde vara antingen eller
			self.redirect('/')
			return
		
		if punterID:
			logging.debug("punter " + punterID)
			punter = db.get(db.Key(punterID))
			bets = punter.betmodel_set
			bets.order('-ordinal')
			template_stuff = {'user': user,
								'loginurl': loginurl,
								'loginurl_text': loginurl_text,
								'punter': punter,
								'bets': bets,
							}
		if gameID: 
			logging.debug("game " + gameID)
			game = db.get(db.Key(gameID))
			logging.debug("game " + str(game.key()))
			bets = game.betmodel_set
			bets.order('-ordinal')
			template_stuff = {'user': user,
								'loginurl': loginurl,
								'loginurl_text': loginurl_text,
								'game': game,
								'isAdmin': users.is_current_user_admin(),
								'bets': bets,
								#'leaderboard': leaderboard,
							}

		path = os.path.join(os.path.dirname(__file__), 'bets.html')
		self.response.out.write(template.render(path, template_stuff))