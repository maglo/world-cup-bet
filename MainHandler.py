from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import *
import os

class MainHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			loginurl = users.create_logout_url(self.request.uri)
			loginurl_text = "Logout..."
		else:
			loginurl = users.create_login_url(self.request.uri)
			loginurl_text = "Login or Register"
		
		#logging.debug(loginurl)
		games = GameModel.gql('ORDER BY gameTime')
		punters = PunterModel.gql('ORDER by score DESC')
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
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, template_stuff))
