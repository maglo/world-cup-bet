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

class TeamModel(db.Model):
	displayName = db.StringProperty()

class GameModel(db.Model):
	homeTeam = db.ReferenceProperty(TeamModel, collection_name="homeTeam")
	awayTeam = db.ReferenceProperty(TeamModel, collection_name="awayTeam")
	played = db.BooleanProperty()
	homeGoals = db.IntegerProperty()
	awayGoals = db.IntegerProperty()
	gameTime = db.DateTimeProperty()

class PunterModel(db.Model):
	user = db.UserProperty()
	displayName = db.StringProperty()
	score = db.IntegerProperty()
	rank = db.IntegerProperty()
	prevRank = db.IntegerProperty()

class BetModel(db.Model):
	game = db.ReferenceProperty(GameModel)
	punter = db.ReferenceProperty(PunterModel)
	homeGoals = db.IntegerProperty()
	awayGoals = db.IntegerProperty()
	score = db.IntegerProperty()

class LeaderBoardModel(db.Model):
	punter = db.ReferenceProperty(PunterModel)
	score = db.IntegerProperty()
	prevPlace = db.IntegerProperty()

class GamesHandler(webapp.RequestHandler):
	
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

class LeaderboardHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('Hello world!')


class BetsHandler(webapp.RequestHandler):
	def get(self):
		punterID = self.request.get('punterID')
		
		punter = db.get(db.Key(punterID))
		bets = punter.betmodel_set
		
		user = users.get_current_user()
		if user:
			loginurl = users.create_logout_url(self.request.uri)
			loginurl_text = "Logout..."
		else:
			loginurl = users.create_login_url(self.request.uri)
			loginurl_text = "Login"
		
		template_stuff = {'user': user,
							'loginurl': loginurl,
							'loginurl_text': loginurl_text,
							#'games': games,
							'isAdmin': users.is_current_user_admin(),
							'punter': punter,
							'bets': bets,
							#'leaderboard': leaderboard,
						}
		path = os.path.join(os.path.dirname(__file__), 'bets.html')
		self.response.out.write(template.render(path, template_stuff))

class ScoreHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		if not users.is_current_user_admin():
			self.redirect('/')
		else:
			q = db.GqlQuery("SELECT __key__ FROM LeaderBoardModel")
			for place in q:
				db.delete(place)
			
			bets = BetModel.all()
			for bet in bets:
				bet.score = 0
				bet.put()
				
			punters = PunterModel.all()
			for punter in punters:
				punter.score = 0
				punter.prevRank = punter.rank
				punter.rank = 0
				punter.put()
			
			games = GameModel.gql("WHERE played = true")
			for game in games:
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
					
					self.response.out.write(punter.displayName)
					self.response.out.write(score)
					
					bet.score = score
					bet.put()
					
					punter.score += score
					punter.put()
					
					self.redirect('/')
					

