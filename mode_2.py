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
##     __________   ____  ____  ____ 
##    / ____/ __ \ / __ \/ __ \/ __ \
##   /___ \/ / / // / / / / / / / / /
##  ____/ / /_/ // /_/ / /_/ / /_/ / 
## /_____/\____( )____/\____/\____/  
##             |/                    
#################################################################################

import procgame
from procgame import *
import locale
import logging

class Mode2(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Mode2, self).__init__(game, priority)
			
	def mode_started(self):
		self.game.utilities.set_player_stats('mode2_status',0)
		self.game.utilities.score(50000)
		self.game.modes.remove(self)

	def mode_stopped(self):
		self.game.utilities.set_player_stats('mode2_status',1)
		self.game.shelter_mode.refreshPlayerInfo()
		self.game.update_lamps()