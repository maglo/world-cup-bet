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
				
			punters = ["Gosta G",
				   "Lasse Dahl",
				   "Marina S",
				   "Thomas Hedstom",
				   "Hakan Jarl",
				   "Anders Astrom",
				   "Peter Tuveland",
				   "Johnny Nilsson",
				   "Helene Spals",
				   "Cecilia B",
				   "Mats kjellberg",
				   "Henke S",
				   "Jerker N",
				   "Leif Jonsson",
				   "Jonas Karlsson",
				   "Janne Jonsson",
				   "Andreas Lundstrom",
				   "Magnus Loof",
				   "Kim W",
				   "Hjalmar Wallander",
				   "Johan Berg",
				   "Andreas Ohrn",
				   "Peter Lofgren",
				   "Magnus Larsson",
				   "Magnus Jansson",
				   "Ingemar Gardell",
				   "Tommy Lund",
				   "Anders Haglund",
				   "Nicklas Haglund",
				   "Fredrik Jansson",
				   "Peter Bentinger",
				   "Johan Wallander",
				   "Andreas Karstrom",
				   ]

			gameslist = [("South Africa","Mexico","Jun 11, 2010 13:30"),
				     ("Uruguay","France","Jun 12, 2010 16:00"),
				     ("Argentina","Nigeria","Jun 12, 2010 13:30"),
				     ("Korea Republic","Greece","Jun 12, 2010 20:30"),
				     ("England","USA","Jun 13, 2010 16:00"),
				     ("Algeria","Slovenia","Jun 13, 2010 20:30"),
				     ("Germany","Australia","Jun 14, 2010 16:00"),
				     ("Serbia","Ghana","Jun 13, 2010 13:30"),
				     ("Netherlands","Denmark","Jun 14, 2010 20:30"),
				     ("Japan","Cameroon","Jun 14, 2010 13:30"),
				     ("Italy","Paraguay","Jun 15, 2010 16:00"),
				     ("New Zealand","Slovakia","Jun 15, 2010 20:30"),
				     ("Cote d'Ivoire","Portugal","Jun 15, 2010 13:30"),
				     ("Brazil","Korea DPR","Jun 16, 2010 16:00"),
				     ("Honduras","Chile","Jun 16, 2010 20:30"),
				     ("Spain","Switzerland","Jun 16, 2010 13:30"),
				     ("South Africa","Uruguay","Jun 17, 2010 16:00"),
				     ("France","Mexico","Jun 18, 2010 16:00"),
				     ("Greece","Nigeria","Jun 17, 2010 13:30"),
				     ("Argentina","Korea Republic","Jun 17, 2010 20:30"),
				     ("Germany","Serbia","Jun 18, 2010 20:30"),
				     ("Slovenia","USA","Jun 18, 2010 13:30"),
				     ("England","Algeria","Jun 19, 2010 16:00"),
				     ("Ghana","Australia","Jun 19, 2010 13:30"),
				     ("Netherlands","Japan","Jun 19, 2010 20:30"),
				     ("Cameroon","Denmark","Jun 20, 2010 16:00"),
				     ("Slovakia","Paraguay","Jun 20, 2010 20:30"),
				     ("Italy","New Zealand","Jun 20, 2010 13:30"),
				     ("Brazil","Cote d'Ivoire","Jun 21, 2010 16:00"),
				     ("Portugal","Korea DPR","Jun 21, 2010 20:30"),
				     ("Chile","Switzerland","Jun 21, 2010 13:30"),
				     ("Spain","Honduras","Jun 22, 2010 16:00"),
				     ("Mexico","Uruguay","Jun 22, 2010 13:30"),
				     ("France","South Africa","Jun 22, 2010 13:30"),
				     ("Nigeria","Korea Republic","Jun 23, 2010 16:00"),
				     ("Greece","Argentina","Jun 23, 2010 16:00"),
				     ("Slovenia","England","Jun 23, 2010 13:30"),
				     ("USA","Algeria","Jun 23, 2010 13:30"),
				     ("Ghana","Germany","Jun 24, 2010 16:00"),
				     ("Australia","Serbia","Jun 24, 2010 16:00"),
				     ("Slovakia","Italy","Jun 25, 2010 16:00"),
				     ("Paraguay","New Zealand","Jun 25, 2010 16:00"),
				     ("Denmark","Japan","Jun 24, 2010 13:30"),
				     ("Cameroon","Netherlands","Jun 24, 2010 13:30"),
				     ("Portugal","Brazil","Jun 25, 2010 13:30"),
				     ("Korea DPR","Cote d'Ivoire","Jun 25, 2010 13:30"),
				     ("Chile","Spain","Jun 26, 2010 16:00"),
				     ("Switzerland","Honduras","Jun 26, 2010 16:00"),
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

				teams = ["Algeria", 
						"Argentina", 
						"Australia", 
						"Brazil",
						"Cameroon",
						"Chile",
						"Cote d'Ivoire",
						"Denmark",
						"England",
						"France",
						"Germany",
						"Ghana",
						"Greece",
						"Honduras",
						"Italy",
						"Japan",
						"Korea DPR",
						"Korea Republic",
						"Mexico",
						"Netherlands",
						"New Zealand",
						"Nigeria",
						"Paraguay",
						"Portugal",
						"Serbia",
						"Spain",
						"Slovakia",
						"Slovenia",
						"South Africa",
						"Switzerland",
						"Uruguay",
						"USA"]

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
					
				bets =  [[1,1,1,0,1,1,1,1,0,4,1,2,0,2,0,2,1,2,1,3,2,0,1,1,0,1,1,1,1,1,1,1,2,2,1,1,0,2,0,1,0,2,1,3,1,2,1,2,1,2,0,2,1,2,1,2,1,1,0,1,1,2,1,2,1,2,],
						[3,0,4,0,3,1,4,0,5,0,2,0,3,1,4,0,2,0,3,0,3,1,2,0,2,0,5,0,4,0,2,0,3,0,2,0,4,1,1,0,2,0,4,1,4,0,3,0,2,0,1,0,3,0,4,0,6,0,4,0,5,0,4,0,3,0,],
						[1,2,0,0,1,1,1,2,0,0,0,1,1,1,1,2,1,1,1,1,1,1,0,2,0,0,1,2,0,2,0,1,1,2,0,1,1,2,0,0,1,1,0,2,1,1,1,1,0,0,1,1,1,2,0,1,1,2,0,1,0,2,2,0,2,2,],
						[2,1,2,0,2,1,3,0,3,1,3,1,3,0,3,1,3,0,2,1,2,1,3,0,3,0,2,0,2,0,3,0,2,1,3,1,2,0,1,0,3,1,3,0,2,0,2,1,1,0,3,0,2,0,3,1,3,1,2,1,3,1,1,0,3,0,],
						[1,1,1,0,1,1,1,1,2,1,1,0,1,1,1,1,1,0,2,0,1,1,1,1,0,1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,2,1,0,1,1,0,1,1,1,1,0,1,2,2,0,2,0,1,0,1,1,1,1,0,1,1,],
						[2,1,2,1,3,1,1,1,3,1,0,1,1,0,1,0,1,1,4,2,1,2,1,1,0,1,1,1,1,1,0,0,1,2,0,1,2,2,1,0,1,1,1,0,1,1,0,1,0,1,1,1,1,2,1,1,1,1,2,0,2,1,2,1,2,2,],
						[0,2,0,2,1,0,1,2,1,2,0,1,0,1,1,2,0,2,2,2,5,0,0,1,0,1,0,1,0,2,0,1,0,1,0,2,1,2,0,0,1,2,0,2,0,0,0,2,0,1,2,1,0,3,1,1,0,2,0,2,0,1,0,1,1,3,],
						[4,1,2,0,2,0,2,0,3,1,2,0,1,0,3,0,1,1,3,1,4,0,1,0,2,1,2,1,2,1,3,1,3,2,2,1,5,0,0,0,2,0,3,0,2,0,3,1,2,0,2,1,2,0,3,1,2,1,3,0,4,0,2,0,3,1,],
						[2,0,1,1,2,1,1,1,3,0,2,0,3,0,2,1,3,1,4,1,3,1,1,1,2,0,1,1,3,0,2,1,3,1,3,1,4,1,1,0,2,1,3,1,3,1,1,0,2,0,3,1,3,1,4,1,3,1,2,1,2,1,3,1,3,1,],
						[1,2,1,2,1,0,1,3,1,2,0,0,0,1,1,1,0,1,2,1,2,1,1,2,0,1,1,2,1,2,0,1,1,2,1,2,2,2,0,0,0,3,1,2,0,1,1,1,0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,2,1,1,],
						[3,0,3,0,2,0,2,0,3,1,1,0,1,0,1,0,2,0,1,1,1,1,1,0,1,0,3,0,2,0,2,0,3,0,2,1,2,0,1,0,3,0,5,0,2,0,0,1,1,1,2,0,2,0,2,0,2,1,5,1,3,1,2,0,3,1,],
						[1,2,1,1,0,1,1,1,3,1,1,0,1,1,1,2,0,1,3,2,0,0,2,0,0,0,1,0,1,0,1,1,1,1,1,1,1,2,0,0,2,1,2,0,1,1,2,0,1,1,0,0,1,2,2,0,1,0,2,1,1,1,1,0,2,0,],
						[4,1,3,0,5,1,2,0,3,0,1,0,2,1,2,0,3,1,4,0,2,0,2,1,3,0,2,0,2,0,3,0,2,1,2,0,2,0,0,0,3,1,3,0,2,0,2,1,1,1,2,0,1,0,3,2,2,1,3,1,4,1,2,0,4,0,],
						[1,2,1,2,2,3,0,2,3,1,1,1,1,1,1,1,0,2,2,3,1,3,1,2,0,2,1,1,1,1,1,2,0,3,1,0,1,1,0,0,1,2,2,1,1,0,1,1,1,0,0,1,1,2,0,2,0,0,1,1,2,2,2,1,2,1,],
						[1,2,0,0,2,2,1,2,1,1,0,0,0,1,1,0,0,2,1,1,2,1,0,0,0,1,0,1,1,0,1,1,3,1,0,0,0,2,0,0,1,1,0,2,0,0,2,2,1,2,1,2,2,2,1,1,0,1,0,1,0,2,1,3,1,1,],
						[2,1,2,1,2,1,2,0,3,2,2,0,2,0,2,0,2,0,3,1,1,1,3,0,1,0,2,0,2,1,2,0,3,0,1,0,2,0,1,0,2,1,3,0,2,0,2,0,1,0,2,0,2,1,3,0,3,0,1,0,4,0,4,1,2,0,],
						[1,1,3,1,3,2,2,0,2,0,2,0,4,0,3,0,4,0,2,0,3,0,1,2,1,0,2,1,2,1,1,1,2,2,3,0,3,0,1,0,3,0,3,0,3,1,2,1,3,0,3,0,2,0,2,2,2,1,2,1,5,1,3,0,3,2,],
						[3,0,2,0,2,1,3,1,2,0,2,0,2,0,3,0,3,0,3,0,1,1,3,0,1,0,3,1,2,0,2,0,4,1,2,0,3,1,1,0,3,0,1,1,3,0,1,2,2,1,2,1,1,0,4,0,4,1,2,0,3,1,2,0,3,1,],
						[1,2,1,1,0,1,1,1,1,2,0,0,0,1,1,1,0,1,1,1,1,4,2,1,1,0,0,0,1,1,1,1,0,0,2,1,1,1,0,0,2,1,1,1,2,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,3,1,2,1,1,2,],
						[3,0,2,1,2,0,3,0,3,0,2,0,2,1,4,1,2,0,4,0,1,2,4,0,2,1,3,0,1,0,3,0,3,1,3,2,2,1,1,0,2,2,4,0,2,0,3,0,2,0,1,0,2,0,3,0,1,0,4,0,2,0,3,1,3,1,],
						[1,1,0,0,1,2,1,1,1,1,1,0,1,1,1,2,1,1,2,2,1,1,0,1,0,0,1,0,1,2,1,1,2,2,2,1,1,0,0,0,2,1,1,2,1,1,1,1,1,2,1,1,2,2,1,1,1,1,1,1,0,1,1,1,1,1,],
						[1,1,3,1,3,2,2,2,2,2,1,0,2,1,1,1,1,1,3,1,2,0,1,2,0,1,2,1,1,1,1,0,3,2,1,2,2,0,0,0,2,2,2,0,1,1,1,2,1,0,2,1,1,0,3,0,2,1,2,1,1,0,2,1,2,1,],
						[2,1,2,1,2,1,2,0,2,1,0,0,1,2,1,0,2,0,1,1,3,0,0,2,1,1,1,1,2,0,1,1,1,2,0,1,1,0,0,0,3,0,1,0,1,1,1,1,1,1,0,2,1,2,1,0,1,2,3,2,2,0,2,1,2,0,],
						[0,3,0,2,0,2,1,2,1,2,0,2,0,2,0,2,0,3,0,4,2,1,1,3,0,2,1,2,0,2,0,3,1,4,0,2,1,3,0,1,2,2,0,3,1,2,0,4,0,2,0,3,0,3,1,3,1,3,0,4,0,2,0,2,0,3,],
						[0,3,1,1,0,1,0,2,1,3,0,2,0,1,1,2,0,2,2,1,1,2,0,0,1,2,1,1,0,2,0,2,0,1,1,1,1,2,0,1,1,2,0,4,1,1,2,1,1,2,1,1,1,2,0,2,0,1,1,3,0,2,1,3,1,2,],
						[2,1,3,1,1,0,3,1,2,1,1,0,1,0,2,1,1,0,2,1,1,1,3,0,1,0,2,0,2,0,2,0,1,0,2,1,2,0,0,0,2,0,3,0,2,2,1,0,2,0,2,2,1,0,1,0,1,1,1,0,0,1,2,1,1,1,],
						[0,2,1,2,1,3,1,5,1,3,0,2,1,2,1,3,0,5,1,4,0,3,1,2,0,1,0,2,1,2,0,3,1,2,0,3,1,3,0,0,1,1,0,3,1,3,1,3,0,3,1,3,1,2,0,4,0,2,0,2,1,3,1,3,1,4,],
						[1,1,0,2,1,3,1,2,0,2,0,1,1,1,0,2,0,1,1,3,2,1,0,2,0,0,1,1,0,0,0,2,1,2,1,1,0,1,0,0,1,0,1,2,1,1,1,2,2,1,0,1,0,0,0,0,1,1,0,0,1,1,2,1,0,1,],
						[1,3,1,1,0,2,0,2,2,3,1,2,1,2,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,2,1,0,1,0,2,0,1,0,2,0,2,1,2,1,1,1,2,1,2,0,1,1,2,1,1,0,1,0,2,1,2,1,2,],
						[2,2,3,2,1,1,2,1,2,1,0,0,1,0,1,0,2,0,1,2,1,1,0,0,2,0,1,0,2,0,1,0,2,0,2,0,2,0,0,0,2,2,2,0,2,0,2,1,2,0,1,0,2,0,2,1,2,1,2,1,4,0,2,1,3,0,],
						[1,0,3,1,2,1,2,0,2,1,1,1,1,1,2,1,2,1,2,2,1,2,1,1,1,0,1,1,1,0,1,0,2,2,1,1,1,1,0,0,2,0,0,1,0,0,1,0,1,1,2,2,1,0,2,2,0,1,0,0,2,2,2,1,2,0,],
						[1,3,2,3,2,5,0,2,1,2,0,2,1,2,1,3,0,2,0,1,1,1,2,2,1,2,0,3,1,3,1,3,1,3,1,3,0,2,0,1,2,2,0,2,2,1,2,2,1,2,0,2,1,3,1,3,0,2,0,2,1,1,1,0,2,1,],
						[1,1,1,2,2,1,2,2,2,2,1,2,1,2,1,2,2,2,3,2,2,4,1,1,1,1,2,2,2,2,1,2,1,1,1,1,2,2,0,0,3,2,2,2,1,2,2,3,1,3,1,1,2,2,1,2,1,2,1,1,1,2,1,3,1,3,],
						[1,2,0,2,1,1,1,2,1,2,0,0,2,1,1,1,0,0,3,3,1,0,1,2,0,1,0,2,0,3,0,3,0,3,1,1,0,1,0,0,1,1,1,0,0,2,1,2,2,0,0,1,1,3,0,3,0,2,1,2,0,1,1,2,1,3,],
						[1,3,0,1,2,3,0,3,1,3,0,1,1,2,1,2,0,2,2,4,1,2,1,1,0,2,1,3,0,1,0,2,1,4,1,3,1,2,0,0,1,2,0,2,1,2,0,2,1,3,1,2,2,2,1,2,1,3,1,3,1,2,1,2,0,2,],
						[2,1,1,1,2,1,1,0,3,1,0,0,0,1,3,0,1,1,1,2,2,1,2,1,0,0,1,0,1,0,2,1,1,2,0,0,1,1,0,0,1,2,3,0,0,0,2,1,3,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,]]
		
				
				q = db.GqlQuery("SELECT * FROM BetCursor")
				
				if q.count() == 0:
					c = BetCursor()
					c.ordinal = 12
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
						bet.homeGoals = bets[gamecursor.ordinal - 12][betcursor]
						betcursor += 1
						bet.awayGoals = bets[gamecursor.ordinal - 12][betcursor]
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

