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
			self.jackpotMaxed = False

			#### Load Mode Feature Defaults ####
			self.jackpotHold = self.game.user_settings['Feature']['Jackpot Hold']
			self.dropTargetHurryUpTime = self.game.user_settings['Feature']['Drop Target Time']

	def mode_started(self):
		self.cancel_delayed('dropReset')
		if (self.jackpotHold == False):
			self.game.utilities.set_player_stats('jackpot_level',1)
		self.resetDrops()
		self.update_lamps()

	def mode_stopped(self):
		self.cancel_delayed('dropReset')
		#self.game.utilities.set_player_stats('jackpot_level',1)

	def update_lamps(self):
		print "Update Lamps: Drop Targets"
		self.jackpotLevel = self.game.utilities.get_player_stats('jackpot_level')
		print 'Drop Targets Update Lamps Called'
		for i in range(1,8):
			if (self.jackpotLevel == i):
				self.jackpotLamp = 'jackpot' + str(i)
				self.game.lamps[self.jackpotLamp].schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			else:
				self.jackpotLamp = 'jackpot' + str(i)
				self.game.lamps[self.jackpotLamp].disable()

	def resetDrops(self):
		self.dropTargetHurryUpEnabled = False
		if (self.game.switches.dropBankLeft.is_active() == True or self.game.switches.dropBankMid.is_active() == True or self.game.switches.dropBankRight.is_active() == True):
			self.game.utilities.acCoilPulse('dropReset_CenterRampFlashers2')

	def incrementJackpot(self):
		if (self.game.utilities.get_player_stats('jackpot_level') < 7):
			self.game.utilities.set_player_stats('jackpot_level',self.game.utilities.get_player_stats('jackpot_level') + 1)
			self.game.utilities.displayText(self.priority,topText='JACKPOT',bottomText='INCREASED',justify='center',seconds=2)
		if (self.game.utilities.get_player_stats('jackpot_level') == 7):
			self.jackpotMaxed = True

	def checkForCompletion(self):
		if (self.game.switches.dropBankLeft.is_active() == True and self.game.switches.dropBankMid.is_active() == True and self.game.switches.dropBankRight.is_active() == True):
			self.dropsCompleted()

	def dropsCompleted(self):
		self.cancel_delayed('dropReset')
		self.incrementJackpot()
		self.update_lamps()
		if (self.jackpotMaxed == False):
			self.resetDrops()

	def dropsSwitchHandler(self):
		self.game.sound.play('drop')
		if self.jackpotMaxed == False:
			if (self.dropTargetHurryUpEnabled == False):
				self.dropTargetHurryUpEnabled = True
				print 'Drop Target Hurry Time: ' + str(self.dropTargetHurryUpTime)
				self.delay(name='dropReset',delay=self.dropTargetHurryUpTime,handler=self.resetDrops)
			else:
				self.checkForCompletion()
		else:
			#Leave drop targets down as the jackpot is maxed
			self.cancel_delayed('dropReset')

	def sw_dropBankLeft_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop

	def sw_dropBankMid_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop

	def sw_dropBankRight_closed(self, sw):
		self.dropsSwitchHandler()
		return procgame.game.SwitchStop
