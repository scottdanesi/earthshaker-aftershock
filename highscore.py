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

			self.aLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','_']
			self.aLettersCount = len(self.aLetters)
			self.currentLetterInt = 0 #Start at A

			self.newPlayerPosition = 0
			self.newPlayerNumber = 0

			self.checkScoreCallback = ''

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

		if self.player1Score == ' ':
			self.player1Score = 0
		if self.player2Score == ' ':
			self.player2Score = 0
		if self.player3Score == ' ':
			self.player3Score = 0
		if self.player4Score == ' ':
			self.player4Score = 0


	def RetrieveScores(self):
		self.retrieveCurrentHighScores()
		self.retrieveCurrentScores()

	def checkPlayer1(self):
		self.newPlayerPosition = 5
		self.newPlayerNumber = 1
		self.checkScoreCallback = self.game.highscore_mode.checkPlayer2
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
			self.enterInitialsStart(self.newPlayerNumber,self.newPlayerPosition)
		else:
			self.checkScoreCallback()

	def checkPlayer2(self):
		self.newPlayerPosition = 5
		self.newPlayerNumber = 2
		self.checkScoreCallback = self.game.highscore_mode.checkPlayer3
		if (self.player2Score > self.highScore4Score):
			self.newPlayerPosition -= 1
		if (self.player2Score > self.highScore3Score):
			self.newPlayerPosition -= 1
		if (self.player2Score > self.highScore2Score):
			self.newPlayerPosition -= 1
		if (self.player2Score > self.highScore1Score):
			self.newPlayerPosition -= 1
		if (self.player2Score > self.grandChampScore):
			self.newPlayerPosition -= 1

		if (self.newPlayerPosition < 5):
			self.enterInitialsStart(self.newPlayerNumber,self.newPlayerPosition)
		else:
			self.checkScoreCallback()

	def checkPlayer3(self):
		self.newPlayerPosition = 5
		self.newPlayerNumber = 3
		self.checkScoreCallback = self.game.highscore_mode.checkPlayer4
		if (self.player3Score > self.highScore4Score):
			self.newPlayerPosition -= 1
		if (self.player3Score > self.highScore3Score):
			self.newPlayerPosition -= 1
		if (self.player3Score > self.highScore2Score):
			self.newPlayerPosition -= 1
		if (self.player3Score > self.highScore1Score):
			self.newPlayerPosition -= 1
		if (self.player3Score > self.grandChampScore):
			self.newPlayerPosition -= 1

		if (self.newPlayerPosition < 5):
			self.enterInitialsStart(self.newPlayerNumber,self.newPlayerPosition)
		else:
			self.checkScoreCallback()

	def checkPlayer4(self):
		self.newPlayerPosition = 5
		self.newPlayerNumber = 4
		self.checkScoreCallback = self.game.highscore_mode.finishHighScores
		if (self.player4Score > self.highScore4Score):
			self.newPlayerPosition -= 1
		if (self.player4Score > self.highScore3Score):
			self.newPlayerPosition -= 1
		if (self.player4Score > self.highScore2Score):
			self.newPlayerPosition -= 1
		if (self.player4Score > self.highScore1Score):
			self.newPlayerPosition -= 1
		if (self.player4Score > self.grandChampScore):
			self.newPlayerPosition -= 1

		if (self.newPlayerPosition < 5):
			self.enterInitialsStart(self.newPlayerNumber,self.newPlayerPosition)
		else:
			self.checkScoreCallback()

	def updateScores(self,score,inits):
		if (self.newPlayerPosition == 5):
			### No New High Score ###
			pass
		elif (self.newPlayerPosition == 4):
			### New High Score 4 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = score
			self.game.game_data['HighScore4']['HighScore4Inits'] = inits
		elif (self.newPlayerPosition == 3):
			### New High Score 3 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = score
			self.game.game_data['HighScore3']['HighScore3Inits'] = inits
		elif (self.newPlayerPosition == 2):
			### New High Score 2 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = self.game.game_data['HighScore2']['HighScore2Score']
			self.game.game_data['HighScore3']['HighScore3Inits'] = self.game.game_data['HighScore2']['HighScore2Inits']
			self.game.game_data['HighScore2']['HighScore2Score'] = score
			self.game.game_data['HighScore2']['HighScore2Inits'] = inits
		elif (self.newPlayerPosition == 1):
			### New High Score 1 ###
			self.game.game_data['HighScore4']['HighScore4Score'] = self.game.game_data['HighScore3']['HighScore3Score']
			self.game.game_data['HighScore4']['HighScore4Inits'] = self.game.game_data['HighScore3']['HighScore3Inits']
			self.game.game_data['HighScore3']['HighScore3Score'] = self.game.game_data['HighScore2']['HighScore2Score']
			self.game.game_data['HighScore3']['HighScore3Inits'] = self.game.game_data['HighScore2']['HighScore2Inits']
			self.game.game_data['HighScore2']['HighScore2Score'] = self.game.game_data['HighScore1']['HighScore1Score']
			self.game.game_data['HighScore2']['HighScore2Inits'] = self.game.game_data['HighScore1']['HighScore1Inits']
			self.game.game_data['HighScore1']['HighScore1Score'] = score
			self.game.game_data['HighScore1']['HighScore1Inits'] = inits
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
			self.game.game_data['GrandChamp']['GrandChampScore'] = score
			self.game.game_data['GrandChamp']['GrandChampInits'] = inits

		else:
			pass


	def enterInitialsStart(self,player_num,new_position):
		self.currentLetterInt = 0 #Start at A
		self.currentPosition = 1
		self.workingInitials = ''

		self.enterInitialsStage1()

	def enterInitialsStage1(self):
		self.currentLetter = self.aLetters[self.currentLetterInt]
		self.game.utilities.displayText(2000,topText='HIGH SCORE',bottomText='PLAYER ' + str(self.newPlayerNumber) + ' ' + self.currentLetter + '__',seconds=0,justify='center')

	def enterInitialsStage2(self):
		self.currentLetter = self.aLetters[self.currentLetterInt]
		self.game.utilities.displayText(2000,topText='HIGH SCORE',bottomText='PLAYER ' + str(self.newPlayerNumber) + ' ' + self.workingInitials + self.currentLetter + '_',seconds=0,justify='center')

	def enterInitialsStage3(self):
		self.currentLetter = self.aLetters[self.currentLetterInt]
		self.game.utilities.displayText(2000,topText='HIGH SCORE',bottomText='PLAYER ' + str(self.newPlayerNumber) + ' ' + self.workingInitials + self.currentLetter,seconds=0,justify='center')

	def setLetter(self):
		if (self.currentPosition == 1):
			self.workingInitials = self.currentLetter
			self.currentPosition = 2
			self.enterInitialsStage2()
		elif (self.currentPosition == 2):
			self.workingInitials = self.workingInitials + self.currentLetter
			self.currentPosition = 3
			self.enterInitialsStage3()
		elif (self.currentPosition == 3):
			self.workingInitials = self.workingInitials + self.currentLetter
			self.updateScores(self.player1Score,self.workingInitials)
			self.checkScoreCallback()

	def sw_startButton_active_for_20ms(self, sw):
		self.setLetter()
		return procgame.game.SwitchStop

	def sw_FlipperLwR_active_for_20ms(self, sw):
		if(self.currentLetterInt < len(self.aLetters) - 1):
			self.currentLetterInt += 1
		else:
			self.currentLetterInt = 0

		if (self.currentPosition == 1):
			self.enterInitialsStage1()
		elif (self.currentPosition == 2):
			self.enterInitialsStage2()
		elif (self.currentPosition == 3):
			self.enterInitialsStage3()

	def sw_FlipperLwL_active_for_20ms(self, sw):
		if(self.currentLetterInt > 0):
			self.currentLetterInt -= 1
		else:
			self.currentLetterInt = len(self.aLetters) - 1

		if (self.currentPosition == 1):
			self.enterInitialsStage1()
		elif (self.currentPosition == 2):
			self.enterInitialsStage2()
		elif (self.currentPosition == 3):
			self.enterInitialsStage3()


	def checkScores(self,callback):
		self.callback = callback

		self.RetrieveScores()
		#### Check Player 1 ####
		self.checkPlayer1()

		
	def showCongrats(self):
		self.game.utilities.displayText(2000,topText='CONGRATULATIONS',bottomText=' ',seconds=0,justify='center')
		self.game.utilities.acCoilPulse(coilname='knocker_RightRampFlashers2',pulsetime=50)

	def finishHighScores(self):
		self.showCongrats()
		self.delay(delay=3,handler=self.callback)
		#self.callback()
		
	