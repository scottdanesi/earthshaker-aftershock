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
##    _____ __  __________  ________________ 
##   / ___// / / / ____/ / /_  __/ ____/ __ \
##   \__ \/ /_/ / __/ / /   / / / __/ / /_/ /
##  ___/ / __  / /___/ /___/ / / /___/ _, _/ 
## /____/_/ /_/_____/_____/_/ /_____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Shelter(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Shelter, self).__init__(game, priority)
			# Settings Variables #
			self.enterSwitch1Triggered = False
			self.enterSwitch2Triggered = False
			
	def mode_started(self):
		pass

	def mode_stopped(self):
		pass

	def ballEnteredShelter(self):
		### Scan for Active Ball Locks ###
		if (self.game.multiball_mode.ballLock1Lit == True):
			self.game.multiball_mode.lockBall1()
		elif (self.game.multiball_mode.ballLock2Lit == True):
			self.game.multiball_mode.lockBall2()
		elif (self.game.multiball_mode.ballLock3Lit == True):
			self.game.multiball_mode.startMultiball()
		else:
			pass

	def sw_underPlayfieldDrop1_active(self, sw):
		self.ballEnteredShelter()
		self.enterSwitch1Triggered = True

	def sw_underPlayfieldDrop2_active(self, sw):
		if self.enterSwitch1Triggered == False:
			self.ballEnteredShelter()
			### Throw Operator Message ###
		self.enterSwitch2Triggered = True

	def sw_ballPopperBottom_closed_for_200ms(self, sw):
		### Check for broken Shelter switches ###
		if (self.enterSwitch1Triggered == False or self.enterSwitch2Triggered == False):
			pass
			### Throw Operator Message ###

		### Handle ball locking if both switches are broken ###
		if (self.enterSwitch1Triggered == False and self.enterSwitch2Triggered == False):
			self.ballEnteredShelter()

		### Reset Switch Monitors ###
		self.enterSwitch1Triggered = False
		self.enterSwitch2Triggered = False

		if(self.game.multiball_mode.multiballStarting == True):
			### Multiball is Starting, let that function handle ball kickouts ###
			return procgame.game.SwitchStop
		else:
			### Multiball is NOT Starting ###
			self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
			self.delay(delay=.2,handler=self.game.sound.play,param='eject')
			self.game.utilities.score(250)
			return procgame.game.SwitchContinue