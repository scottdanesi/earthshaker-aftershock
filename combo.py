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
## A P-ROC Project by Scott Danesi, Copyright 2013-2015
## Built on the PyProcGame Framework from Adam Preble and Gerry Stellenberg
#################################################################################

#################################################################################
##    __________  __  _______  ____     __  _______  ____  ______
##   / ____/ __ \/  |/  / __ )/ __ \   /  |/  / __ \/ __ \/ ____/
##  / /   / / / / /|_/ / __  / / / /  / /|_/ / / / / / / / __/   
## / /___/ /_/ / /  / / /_/ / /_/ /  / /  / / /_/ / /_/ / /___   
## \____/\____/_/  /_/_____/\____/  /_/  /_/\____/_____/_____/   
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Combo(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Combo, self).__init__(game, priority)
			self.currentComboInt = -1
			self.comboTime = 3
			
	def mode_started(self):
		pass

	def mode_stopped(self):
		self.cancel_delayed('comboReset')
		self.game.coils.unused_RightRampFlashers3.disable()

	def update_lamps(self):
		pass

	def resetComboInt(self):
		self.currentComboInt = -1
		self.game.coils.unused_RightRampFlashers3.disable()

	def evaluateCombo(self):
		self.cancel_delayed('comboReset')
		self.game.coils.unused_RightRampFlashers3.disable()
		self.currentComboInt += 1
		if (self.currentComboInt == 0):
			#no point value
			pass
		elif (self.currentComboInt == 1):
			self.game.sound.play('combo1')
			self.earnedPoints = 10000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 2):
			self.game.sound.play('combo2')
			self.earnedPoints = 20000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 3):
			self.game.sound.play('combo3')
			self.earnedPoints = 40000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 4):
			self.game.sound.play('combo4')
			self.earnedPoints = 80000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 5):
			self.game.sound.play('combo5')
			self.earnedPoints = 160000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 6):
			self.game.sound.play('combo6')
			self.earnedPoints = 320000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 7):
			self.game.sound.play('combo7')
			self.earnedPoints = 640000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		elif (self.currentComboInt == 8):
			self.game.sound.play('combo8')
			self.earnedPoints = 1280000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)
		else:
			self.game.sound.play('combo8')
			self.earnedPoints = 1280000
			self.game.utilities.score(self.earnedPoints)
			self.delay(delay=.5,handler=self.game.sound.play_voice,param='complete_shot')
			self.game.utilities.displayText(priority=self.priority,topText='LOOP COMBO ' + str(self.currentComboInt),bottomText=locale.format("%d", self.earnedPoints, True) + ' POINTS',justify='center',seconds=self.comboTime)

		self.delay(name='comboReset',delay=self.comboTime,handler=self.resetComboInt)
		self.game.coils.unused_RightRampFlashers3.schedule(schedule=0x0C0C0C0C, cycle_seconds=0, now=False)

	def sw_rightLoop6_closed(self, sw):
		if sw.time_since_change() > 0.5:
			self.game.sound.play('combo_swoosh')
			self.evaluateCombo()
		return procgame.game.SwitchContinue
		
	def sw_ballPopperTop_closed(self, sw):
		if sw.time_since_change() > 0.5:
			self.evaluateCombo()
		return procgame.game.SwitchContinue
		



