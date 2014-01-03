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
##    _____ __________  ____  ______   __  _____    _   ______  __    __________ 
##   / ___// ____/ __ \/ __ \/ ____/  / / / /   |  / | / / __ \/ /   / ____/ __ \
##   \__ \/ /   / / / / /_/ / __/    / /_/ / /| | /  |/ / / / / /   / __/ / /_/ /
##  ___/ / /___/ /_/ / _, _/ /___   / __  / ___ |/ /|  / /_/ / /___/ /___/ _, _/ 
## /____/\____/\____/_/ |_/_____/  /_/ /_/_/  |_/_/ |_/_____/_____/_____/_/ |_|  
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import scoredisplay
from scoredisplay import AlphaScoreDisplay

class ScoreHandler(game.Mode):
	def __init__(self, game):
			super(ScoreHandler, self).__init__(game=game, priority=7)

	def mode_started(self):
		pass

	def mode_stopped(self):
		pass

	def update_display(self):
		self.p = self.game.current_player()
		self.score_display.set_text(str(self.p.score),0)
		self.score_display.set_text("Ball "+str(self.game.ball),1)
		
	def score(self, points):
		p = self.game.current_player()
		p.score += points
		#self.cancel_delayed('updatescore')
		#self.delay(name='updatescore',delay=0.5,handler=self.update_display)