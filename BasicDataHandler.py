# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import logging
from google.appengine.ext import db
from models import *
import datetime

class BasicDataHandler(webapp.RequestHandler):
	"""docstring for BasicDataHandler"""
	@login_required
	def get(self):
		if not users.is_current_user_admin():
			self.error(401)
		else:
			user = users.get_current_user()
			loginurl = users.create_logout_url(self.request.uri)
			loginurl_text = "Logout..."
							
			op = self.request.get('op')
				
			punters = ["Anders Haglund",
				   "Andreas Pousette",
				   u"Andreas Öhrn",
				   "Christian Axelsson",
				   u"Kristofer Åkerblom",
				   "Erik Lundkvist",
				   "Fredrik Jansson",
				   "Jerker Nordmark",
				   "Johnny Nilsson",
				   "Kim Wellton", 
				   u"Magnus Lööf",
				   "Mattias Andersson",
				   "Oskar Larsson",
				   "Peter Johnsson",
				   u"Peter Löfgren",
				   "Tommy Lund",
				   ]

			gameslist = [("Polen", "Grekland", "Jun 08, 2012 18:00"),
				     ("Ryssland","Tjeckien","Jun 08, 2012 20:45"),
				     ("Holland","Danmark","Jun 09, 2012 18:00"),
				     ("Tyskland","Portugal","Jun 09, 2012 20:45"),
				     ("Spanien","Italien","Jun 10, 2012 18:00"),
				     ("Irland","Kroatien","Jun 10, 2012 20:45"),
				     ("Frankrike","England","Jun 11, 2012 18:00"),
				     ("Ukraina","Sverige","Jun 11, 2012 20:45"),
				     ("Grekland","Tjeckien","Jun 12, 2012 18:00"),
				     ("Polen","Ryssland","Jun 12, 2012 20:45"),
				     ("Danmark","Portugal","Jun 13, 2012 18:00"),
				     ("Holland","Tyskland","Jun 13, 2012 20:45"),
				     ("Italien","Kroatien","Jun 14, 2012 18:00"),
				     ("Spanien","Irland","Jun 14, 2012 20:45"),
				     ("Ukraina","Frankrike","Jun 15, 2012 18:00"),
				     ("Sverige","England","Jun 15, 2012 20:45"),
				     ("Grekland","Ryssland","Jun 16, 2012 20:45"),
				     ("Tjeckien","Polen","Jun 16, 2012 20:45"),
				     ("Portugal","Holland","Jun 17, 2012 20:45"),
				     ("Danmark","Tyskland","Jun 17, 2012 20:45"),
				     ("Spanien","Kroatien","Jun 18, 2012 20:45"),
				     ("Italien","Irland","Jun 18, 2012 20:45"),
				     ("Sverige","Frankrike","Jun 19, 2012 20:45"),
				     ("England","Ukraina","Jun 19, 2012 20:45"), 
				     ]
				
			if op == "games":
				q = db.GqlQuery("SELECT __key__ FROM GameModel")
				for game in q:
					db.delete(game)
				
				teams = TeamModel.all()
				teamlist = {}
				for team in teams:
					teamlist[team.displayName] = team
				
				gamecursor = 0
				for game in gameslist:
					home = game[0]
					away = game[1]
					date = game[2]
					gameobj = GameModel()
					gameobj.homeTeam = teamlist[home]
					gameobj.awayTeam = teamlist[away]
					gameobj.gameTime = datetime.datetime.strptime(date, "%b %d, %Y %H:%M")
					gameobj.ordinal = gamecursor
					gameobj.played = False
					gameobj.scored = False
					gameobj.put()
					gamecursor += 1
				
				self.redirect('/basicdataload')
			
			if op == "teams":
				q = db.GqlQuery("SELECT __key__ FROM TeamModel")
				for team in q:
					db.delete(team)

				teams = ["Danmark",
					 "England",
					 "Frankrike",
					 "Grekland",
					 "Holland",
					 "Irland",
					 "Italien",
					 "Kroatien",
					 "Polen",
					 "Portugal",
					 "Ryssland",
					 "Spanien",
					 "Sverige",
					 "Tjeckien",
					 "Tyskland",
					 "Ukraina",
					]

				for team in teams:
					tmp = TeamModel()
					tmp.displayName = team
					tmp.put()
				
				self.redirect('/basicdataload')
			
			if op == "punters":
				q = db.GqlQuery("SELECT __key__ FROM PunterModel")
				for punter in q:
					db.delete(punter)
				
				#TODO fixa bugg, bets kommer inte in i nummerordning, puntercursor borde persistenshanteras i datastore
				puntercursor = 0
				for punter in punters:
					tmp = PunterModel()
					tmp.displayName = punter
					tmp.ordinal = puntercursor
					tmp.score = 0
					tmp.put()
					puntercursor += 1
				
				self.redirect('/basicdataload')
			if op == "clearbets":
				q = db.GqlQuery("SELECT __key__ FROM BetModel")
				punters = PunterModel.all()
				for bet in q:
					db.delete(bet)
				for punter in punters:
					punter.score = 0
					punter.put()
				
			
			if op == "bets":
#[1,1,1,0,1,1,1,1,0,4,1,2,0,2,0,2,1,2,1,3,2,0,1,1,0,1,1,1,1,1,1,1,2,2,1,1,0,2,0,1,0,2,1,3,1,2,1,2,1,2,0,2,1,2,1,2,1,1,0,1,1,2,1,2,1,2,],					
# en rad per match - bets per punter home-away
				bets =  [[2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					 [2,1,2,2,3,0,4,1,3,1,0,4,4,2,1,3,0,0,2,1,2,3,4,2,2,2,5,0,0,4,3,2,1,1,2,3,3,3,1,4,3,3,2,0,4,3,3,1],
					]
		
				
				q = db.GqlQuery("SELECT * FROM BetCursor")
				
				if q.count() == 0:
					c = BetCursor()
					c.ordinal = 0
					c.put()
				
				gamecursor = q.get()
				logging.debug("gamecursor: " + str(gamecursor.ordinal))
					
				games = GameModel.gql("WHERE ordinal = :ordinal", ordinal=gamecursor.ordinal)
				if not games:
					self.redirect('/')

				punters = PunterModel.gql("ORDER BY ordinal")
				
				for game in games:
					logging.debug("RUNNING GAME")
					betcursor = 0
					ordinalcursor = 0
					for punter in punters:
						bet = BetModel()
						bet.game = game
						bet.punter = punter
						bet.homeGoals = bets[gamecursor.ordinal][betcursor]
						betcursor += 1
						bet.awayGoals = bets[gamecursor.ordinal][betcursor]
						betcursor += 1
						bet.ordinal = ordinalcursor
						ordinalcursor += 1
						bet.put()
				
				gamecursor.ordinal += 1
				gamecursor.put()
					
				
				self.redirect('/basicdataload?' + str(gamecursor.ordinal))

			path = os.path.join(os.path.dirname(__file__), 'templates/basicdata.html')
			template_stuff = {'user': user,
					  'loginurl': loginurl,
					  'loginurl_text': loginurl_text,
					  }
			self.response.out.write(template.render(path, template_stuff))

