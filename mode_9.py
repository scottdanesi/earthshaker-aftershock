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
##    _________    ____  ___________    ________   _________    ____  _   _______    _____    __ 
##   / ____/   |  / __ \/_  __/  _/ |  / / ____/  / ____/   |  / __ \/ | / /  _/ |  / /   |  / / 
##  / /   / /| | / /_/ / / /  / / | | / / __/    / /   / /| | / /_/ /  |/ // / | | / / /| | / /  
## / /___/ ___ |/ ____/ / / _/ /  | |/ / /___   / /___/ ___ |/ _, _/ /|  // /  | |/ / ___ |/ /___
## \____/_/  |_/_/     /_/ /___/  |___/_____/   \____/_/  |_/_/ |_/_/ |_/___/  |___/_/  |_/_____/
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode9(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode9, self).__init__(game, priority)
			self.captiveLevel = 0
			
	def mode_started(self):
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.utilities.set_player_stats('mode9_status',0)
		self.game.shelter_mode.refreshPlayerInfo()
		self.game.update_lamps()
		self.incrementCaptiveLevel()
		

	def mode_stopped(self):
		self.captiveLevel = 0
		self.game.lamps.captive25k.disable()
		self.game.lamps.captive50k.disable()
		self.game.lamps.captive100k.disable()
		self.game.lamps.captive150k.disable()
		self.game.lamps.captive250k.disable()
		self.game.utilities.set_player_stats('mode9_status',1)


	def update_lamps(self):
		self.game.lamps.captive25k.disable()
		self.game.lamps.captive50k.disable()
		self.game.lamps.captive100k.disable()
		self.game.lamps.captive150k.disable()
		self.game.lamps.captive250k.disable()

		if self.captiveLevel >= 1:
			self.game.lamps.captive25k.enable()
		if self.captiveLevel >= 2:
			self.game.lamps.captive50k.enable()
		if self.captiveLevel >= 3:
			self.game.lamps.captive100k.enable()
		if self.captiveLevel >= 4:
			self.game.lamps.captive150k.enable()
		if self.captiveLevel == 5:
			self.game.lamps.captive250k.enable()

	def incrementCaptiveLevel(self):
		if (self.captiveLevel < 5):
			self.captiveLevel += 1
		else:
			self.captiveLevel = 1
		self.update_lamps()
		self.delay(name='increment',delay=.2,handler=self.incrementCaptiveLevel)

	def awardCaptiveValue(self):
		self.cancel_delayed('increment')
		if self.captiveLevel == 1:
			self.game.utilities.score(25000)
			self.game.lamps.captive25k.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 2:
			self.game.utilities.score(50000)
			self.game.lamps.captive50k.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 3:
			self.game.utilities.score(100000)
			self.game.lamps.captive100k.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 4:
			self.game.utilities.score(150000)
			self.game.lamps.captive150k.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		elif self.captiveLevel == 5:
			self.game.utilities.score(200000)
			self.game.lamps.captive250k.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)

		self.game.sound.play('captive_carnival')
		self.delay(delay=.1,handler=self.game.sound.play,param='captive_carnival')
		self.delay(delay=.2,handler=self.game.sound.play,param='captive_carnival')
		self.delay(delay=.4,handler=self.game.sound.play_voice,param='complete_shot')

		#self.delay(delay=2,handler=self.update_lamps)
		self.delay(delay=2,handler=self.game.modes.remove,param=self)

	def sw_captiveBall9_closed(self, sw):
		self.awardCaptiveValue()
		return procgame.game.SwitchStop