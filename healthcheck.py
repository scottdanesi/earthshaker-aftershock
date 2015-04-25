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
##     __  ___________    __  ________  __   ________  ________________ __
##    / / / / ____/   |  / / /_  __/ / / /  / ____/ / / / ____/ ____/ //_/
##   / /_/ / __/ / /| | / /   / / / /_/ /  / /   / /_/ / __/ / /   / ,<   
##  / __  / /___/ ___ |/ /___/ / / __  /  / /___/ __  / /___/ /___/ /| |  
## /_/ /_/_____/_/  |_/_____/_/ /_/ /_/   \____/_/ /_/_____/\____/_/ |_|  
## 
## This mode is used during gameplay to ensure that the machine knows where all
## balls are located at any given time.
#################################################################################

import procgame.game
from procgame import *
import pinproc
import locale
import logging
import math
from random import *

import player
from player import *

class HealthCheckMode(game.Mode):
	def __init__(self, game, priority):
			super(HealthCheckMode, self).__init__(game, priority)
			##############################
			#### Set Global Variables ####
			##############################
			self.healthCheckDelay = 5

	def mode_started(self):
		self.delay(name='healthcheck',delay=self.healthCheckDelay,handler=self.checkBallStatus)

	def mode_stopped(self):
		self.cancel_delayed('healthcheck')

	def checkBallStatus(self):
		#self.game.utilities.displayText(200,topText='HEALTH CHECK',bottomText='IN TROUGH ' + str(self.game.trough.num_balls()),seconds=2,justify='center')
		#if(self.game.utilities.get_player_stats('multiball_running') == True):
			#self.game.trough.checkForEndOfMultiball()
		#else:
		self.game.trough.checkForEndOfBall()
		self.delay(name='healthcheck',delay=self.healthCheckDelay,handler=self.checkBallStatus)