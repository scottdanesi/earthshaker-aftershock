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
##    _____________   __________________     ____  ___    __  _______     __________  __ __
##   / ____/ ____/ | / /_  __/ ____/ __ \   / __ \/   |  /  |/  / __ \   / ____/ __ \/ //_/
##  / /   / __/ /  |/ / / / / __/ / /_/ /  / /_/ / /| | / /|_/ / /_/ /  /___ \/ / / / ,<   
## / /___/ /___/ /|  / / / / /___/ _, _/  / _, _/ ___ |/ /  / / ____/  ____/ / /_/ / /| |  
## \____/_____/_/ |_/ /_/ /_____/_/ |_|  /_/ |_/_/  |_/_/  /_/_/      /_____/\____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode4(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode4, self).__init__(game, priority)
			self.TotalAwarded = 0
			self.MaxAwarded = 3
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode4_status',0)
		self.game.update_lamps()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode4_status',1)
		self.game.lamps.centerRamp50k.disable()
		self.game.shelter_mode.refreshPlayerInfo()
		self.game.update_lamps()

	def update_lamps(self):
		print "Update Lamps: Mode 4 Center 50k"
		self.game.lamps.centerRamp50k.schedule(schedule=0xF0F0F0F0, cycle_seconds=0, now=True)

	def sw_centerRampMiddle_active(self, sw):
		if (self.game.utilities.get_player_stats('ball_in_play') == True):
				self.game.utilities.score(50000)
				self.TotalAwarded += 1
		if (self.TotalAwarded <= self.MaxAwarded):
			pass				
		else:
			self.game.modes.remove(self)
		return procgame.game.SwitchContinue


