from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from models import *
import os
import logging

class ScoreHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		if not users.is_current_user_admin():
			self.redirect('/')
		else:
			q = db.GqlQuery("SELECT * FROM GameModel WHERE played = :played AND scored = :scored", played=True, scored=False)
			game = q.get()
			
			
			if not game:
				logging.debug("NONE")
				self.redirect('/')
				return
			
			#for game in games:
			logging.debug(game.homeTeam.displayName + "-" + game.awayTeam.displayName)
			
			for bet in game.betmodel_set:
				score = 0
				punter = bet.punter
				
				bettedResult = 0
				if bet.homeGoals > bet.awayGoals:
					bettedResult = 1
				if bet.homeGoals < bet.awayGoals:
					bettedResult = -1
				
				actualResult = 0
				if game.homeGoals > game.awayGoals:
					actualResult = 1
				if game.homeGoals < game.awayGoals:
					actualResult = -1
				
				if bettedResult == actualResult:
					score += 2
				
				if game.homeGoals == bet.homeGoals and game.awayGoals == bet.awayGoals:
					score += 4
				
				bet.score = score
				bet.put()
				
				punter.score += score
				punter.put()
				
			game.scored = True
			game.put()
				
			self.redirect('/')