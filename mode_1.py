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
##    _____ __  ______  __________         ___________________
##   / ___// / / / __ \/ ____/ __ \       / / ____/_  __/ ___/
##   \__ \/ / / / /_/ / __/ / /_/ /  __  / / __/   / /  \__ \ 
##  ___/ / /_/ / ____/ /___/ _, _/  / /_/ / /___  / /  ___/ / 
## /____/\____/_/   /_____/_/ |_|   \____/_____/ /_/  /____/  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode1(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode1, self).__init__(game, priority)
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode1_status',0)
		self.update_lamps()

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode1_status',1)

	def update_lamps(self):
		print "Update Lamps: Mode 1 Jet Bumpers"
		self.game.lamps.jetLeftLamp.schedule(schedule=0x000F000F, cycle_seconds=0, now=True)
		self.game.lamps.jetRightLamp.schedule(schedule=0xF0F0F0F0, cycle_seconds=0, now=True)	
		self.game.lamps.jetTopLamp.schedule(schedule=0x0F000F00, cycle_seconds=0, now=True)	
		self.game.lamps.jetCenter.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)	

	def sw_jetLeft_active(self, sw):
		self.game.sound.play('jet_super')
		self.game.utilities.acFlashPulse(coilname='californiaFault_CenterRampFlashers3',pulsetime=60)
		self.game.utilities.score(5000)
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		self.game.sound.play('jet_super')
		self.game.utilities.acFlashPulse(coilname='californiaFault_CenterRampFlashers3',pulsetime=60)
		self.game.utilities.score(5000)
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		self.game.sound.play('jet_super')
		self.game.utilities.acFlashPulse(coilname='californiaFault_CenterRampFlashers3',pulsetime=60)
		self.game.utilities.score(5000)
		return procgame.game.SwitchStop
		
		


