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
##     __  _____  ____  ______________  ___    __    __ 
##    /  |/  / / / / / /_  __/  _/ __ )/   |  / /   / / 
##   / /|_/ / / / / /   / /  / // __  / /| | / /   / /  
##  / /  / / /_/ / /___/ / _/ // /_/ / ___ |/ /___/ /___
## /_/  /_/\____/_____/_/ /___/_____/_/  |_/_____/_____/
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
from random import choice
from random import seed

class Multiball(game.Mode):
	def __init__(self, game, priority):
			super(Multiball, self).__init__(game, priority)
			self.ballsLocked = 0

	def mode_started(self):
		self.getUserStats()
		self.update_lamps()
		return super(Multiball, self).mode_started()

	def mode_stopped(self):
		return super(Multiball, self).mode_stopped()

	def update_lamps(self):
		self.disableLockLamps()
		if (self.ballLock1Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
		elif (self.ballLock2Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
		elif (self.ballLock3Lit == True):
			#self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			
	def disableLockLamps(self):
		self.game.lamps.rightRampLock.disable()
		self.game.lamps.ejectLock.disable()
		self.game.lamps.dropHoleLock.disable()

	def getUserStats(self):
		self.ballLock1Lit = self.game.utilities.get_player_stats('lock1_lit')
		self.ballLock2Lit = self.game.utilities.get_player_stats('lock2_lit')
		self.ballLock3Lit = self.game.utilities.get_player_stats('lock3_lit')
		self.ballsLocked = self.game.utilities.get_player_stats('balls_locked')

	def liteLock(self,callback):
		self.callback = callback
		if (self.ballsLocked == 0):
			self.ballLock1Lit = True
		elif (self.ballsLocked == 1):
			self.ballLock2Lit = True
		elif (self.ballsLocked == 2):
			self.ballLock3Lit = True
		self.update_lamps()

	def lockBall1(self):
		self.ballsLocked = 1
		self.ballLock1Lit = False
		self.update_lamps()
		self.callback()

	def lockBall2(self):
		self.ballsLocked = 2
		self.ballLock2Lit = False
		self.update_lamps()
		self.callback()

	def startMultiball(self):
		self.callback()

	def sw_underPlayfieldDrop1_active(self, sw):
		if (self.ballLock1Lit == True):
			self.lockBall1()
		elif (self.ballLock2Lit == True):
			self.lockBall2()
		elif (self.ballLock3Lit == True):
			self.startMultiball()
		else:
			pass


