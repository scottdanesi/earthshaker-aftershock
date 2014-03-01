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
##     ____  ____  _   ____  _______
##    / __ )/ __ \/ | / / / / / ___/
##   / __  / / / /  |/ / / / /\__ \ 
##  / /_/ / /_/ / /|  / /_/ /___/ / 
## /_____/\____/_/ |_/\____//____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Bonus(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Bonus, self).__init__(game, priority)
			self.delay_time = 1.6
			self.total_value = 0
			self.miles_value = 2000

	def mode_started(self):
		# Disable the flippers
		self.game.coils.flipperEnable.disable()
		self.game.sound.stop_music()

	def mode_stopped(self):
		# Enable the flippers
		self.game.coils.flipperEnable.enable()
		self.game.sound.stop_music()

	def calculate(self,callback):
		#self.game.sound.play_music('bonus', loops=1)
		self.callback = callback
		self.total_value = self.game.utilities.get_player_stats('miles') * self.miles_value * self.game.utilities.get_player_stats('bonus_x')
		self.miles()

	def miles(self):
		self.game.utilities.displayText(priority=self.priority,topText=str(self.game.utilities.get_player_stats('miles'))+' MILES'.upper(),bottomText=locale.format("%d", self.game.utilities.get_player_stats('miles') * self.miles_value, True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_features')
		self.game.coils.backboxLighting.pulse(100)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.multiplier)

	def multiplier(self):
		self.game.utilities.displayText(priority=self.priority,topText='X'+str(self.game.utilities.get_player_stats('bonus_x')).upper(),bottomText=locale.format("%d", self.total_value, True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_features')
		self.game.coils.backboxLighting.pulse(100)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.total)

	def total(self):
		self.game.utilities.score(self.total_value) # this should upadte the player score in question
		self.game.utilities.displayText(priority=self.priority,topText=locale.format("%d", self.game.utilities.currentPlayerScore(), True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_total')
		self.game.coils.backboxLighting.schedule(schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.finish)		

	def finish(self):
		self.game.sound.stop_music()
		self.callback()
		#self.game.base_mode.end_ball()