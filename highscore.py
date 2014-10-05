#################################################################################
##     _________    ____  ________  _______ __  _____    __ __ __________  __
##    / ____/   |  / __ \/_  __/ / / / ___// / / /   |  / //_// ____/ __ \/ /
##   / __/ / /| | / /_/ / / / / /_/ /\__ \/ /_/ / /| | / ,<  / __/ / /_/ / / 
##  / /___/ ___ |/ _, _/ / / / __  /___/ / __  / ___ |/ /| |/ /___/ _, _/_/  
## /_____/_/  |_/_/ |_| /_/ /_/ /_//____/_/ /_/_/  |_/_/ |_/_____/_/ |_(_)   
##     ___    ______________________  _____ __  ______  ________ __
##    /   |  / ____/_  __/ ____/ __ \/ ___// / / / __ \/ ____/ //_/
##   / /| | / /_    / / / __/ / /_/ /\__ \/ /_/ / / / / /   / ,<   
##  / ___ |/ __/   / / / /___/ _, _/___/ / __  / /_/ / /___/ /| |  
## /_/  |_/_/     /_/ /_____/_/ |_|/____/_/ /_/\____/\____/_/ |_|                     
##                                                     
## A P-ROC Project by Scott Danesi, Copyright 2013-2014
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
#################################################################################

#################################################################################
##     __  ______________  __   _____ __________  ____  ______
##    / / / /  _/ ____/ / / /  / ___// ____/ __ \/ __ \/ ____/
##   / /_/ // // / __/ /_/ /   \__ \/ /   / / / / /_/ / __/   
##  / __  // // /_/ / __  /   ___/ / /___/ /_/ / _, _/ /___   
## /_/ /_/___/\____/_/ /_/   /____/\____/\____/_/ |_/_____/   
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc

class HighScore(game.Mode):
	def __init__(self, game, priority):
			super(HighScore, self).__init__(game, priority)
			self.CurrentGrandChamp = 0
			self.CurrentHighScore1 = 0
			self.CurrentHighScore2 = 0
			self.CurrentHighScore3 = 0
			self.CurrentHighScore4 = 0
			self.CurrentMileChamp = 0

			self.player1Score = 0
			self.player2Score = 0
			self.player3Score = 0
			self.player4Score = 0

	############################
	#### Standard Functions ####
	############################
	def mode_started(self):
		pass

	def update_lamps(self):
		pass

	def retrieveCurrentHighScores(self):
		for category in self.game.highscore_categories:
			for index, score in enumerate(category.scores):
				name = str(score.inits)

				#### Classic High Score Data ####
				if category.game_data_key == 'ClassicHighScoreData':
					if index == 0:
						#### GRAND CHAMPION ####
						self.CurrentGrandChamp = score
					elif index == 1:
						self.CurrentHighScore1 = score
					elif index == 2:
						self.CurrentHighScore2 = score
					elif index == 3:
						self.CurrentHighScore3 = score
					elif index == 4:
						self.CurrentHighScore4 = score

				#### Mileage Champion ####
				elif category.game_data_key == 'MilesChampion':
					if index == 0:
						#### MILEAGE CHAMP ####
						self.CurrentMileChamp = score

	def retrieveCurrentScores(self):
		self.player1Score = self.game.game_data['LastGameScores']['LastPlayer1Score']
		self.player2Score = self.game.game_data['LastGameScores']['LastPlayer2Score']
		self.player3Score = self.game.game_data['LastGameScores']['LastPlayer3Score']
		self.player4Score = self.game.game_data['LastGameScores']['LastPlayer4Score']

	def checkScores(self,callback):
		pass
	