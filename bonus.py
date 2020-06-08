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
			# Settings Variables #
			self.delay_time = 1.5
			self.miles_value = 3000
			self.totalGreatHarm=0

			# System Variables #
			self.total_value = 0
			

	def mode_started(self):

		# Disable the flippers
		self.game.coils.flipperEnable.disable()
		self.game.sound.stop_music()
		self.game.utilities.disableGI()
		self.game.million_mode.stopLastChanceMillion()

		#### Disable All Lamps ####
		for lamp in self.game.lamps:
			lamp.disable()

	def mode_stopped(self):
		# Enable the flippers
		self.game.coils.flipperEnable.enable() # Can possibly remove this and let the "Ball Start" function handle it.
		#self.game.sound.stop_music() # Only needed if using background Bonus music
		self.game.utilities.enableGI()

	def calculate(self,callback):
		#self.game.sound.play_music('bonus', loops=1)
		self.callback = callback
		self.totalGreatHarm = self.game.utilities.get_player_stats('greatharm_switch_hits') * 150
		self.total_value = ((self.game.utilities.get_player_stats('miles') * self.miles_value) + self.totalGreatHarm) * self.game.utilities.get_player_stats('bonus_x')
		self.miles()

	def miles(self):
		totalMiles=self.game.utilities.get_player_stats('miles')
		self.game.utilities.displayText(priority=self.priority,topText=str(totalMiles)+' MILES'.upper(),bottomText=locale.format("%d", totalMiles * self.miles_value, True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_features')
		self.game.lampctrlflash.play_show('bonus_feat_left', repeat=False)
		#self.game.sound.play('bonus_music')
		self.game.utilities.setBackboxLED(255,0,0,pulsetime=100)
		#self.game.utilities.acFlashSchedule(coilname='ballReleaseShooterLane_CenterRampFlashers1',schedule=0x0000000C, cycle_seconds=1, now=True)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.greatHarm)

	def greatHarm(self):
		self.game.utilities.displayText(priority=self.priority,topText='GREAT HARM BONUS',bottomText=str(self.totalGreatHarm),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_features')
		self.game.lampctrlflash.play_show('bonus_feat_right', repeat=False)
		self.game.utilities.setBackboxLED(255,0,0,pulsetime=100)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.multiplier)

	def multiplier(self):
		self.game.utilities.displayText(priority=self.priority,topText='X'+str(self.game.utilities.get_player_stats('bonus_x')).upper(),bottomText=locale.format("%d", self.total_value, True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_features')
		self.game.lampctrlflash.play_show('bonus_feat_left', repeat=False)
		self.game.utilities.setBackboxLED(255,0,0,pulsetime=100)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.total)

	def total(self):
		self.game.utilities.score(self.total_value) # this should upadte the player score in question
		self.game.utilities.displayText(priority=self.priority,topText=locale.format("%d", self.game.utilities.currentPlayerScore(), True),justify='center',seconds=self.delay_time)
		self.game.sound.play('bonus_total')
		#self.game.utilities.acFlashSchedule(coilname='ejectHole_CenterRampFlashers4',schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		#self.game.utilities.acFlashSchedule(coilname='outholeKicker_CaptiveFlashers',schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		#self.game.coils.backboxLightingB.schedule(schedule=0x00CCCCCC, cycle_seconds=1, now=True)
		self.game.lampctrlflash.play_show('bonus_total', repeat=False)
		self.delay(name='next_frame', event_type=None, delay=self.delay_time, handler=self.finish)		

	def finish(self):
		self.game.sound.stop_music()
		self.callback()
		#self.game.base_mode.end_ball()