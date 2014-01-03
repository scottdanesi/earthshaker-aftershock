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
##     ____  ___    __    __       _____ ___ _    ____________ 
##    / __ )/   |  / /   / /      / ___//   | |  / / ____/ __ \
##   / __  / /| | / /   / /       \__ \/ /| | | / / __/ / /_/ /
##  / /_/ / ___ |/ /___/ /___    ___/ / ___ | |/ / /___/ _, _/ 
## /_____/_/  |_/_____/_____/   /____/_/  |_|___/_____/_/ |_|  
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import scoredisplay
from scoredisplay import AlphaScoreDisplay
#from base import AlphaScoreDisplay

class BallSaver(game.Mode):
	def __init__(self, game):
			super(BallSaver, self).__init__(game=game, priority=100)

	def mode_started(self):
		self.startBallSaverLamps()

	def mode_stopped(self):
		self.stopSkillshotLamps()

	def update_display(self):
		self.p = self.game.current_player()
		self.score_display.set_text(str(self.p.score),0)
		self.score_display.set_text("Ball "+str(self.game.ball),1)
		
	def startBallSaverLamps(self):
		self.game.lamps.shootAgain.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=False)

	def stopBallSaverLamps(self):
		self.game.lamps.shootAgain.disable()

	def sw_outhole_active(self, sw):
		#Kick another ball
		return procgame.game.SwitchStop