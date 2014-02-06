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
			self.centerRamp2MilesTimer = 8 #in Seconds

			## Global System Variables ##
			self.centerRampShotStarted = False
			self.enabled50k = False
			self.enabled2Miles = False

	def update_lamps(self):
		### 2 Miles Lamp ###
		if (self.enabled2Miles == True):
			self.game.lamps.centerRamp2Miles.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
		else:
			self.game.lamps.centerRamp2Miles.disable()

		### 50k Target Lamp ###
		if (self.enabled50k == True):
			self.game.lamps.standupRight50k.enable()
		else:
			self.game.lamps.standupRight50k.disable()

		### Miles Update ###
		self.disableMilesLamps()
		self.tempMiles = self.game.utilities.get_player_stats('miles')
		if (self.tempMiles >= 30):
			self.game.lamps.miles30.enable()
			self.tempMiles -= 30
		if (self.tempMiles >= 20):
			self.game.lamps.miles20.enable()
			self.tempMiles -= 20
		if (self.tempMiles >= 10):
			self.game.lamps.miles10.enable()
			self.tempMiles -= 10
		if (self.tempMiles >= 5):
			self.game.lamps.miles5.enable()
			self.tempMiles -= 5
		if (self.tempMiles >= 4):
			self.game.lamps.miles4.enable()
			self.tempMiles -= 4
		if (self.tempMiles >= 3):
			self.game.lamps.miles3.enable()
			self.tempMiles -= 3
		if (self.tempMiles >= 2):
			self.game.lamps.miles2.enable()
			self.tempMiles -= 2
		if (self.tempMiles >= 1):
			self.game.lamps.miles1.enable()
			self.tempMiles -= 1

	def disableMilesLamps(self):
		self.game.lamps.miles30.disable()
		self.game.lamps.miles20.disable()
		self.game.lamps.miles10.disable()
		self.game.lamps.miles5.disable()
		self.game.lamps.miles4.disable()
		self.game.lamps.miles3.disable()
		self.game.lamps.miles2.disable()
		self.game.lamps.miles1.disable()

	def resetCenterRampShotStarted(self):
		self.centerRampShotStarted = False

	def reset2MilesAward(self):
		self.enabled2Miles = False
		self.update_lamps()

	def centerRampShotCompleted(self):
		self.centerRampShotStarted = False
		self.game.coils.californiaFault_CenterRampFlashers3.schedule(schedule=0x0000000F, cycle_seconds=1, now=True)
		self.game.coils.ejectHole_CenterRampFlashers4.schedule(schedule=0x000000F0, cycle_seconds=1, now=True)
		# Sound FX #
		self.game.sound.play('centerRampComplete')
		# Score it! #
		self.game.utilities.score(1000)
		# Award Miles #
		if (self.enabled2Miles == True):
			self.game.utilities.set_player_stats('miles',self.game.utilities.get_player_stats('miles') + 2)
		else:
			self.game.utilities.set_player_stats('miles',self.game.utilities.get_player_stats('miles') + 1)

		self.cancel_delayed('reset2MilesAward')
		self.enabled2Miles = True
		self.delay(name='reset2MilesAward',delay=self.centerRamp2MilesTimer,handler=self.reset2MilesAward)
		self.game.utilities.set_player_stats('center_shots',self.game.utilities.get_player_stats('center_shots') + 1)
		if (self.game.utilities.get_player_stats('center_shots') == self.centerRampShotsToLite50k):
			self.enable50kTarget()
		self.update_lamps()

	def enable50kTarget(self):
		self.enabled50k = True

	def disable50kTarget(self):
		self.enabled50k = False

	def sw_centerRampEntry_active(self, sw):
		self.cancel_delayed('centerRampShotStarted')
		self.game.coils.ballReleaseShooterLane_CenterRampFlashers1.disable()
		self.game.coils.ballReleaseShooterLane_CenterRampFlashers1.schedule(schedule=0x00000CCC, cycle_seconds=1, now=True)
		self.game.coils.dropReset_CenterRampFlashers2.schedule(schedule=0x0000F000, cycle_seconds=1, now=True)
		# Sound FX #
		self.game.sound.play('centerRampEnter')
		self.centerRampShotStarted = True
		self.delay(name='centerRampShotStarted',delay=self.centerRampShotStartedDelay,handler=self.resetCenterRampShotStarted)
		return procgame.game.SwitchContinue

	def sw_centerRampMiddle_active(self, sw):
		if (self.centerRampShotStarted == True):
			self.centerRampShotCompleted()
		return procgame.game.SwitchContinue

	def sw_centerRampEnd_active(self, sw):
		#in case the ball skips one of the ramp switches
		#if (self.centerRampShotStarted == True):
			#self.centerRampShotCompleted()
		return procgame.game.SwitchContinue

	def sw_rightStandup50k_active(self, sw):
		if (self.enabled50k == True):
			self.game.utilities.score(50000)
			self.game.coils.outholeKicker_CaptiveFlashers.schedule(schedule=0x0000000F, cycle_seconds=1, now=True)
			self.disable50kTarget()
			self.update_lamps()
		return procgame.game.SwitchContinue




	