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
##    _____________   __________________     ____  ___    __  _______ 
##   / ____/ ____/ | / /_  __/ ____/ __ \   / __ \/   |  /  |/  / __ \
##  / /   / __/ /  |/ / / / / __/ / /_/ /  / /_/ / /| | / /|_/ / /_/ /
## / /___/ /___/ /|  / / / / /___/ _, _/  / _, _/ ___ |/ /  / / ____/ 
## \____/_____/_/ |_/ /_/ /_____/_/ |_|  /_/ |_/_/  |_/_/  /_/_/      
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import scoredisplay
from scoredisplay import AlphaScoreDisplay
#from base import AlphaScoreDisplay

class CenterRampMode(game.Mode):
	def __init__(self, game, priority):
			super(CenterRampMode, self).__init__(game, priority)
			## Global Setting Variables ##
			self.centerRampShotsToLite50k = 3
			self.centerRampShotStartedDelay = 3 #in seconds

			## Global System Variables ##
			self.centerRampShotStarted = False
			self.centerRampShotsMade = 0
			self.enabled50k = False

	def resetCenterRampShotStarted(self):
		self.centerRampShotStarted = False

	def enable50kTarget(self):
		self.enabled50k = True
		self.game.lamps.standupRight50k.enable()

	def disable50kTarget(self):
		self.enabled50k = False
		self.game.lamps.standupRight50k.disable()

	def sw_centerRampEntry_active(self, sw):
		self.cancel_delayed('centerRampShotStarted')
		self.game.coils.ballReleaseShooterLane_CenterRampFlashers1.disable()
		self.game.coils.ballReleaseShooterLane_CenterRampFlashers1.schedule(schedule=0x00000CCC, cycle_seconds=1, now=True)
		self.centerRampShotStarted = True
		self.delay(name='centerRampShotStarted',delay=self.centerRampShotStartedDelay,handler=self.resetCenterRampShotStarted)
		return procgame.game.SwitchContinue

	def sw_centerRampMiddle_active(self, sw):
		if (self.centerRampShotStarted == True):
			self.game.coils.dropReset_CenterRampFlashers2.schedule(schedule=0x0000000F, cycle_seconds=1, now=True)
			self.game.coils.californiaFault_CenterRampFlashers3.schedule(schedule=0x000000F0, cycle_seconds=1, now=True)
			self.game.coils.ejectHole_CenterRampFlashers4.schedule(schedule=0x00000F00, cycle_seconds=1, now=True)
			self.centerRampShotsMade += 1
			if (self.centerRampShotsMade == self.centerRampShotsToLite50k):
				#Enable 50k target
				self.enable50kTarget()
		return procgame.game.SwitchContinue

	def sw_centerRampEnd_active(self, sw):
		return procgame.game.SwitchContinue

	def sw_rightStandup50k_active(self, sw):
		if (self.enable50kTarget == True):
			self.game.utilities.score(50000)
			self.disable50kTarget()
		return procgame.game.SwitchContinue




	