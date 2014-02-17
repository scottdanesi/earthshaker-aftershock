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
##    _____ ____  _____   ___   ____________ 
##   / ___// __ \/  _/ | / / | / / ____/ __ \
##   \__ \/ /_/ // //  |/ /  |/ / __/ / /_/ /
##  ___/ / ____// // /|  / /|  / /___/ _, _/ 
## /____/_/   /___/_/ |_/_/ |_/_____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Spinner(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Spinner, self).__init__(game, priority)
			self.superSpinnerSpins = self.game.user_settings['Feature']['Super Spinner Spins']
			self.superSpinnerTime = self.game.user_settings['Feature']['Super Spinner Time']
			self.superSpinnerLit = False
			self.superSpinnerEnabled = False
			
	def mode_started(self):
		self.totalSpinnerCount = 0
		self.qualifyingSpinnerCount = 0

	def mode_stopped(self):
		self.cancel_delayed('superSpinnerReset')
		self.resetSuperSpinner()

	def update_lamps(self):
		# Super Spinner Lit #
		if (self.superSpinnerLit == True):
			self.game.lamps.inlaneRightSpinner.enable()
		else:
			self.game.lamps.inlaneRightSpinner.disable()

		# Super Spinner Enabled #
		if (self.superSpinnerEnabled == True):
			self.game.lamps.spinner.enable()
		else:
			self.game.lamps.spinner.disable()

	def superSpinnerCheck(self):
		if (self.qualifyingSpinnerCount >= self.superSpinnerSpins and self.superSpinnerLit == False and self.superSpinnerEnabled == False):
			self.superSpinnerLit = True
			self.update_lamps()

	def scoreSpinner(self):
		if self.superSpinnerEnabled == True:
			self.game.utilities.score(3000)
		else:
			self.game.utilities.score(300)

	def resetSuperSpinner(self):
		self.superSpinnerEnabled = False
		self.superSpinnerLit = False
		self.qualifyingSpinnerCount = 0
		self.update_lamps()

	def sw_spinner_active(self, sw):
		if self.superSpinnerEnabled == True:
			self.game.utilities.score(3000)
			self.game.utilities.acFlashPulse(coilname='dropReset_CenterRampFlashers2',pulsetime=40)
			self.game.sound.play('super_spinner')
		else:
			self.game.utilities.score(300)
			self.game.lamps.spinner.pulse(50)
			self.game.sound.play('spinner')
			self.superSpinnerCheck()
		self.totalSpinnerCount += 1
		self.qualifyingSpinnerCount += 1
		return procgame.game.SwitchStop

	def sw_rightOutsideReturn_active(self, sw):
		if (self.superSpinnerLit == True):
			self.superSpinnerEnabled = True
			self.superSpinnerLit = False
			if (self.superSpinnerTime <> -1):
				self.delay(name='superSpinnerReset',delay=self.superSpinnerTime,handler=self.resetSuperSpinner)
			self.update_lamps()
			self.game.sound.play('super_spinner_lit')
		else:
			self.game.sound.play('zone_na')


