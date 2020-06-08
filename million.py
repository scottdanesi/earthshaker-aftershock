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
##     __  _________    __    ________  _   __   __  _______  ____  ______
##    /  |/  /  _/ /   / /   /  _/ __ \/ | / /  /  |/  / __ \/ __ \/ ____/
##   / /|_/ // // /   / /    / // / / /  |/ /  / /|_/ / / / / / / / __/   
##  / /  / // // /___/ /____/ // /_/ / /|  /  / /  / / /_/ / /_/ / /___   
## /_/  /_/___/_____/_____/___/\____/_/ |_/  /_/  /_/\____/_____/_____/   
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Million(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Million, self).__init__(game, priority)
			self.millionTotalTime = 15
			
	def mode_started(self):
		#self.startLastChanceMillion()
		pass

	def mode_stopped(self):
		self.stopLastChanceMillion()
		pass

	def update_lamps(self):
		if (self.game.utilities.get_player_stats('million_lit') == True):
			self.game.lamps.rightRamp3Miles.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
		else:
			self.game.lamps.rightRamp3Miles.disable()
		
	def startCountdownTimers(self):
		self.delay(name='count0',delay=self.millionTotalTime-3,handler=self.game.sound.play,param='countdown_0_vox')
		self.delay(name='count1',delay=self.millionTotalTime-4,handler=self.game.sound.play,param='countdown_1_vox')
		self.delay(name='count2',delay=self.millionTotalTime-5,handler=self.game.sound.play,param='countdown_2_vox')
		self.delay(name='count3',delay=self.millionTotalTime-6,handler=self.game.sound.play,param='countdown_3_vox')
		self.delay(name='count4',delay=self.millionTotalTime-7,handler=self.game.sound.play,param='countdown_4_vox')
		self.delay(name='count5',delay=self.millionTotalTime-8,handler=self.game.sound.play,param='countdown_5_vox')
		self.delay(name='missed',delay=self.millionTotalTime-11,handler=self.game.sound.play,param='shoot_rr')
		#self.delay(name='count5',delay=self.millionTotalTime-12,handler=self.game.sound.play,param='countdown_5_vox') Pleacholder for Shoot Right Ramp or Last Chance Million is lit.

	def stopCountdownTimers(self):
		self.cancel_delayed('count0')
		self.cancel_delayed('count1')
		self.cancel_delayed('count2')
		self.cancel_delayed('count3')
		self.cancel_delayed('count4')
		self.cancel_delayed('count5')
		self.cancel_delayed('missed')

	def startLastChanceMillion(self):
		self.game.utilities.set_player_stats('million_lit',True)
		self.game.sound.play_voice('lcm_lit')
		self.delay(delay=15,handler=self.stopLastChanceMillion)
		self.startCountdownTimers()
		self.game.update_lamps()

	def stopLastChanceMillion(self):
		self.game.utilities.set_player_stats('million_lit',False)
		#self.game.sound.play_voice('lcm_missed')
		#self.game.utilities.set_player_stats('last_chance_million_qualified',True)
		self.stopCountdownTimers()
		self.game.update_lamps()

	def scoreLastChanceMillion(self):
		self.game.lampctrlflash.play_show('jackpot', repeat=False, callback=self.game.update_lamps)
		self.game.utilities.score(1000000)
		self.game.sound.play('million_vocal_crazy')
		self.stopLastChanceMillion()