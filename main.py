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

class TeamModel(db.Model):
	displayName = db.StringProperty()

class GameModel(db.Model):
	homeTeamID = db.ReferenceProperty(TeamModel, collection_name="homeTeamID")
	awayTeamID = db.ReferenceProperty(TeamModel, collection_name="awayTeamID")
	played = db.BooleanProperty()
	homeGoals = db.IntegerProperty()
	awayGoals = db.IntegerProperty()
	gameTime = db.DateTimeProperty()

class PunterModel(db.Model):
	user = db.UserProperty()
	displayName = db.StringProperty()

class BetModel(db.Model):
	gameID = db.ReferenceProperty(GameModel)
	punterID = db.ReferenceProperty(PunterModel)
	homeGoals = db.IntegerProperty()
	awayGoals = db.IntegerProperty()

class GamesHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('Hello world!')

class LeaderboardHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('Hello world!')

class BetsHandler(webapp.RequestHandler):
	def get(self):
		self.reponse.out.write('Hello world!')

class MainHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			games = GameModel.gql('ORDER BY gameTime')
			template_stuff = {'user': user,
								'logout_url': users.create_logout_url(self.request.uri),
								'games': games,
							}
			path = os.path.join(os.path.dirname(__file__), 'index.html')
			self.response.out.write(template.render(path, template_stuff))

def main():
	application = webapp.WSGIApplication([('/', MainHandler),('/leaderboard',LeaderboardHandler),('/bets',BetsHandler),('/games',GamesHandler)],debug=True)
	den = TeamModel()
	den.displayName = 'Denmark'
	den.put()
	
	swe = TeamModel()
	swe.displayName = 'Sweden'
	swe.put()
	
	game1 = GameModel()
	game1.homeTeamID = den.key()
	game1.awayTeamID = swe.key()
	game1.played = True
	game1.homeGoals = 1
	game1.awayGoals = 3
	game1.gameTime = datetime.datetime(2010,06,07,12,15)
	game1.put()
	
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
