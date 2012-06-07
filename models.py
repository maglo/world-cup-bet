from google.appengine.ext import db

class BetCursor(db.Model):
	ordinal = db.IntegerProperty()

class TournamentModel(db.Model):
	displayName = db.StringProperty()
	betsAreOffDate = db.DateTimeProperty()
	openingDate = db.DateTimeProperty()
	description = db.StringProperty()
	logo = db.StringProperty()
	
class TeamModel(db.Model):
	tournament = db.ReferenceProperty(TournamentModel)
	displayName = db.StringProperty()
	logo = db.StringProperty()

class GameModel(db.Model):
	homeTeam = db.ReferenceProperty(TeamModel, collection_name="homeTeam")
	awayTeam = db.ReferenceProperty(TeamModel, collection_name="awayTeam")
	played = db.BooleanProperty()
	scored = db.BooleanProperty()
	homeGoals = db.IntegerProperty()
	awayGoals = db.IntegerProperty()
	gameTime = db.DateTimeProperty()
	ordinal = db.IntegerProperty()

class PunterModel(db.Model):
	user = db.UserProperty()
	displayName = db.StringProperty()
	score = db.IntegerProperty(0)
	rank = db.IntegerProperty()
	prevRank = db.IntegerProperty()
	ordinal = db.IntegerProperty()

class BetModel(db.Model):
	game = db.ReferenceProperty(GameModel)
	punter = db.ReferenceProperty(PunterModel)
	homeGoals = db.IntegerProperty()
	awayGoals = db.IntegerProperty()
	score = db.IntegerProperty()
	ordinal = db.IntegerProperty()

class LeaderBoardModel(db.Model):
	punter = db.ReferenceProperty(PunterModel)
	score = db.IntegerProperty()
	prevPlace = db.IntegerProperty()
