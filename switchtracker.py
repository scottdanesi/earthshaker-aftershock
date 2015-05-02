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
##    ______       ____________________  __   __________  ___   ________ __ __________ 
##   / ___/ |     / /  _/_  __/ ____/ / / /  /_  __/ __ \/   | / ____/ //_// ____/ __ \
##   \__ \| | /| / // /  / / / /   / /_/ /    / / / /_/ / /| |/ /   / ,<  / __/ / /_/ /
##  ___/ /| |/ |/ // /  / / / /___/ __  /    / / / _, _/ ___ / /___/ /| |/ /___/ _, _/ 
## /____/ |__/|__/___/ /_/  \____/_/ /_/    /_/ /_/ |_/_/  |_\____/_/ |_/_____/_/ |_|  
## 
## This mode will be used to track all switch hits during the game.  Will get
## loaded and unloaded for each ball.
#################################################################################

import procgame.game
from procgame import *
import pinproc
import locale
import logging

class SwitchTrackerMode(game.Mode):
	def __init__(self, game, priority):
			super(SwitchTrackerMode, self).__init__(game, priority)
			##############################
			#### Set Global Variables ####
			##############################
			self.greatharm_switchnames = []
			self.ballSearchDelayTime = 15
			
			for switch in self.game.switches.items_tagged('greatharm'):
				self.greatharm_switchnames.append(switch.name)

			for switch in self.greatharm_switchnames:
				self.add_switch_handler(name=switch, event_type='active', delay=None, handler=self.greatharm_switch_handler)

	def greatharm_switch_handler(self,sw):
		self.cancel_delayed('ballSearchTimer')
		self.game.utilities.set_player_stats('greatharm_switch_hits',self.game.utilities.get_player_stats('greatharm_switch_hits') + 1)
		self.delay(name='ballSearchTimer',delay=self.ballSearchDelayTime,handler=self.ballSearch)

	def ballSearch(self):
		if self.game.utilities.get_player_stats('ball_in_play') == True:
			self.game.utilities.executeBallSearch()

	def mode_started(self):
		pass

	def mode_stopped(self):
		pass


