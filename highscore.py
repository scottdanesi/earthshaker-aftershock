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
		self.grandChampScore = self.game.game_data['GrandChamp']['GrandChampScore']
		self.grandChampInits = self.game.game_data['GrandChamp']['GrandChampInits']

		self.highScore1Score = self.game.game_data['HighScore1']['HighScore1Score']
		self.highScore1Inits = self.game.game_data['HighScore1']['HighScore1Inits']

		self.highScore2Score = self.game.game_data['HighScore2']['HighScore2Score']
		self.highScore2Inits = self.game.game_data['HighScore2']['HighScore2Inits']

		self.highScore3Score = self.game.game_data['HighScore3']['HighScore3Score']
		self.highScore3Inits = self.game.game_data['HighScore3']['HighScore3Inits']

		self.highScore4Score = self.game.game_data['HighScore4']['HighScore4Score']
		self.highScore4Inits = self.game.game_data['HighScore4']['HighScore4Inits']

		self.milesChampMiles = self.game.game_data['MilesChamp']['MilesChampMiles']
		self.milesChampInits = self.game.game_data['MilesChamp']['MilesChampInits']

	def retrieveCurrentScores(self):
		self.player1Score = self.game.game_data['LastGameScores']['LastPlayer1Score']
		self.player2Score = self.game.game_data['LastGameScores']['LastPlayer2Score']
		self.player3Score = self.game.game_data['LastGameScores']['LastPlayer3Score']
		self.player4Score = self.game.game_data['LastGameScores']['LastPlayer4Score']

	def RetrieveScores(self):
		self.retrieveCurrentHighScores()
		self.retrieveCurrentScores()

	def checkPlayer1(self):
		self.newPlayerPosition = 5
		if (self.player1Score > self.highScore4Score):
			self.newPlayerPosition -= 1
		if (self.player1Score > self.highScore3Score):
			self.newPlayerPosition -= 1
		if (self.player1Score > self.highScore2Score):
			self.newPlayerPosition -= 1
		if (self.player1Score > self.highScore1Score):
			self.newPlayerPosition -= 1
		if (self.player1Score > self.grandChampScore):
			self.newPlayerPosition -= 1

		if (self.newPlayerPosition < 5):
			
			self.enterInitialsStart(1,self.newPlayerPosition)

	def updateScores(self,score,inits):
		if (self.newPlayerPosition == 5):
			### No New High Score ###
			pass
		elif (self.newPlayerPosition == 4):
			### New High Score 4 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.player1Score
			self.game.game_data['HighScore4']['HighScore4Inits'] = 'ABC'
		elif (self.newPlayerPosition == 3):
			### New High Score 3 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = self.player1Score
			self.game.game_data['HighScore3']['HighScore3Inits'] = 'ABC'
		elif (self.newPlayerPosition == 2):
			### New High Score 2 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = self.game.game_data['HighScore2']['HighScore2Score']
			self.game.game_data['HighScore3']['HighScore3Inits'] = self.game.game_data['HighScore2']['HighScore2Inits']
			self.game.game_data['HighScore2']['HighScore2Score'] = self.player1Score
			self.game.game_data['HighScore2']['HighScore2Inits'] = 'ABC'
		elif (self.newPlayerPosition == 1):
			### New High Score 1 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = self.game.game_data['HighScore2']['HighScore2Score']
			self.game.game_data['HighScore3']['HighScore3Inits'] = self.game.game_data['HighScore2']['HighScore2Inits']
			self.game.game_data['HighScore2']['HighScore2Score'] = self.game.game_data['HighScore1']['HighScore1Score']
			self.game.game_data['HighScore2']['HighScore2Inits'] = self.game.game_data['HighScore1']['HighScore1Inits']
			self.game.game_data['HighScore1']['HighScore1Score'] = self.player1Score
			self.game.game_data['HighScore1']['HighScore1Inits'] = 'ABC'
		elif (self.newPlayerPosition == 0):
			### New Grand Champ ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = self.game.game_data['HighScore2']['HighScore2Score']
			self.game.game_data['HighScore3']['HighScore3Inits'] = self.game.game_data['HighScore2']['HighScore2Inits']
			self.game.game_data['HighScore2']['HighScore2Score'] = self.game.game_data['HighScore1']['HighScore1Score']
			self.game.game_data['HighScore2']['HighScore2Inits'] = self.game.game_data['HighScore1']['HighScore1Inits']
			self.game.game_data['HighScore1']['HighScore1Score'] = self.game.game_data['GrandChamp']['GrandChampScore']
			self.game.game_data['HighScore1']['HighScore1Inits'] = self.game.game_data['GrandChamp']['GrandChampInits']
			self.game.game_data['GrandChamp']['GrandChampScore'] = self.player1Score
			self.game.game_data['GrandChamp']['GrandChampInits'] = 'ABC'

		else:
			pass


	def enterInitialsStart(self,player_num,new_position):
		self.aLetters = ['A','B','C','D']
		#self.currentLetter = self.aLetters[1]
		self.currentPosition = 1
		self.workingInitials = ''

		self.enterInitialsStage1(player_num,new_position)

	def enterInitialsStage1(self,player_num,new_position):
		self.currentLetter = self.aLetters[1]
		self.game.utilities.displayText(2000,topText='HIGH SCORE',bottomText='PLAYER ' + str(player_num) + self.currentLetter + '__',seconds=0,justify='center')

	def enterInitialsStage2(self,player_num,new_position):
		self.game.utilities.displayText(2000,topText='HIGH SCORE',bottomText='PLAYER ' + str(player_num) + self.workingInitials + self.currentLetter + '_',seconds=0,justify='center')

	def enterInitialsStage3(self,player_num,new_position):
		self.game.utilities.displayText(2000,topText='HIGH SCORE',bottomText='PLAYER ' + str(player_num) + self.workingInitials + self.currentLetter,seconds=0,justify='center')

	def setLetter(self):
		if (self.currentPosition == 1):
			self.workingInitials = self.aLetters[self.currentLetter]
			self.currentPosition = 2
			self.enterenterInitialsStage2()
		elif (self.currentPosition == 2):
			self.workingInitials = self.workingInitials + self.aLetters[self.currentLetter]
			self.currentPosition = 3
			self.enterenterInitialsStage2()
		elif (self.currentPosition == 3):
			self.workingInitials = self.workingInitials + self.aLetters[self.currentLetter]

	def displayCongrats(self):
		pass

	def sw_startButton_active_for_20ms(self, sw):
		self.setLetter()
		return procgame.game.SwitchStop


	def checkScores(self,callback):
		self.callback = callback

		self.RetrieveScores()
		#### Check Player 1 ####
		self.checkPlayer1()

		

	def finishHighScores(self):
		self.callback()
		
	