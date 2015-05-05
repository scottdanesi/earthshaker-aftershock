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
##     ____  ____  _   ____  _______    __  _____  ____  ______________  __    ______________ 
##    / __ )/ __ \/ | / / / / / ___/   /  |/  / / / / / /_  __/  _/ __ \/ /   /  _/ ____/ __ \
##   / __  / / / /  |/ / / / /\__ \   / /|_/ / / / / /   / /  / // /_/ / /    / // __/ / /_/ /
##  / /_/ / /_/ / /|  / /_/ /___/ /  / /  / / /_/ / /___/ / _/ // ____/ /____/ // /___/ _, _/ 
## /_____/\____/_/ |_/\____//____/  /_/  /_/\____/_____/_/ /___/_/   /_____/___/_____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging

class BonusMultiplier(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(BonusMultiplier, self).__init__(game, priority)
			
	def mode_started(self):
		self.update_lamps()

	def mode_stopped(self):
		pass

	def update_lamps(self):
		#### Get Multiplier ####
		self.multiplier = self.game.utilities.get_player_stats('bonus_x')

		#### Clear Lamps ####
		self.game.lamps.bonus2x.disable()
		self.game.lamps.bonus3x.disable()
		self.game.lamps.bonus4x.disable()
		self.game.lamps.bonus5x.disable()
		self.game.lamps.bonus6xExtraBall.disable()
		self.game.lamps.bonus6xSpecial.disable()

		if (self.multiplier > 1):
			self.game.lamps.bonus2x.enable()
		if (self.multiplier > 2):
			self.game.lamps.bonus3x.enable()
		if (self.multiplier > 3):
			self.game.lamps.bonus4x.enable()
		if (self.multiplier > 4):
			self.game.lamps.bonus5x.enable()
		if (self.multiplier > 5):
			self.game.lamps.bonus6xExtraBall.enable()
			
	def incrementBonusMultiplier(self):
		self.multiplier = self.game.utilities.get_player_stats('bonus_x')
		if (self.multiplier <> 6):
			self.game.utilities.set_player_stats('bonus_x',self.multiplier + 1)
			#self.game.sound.play('bonus_multiplier_vox')
			self.update_lamps()
		else:
			#### Bonus Maxed ####
			pass

		
		


