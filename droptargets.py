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
##     ____  ____  ____  ____     _________    ____  _______________________
##    / __ \/ __ \/ __ \/ __ \   /_  __/   |  / __ \/ ____/ ____/_  __/ ___/
##   / / / / /_/ / / / / /_/ /    / / / /| | / /_/ / / __/ __/   / /  \__ \ 
##  / /_/ / _, _/ /_/ / ____/    / / / ___ |/ _, _/ /_/ / /___  / /  ___/ / 
## /_____/_/ |_|\____/_/        /_/ /_/  |_/_/ |_|\____/_____/ /_/  /____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class DropTargets(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(DropTargets, self).__init__(game, priority)
			self.dropTargetHurryUpEnabled = False

			#### Load Mode Feature Defaults ####
			self.dropTargetHurryUpTime = self.game.user_settings['Feature']['Drop Target Time']

	def mode_started(self):
		self.resetDrops()

	def resetDrops(self):
		self.dropTargetHurryUpEnabled = False
		if (self.game.switches.dropBankLeft.is_active() == True or self.game.switches.dropBankMid.is_active() == True or self.game.switches.dropBankRight.is_active() == True):
			self.game.utilities.acCoilPulse('dropReset_CenterRampFlashers2')

	def checkForCompletion(self):
		if (self.game.switches.dropBankLeft.is_active() == True and self.game.switches.dropBankMid.is_active() == True and self.game.switches.dropBankRight.is_active() == True):
			self.dropsCompleted()

	def dropsCompleted(self):
		self.game.jackpot_mode.incrementJackpot()
		self.game.jackpot_mode.update_lamps()
		if (self.game.jackpot_mode.jackpotMaxed == False):
			self.resetDrops()

	def dropsSwitchHandler(self):
		self.game.sound.play('drop')
		self.checkForCompletion()

	def sw_dropBankLeft_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop

	def sw_dropBankMid_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop

	def sw_dropBankRight_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop
