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

class Mode6(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode6, self).__init__(game, priority)
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode6_status',0)
		self.game.update_lamps()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode6_status',1)

	def update_lamps(self):
		print "Update Lamps: Mode 6 Spinner"
		self.game.lamps.inlaneRightSpinner.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)
		self.game.lamps.spinner.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)		

	def sw_spinner_active(self, sw):
		self.game.utilities.score(6000)
		self.game.utilities.acFlashPulse(coilname='dropReset_CenterRampFlashers2',pulsetime=40)
		self.game.sound.play('super_spinner')
		return procgame.game.SwitchStop

	def sw_rightOutsideReturn_active(self, sw):
		return procgame.game.SwitchContinue


