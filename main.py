#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#import GameModel

import wsgiref.handlers
import os
import logging
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
from models import *
from BasicDataHandler import BasicDataHandler
from MainHandler import MainHandler
from ScoreHandler import ScoreHandler
from GamesHandler import GamesHandler

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

def main():
	application = webapp.WSGIApplication([('/', MainHandler),
	('/bets',BetsHandler),
	('/games',GamesHandler),
	('/gamesedit',GamesEditHandler),
	('/basicdataload', BasicDataHandler),
	('/calculatescore', ScoreHandler),], debug=True)
	
	logging.getLogger().setLevel(logging.DEBUG)
	
	util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