class BasicDataHandler(webapp.RequestHandler):
	"""docstring for BasicDataHandler"""
	@login_required
	def get(self):
		if not users.is_current_user_admin():
			self.redirect('/')
		else:
			q = db.GqlQuery("SELECT __key__ FROM GameModel")
			for game in q:
				db.delete(game)

			q = db.GqlQuery("SELECT __key__ FROM TeamModel")
			for team in q:
				db.delete(team)

			q = db.GqlQuery("SELECT __key__ FROM PunterModel")
			for punter in q:
				db.delete(punter)

			q = db.GqlQuery("SELECT __key__ FROM BetModel")
			for bet in q:
				db.delete(bet)
				
			teams = ["Algeriet", 
					"Argentina", 
					"Australien", 
					"Brazil",
					"Kamerun",
					"Chile",
					"Elfenbenskusten",
					"Danmark",
					"England",
					"France",
					"Tyskland",
					"Ghana",
					"Grekland",
					"Honduras",
					"Italien",
					"Japan",
					"Nordkorea",
					"Sydkorea",
					"Mexico",
					"Holland",
					"Nya Zeeland",
					"Nigeria",
					"Paraguay",
					"Portugal",
					"Serbien",
					"Slovakien"
					"Slovenien",
					"Sydafrika",
					"Spanien",
					"Schweiz",
					"Uruguay",
					"USA"]
			
			teamlist = {}
			
			for team in teams:
				tmp = TeamModel()
				tmp.displayName = team
				tmp.put()
				teamlist[team] = tmp
			
			gameslist = [("Algeriet","Argentina","2010-06-11 12:30"),
						("Italien", "Nordkorea", "2010-06-12 13:30")]
			
			for game in gameslist:
				home = game[0]
				away = game[1]
				date = game[2]
				game = GameModel()
				game.homeTeam = teamlist[home]
				game.awayTeam = teamlist[away]
				game.gameTime = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
				game.put()
				
			punters = ["Gosta G","Lasse Dahl","Marina S","Thomas Hedstom","Hakan Jarl","Anders Astrom","Peter Tuveland","Johnny Nilsson","Helene Spals","Cecilia B","Mats kjellberg","Henke S","Jerker N","Leif Jonsson","Jonas Karlsson","Janne Jonsson","Andreas Lundstrom","Magnus Loof","Kim W","Hjalmar Wallander","Johan Berg","Andreas Ohrn","Peter Lofgren","Magnus Larsson","Magnus Jansson","Ingemar Gardell","Tommy Lund","Anders Haglund","Nicklas Haglund","Fredrik Jansson","Peter Bentinger","Johan Wallander","Andreas Karstrom"]
			
			for punter in punters:
				tmp = PunterModel()
				tmp.displayName = punter
				tmp.put()
				
			den = teamlist["Algeriet"]
			swe = teamlist["Argentina"]
			bra = teamlist["Brazil"]
			por = teamlist["Australien"]

			game1 = GameModel()
			game1.homeTeam = den.key()
			game1.awayTeam = swe.key()
			game1.played = True
			game1.homeGoals = 1
			game1.awayGoals = 3
			game1.gameTime = datetime.datetime(2010,06,07,12,15)
			game1.put()
			
			game2 = GameModel()
			game2.homeTeam = bra.key()
			game2.awayTeam = por.key()
			game2.played = False
			game2.gameTime = datetime.datetime(2010,06,9,12,15)
			game2.put()
			
			malo = PunterModel()
			malo.displayName = "Magnus Loof"
			malo.put()
			
			bet = BetModel()
			bet.game = game1
			bet.punter = malo.key()
			bet.homeGoals = 1
			bet.awayGoals = 3
			bet.put()
			
			niha = PunterModel()
			niha.displayName = "Nicklas Haglund"
			niha.put()
			
			bet = BetModel()
			bet.game = game1
			bet.punter = niha
			bet.homeGoals = 1
			bet.awayGoals = 2
			bet.put()
			
			self.redirect('/')

class MainHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			loginurl = users.create_logout_url(self.request.uri)
			loginurl_text = "Logout..."
		else:
			loginurl = users.create_login_url(self.request.uri)
			loginurl_text = "Login"
		
		#logging.debug(loginurl)
		games = GameModel.gql('ORDER BY gameTime')
		punters = PunterModel.gql('ORDER by displayName')
		bets = BetModel.all()
		leaderboard = LeaderBoardModel.gql('ORDER BY score')
		
		template_stuff = {'user': user,
							'loginurl': loginurl,
							'loginurl_text': loginurl_text,
							'games': games,
							'isAdmin': users.is_current_user_admin(),
							'punters': punters,
							'bets': bets,
							'leaderboard': leaderboard,
						}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_stuff))

def main():
	application = webapp.WSGIApplication([('/', MainHandler),
	('/leaderboard',LeaderboardHandler),
	('/bets',BetsHandler),
	('/games',GamesHandler),
	('/basicdataload', BasicDataHandler),
	('/calculatescore', ScoreHandler)], debug=True)
	
	logging.getLogger().setLevel(logging.DEBUG)
	
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
