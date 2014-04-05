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
			self.ballLock1Lit = False
			self.ballLock2Lit = False
			self.ballLock3Lit = False
			self.multiballStarting = False
			self.multiballIntroLength = 11.287

	def mode_started(self):
		self.getUserStats()
		self.update_lamps()
		return super(Multiball, self).mode_started()

	#def mode_stopped(self):
		#self.game.update_lamps()

	def update_lamps(self):
		print "Update Lamps: Multiball"
		self.disableLockLamps()
		if (self.ballLock1Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			print "Lock 1 is Lit"
		elif (self.ballLock2Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			print "Lock 2 is Lit"
		elif (self.ballLock3Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			print "Lock 3 is Lit"
			
	def disableLockLamps(self):
		self.game.lamps.rightRampLock.disable()
		self.game.lamps.ejectLock.disable()
		self.game.lamps.dropHoleLock.disable()

	def getUserStats(self):
		self.ballLock1Lit = self.game.utilities.get_player_stats('lock1_lit')
		self.ballLock2Lit = self.game.utilities.get_player_stats('lock2_lit')
		self.ballLock3Lit = self.game.utilities.get_player_stats('lock3_lit')
		self.ballsLocked = self.game.utilities.get_player_stats('balls_locked')
		print "Lock 1: " + str(self.game.utilities.get_player_stats('lock1_lit'))
		print "Lock 2: " + str(self.game.utilities.get_player_stats('lock2_lit'))
		print "Lock 3: " + str(self.game.utilities.get_player_stats('lock3_lit'))
		print "Balls Locked: " + str(self.game.utilities.get_player_stats('balls_locked'))

	def liteLock(self,callback):
		self.callback = callback
		if (self.ballsLocked == 0):
			self.game.utilities.set_player_stats('lock1_lit',True)
			print "Setting Ball 1 Lock to Lit"
			self.getUserStats()
		elif (self.ballsLocked == 1):
			self.game.utilities.set_player_stats('lock2_lit',True)
			self.getUserStats()
		elif (self.ballsLocked == 2):
			self.game.utilities.set_player_stats('lock3_lit',True)
			self.getUserStats()
		self.update_lamps()

	def lockBall1(self):
		self.game.utilities.set_player_stats('balls_locked',1)
		self.game.utilities.set_player_stats('lock1_lit',False)
		self.getUserStats()
		self.update_lamps()
		self.callback()

	def lockBall2(self):
		self.game.utilities.set_player_stats('balls_locked',2)
		self.game.utilities.set_player_stats('lock2_lit',False)
		self.getUserStats()
		self.update_lamps()
		self.callback()

	def startMultiball(self):
		self.multiballStarting = True
		self.game.utilities.set_player_stats('multiball_running',True)
		self.resetMultiballStats()
		self.game.collect_mode.incrementActiveZoneLimit()
		self.getUserStats()
		self.update_lamps()
		self.multiballIntro()

	def multiballIntro(self):
		self.game.utilities.disableGI()
		self.game.sound.stop_music()
		# Sound FX #
		self.game.sound.play('main_loop_tape_stop')
		self.game.sound.play('earthquake_1')
		self.game.sound.play_music('multiball_intro',loops=1,music_volume=.5)
		self.game.coils.quakeMotor.schedule(schedule=0x08080808,cycle_seconds=-1,now=True)
		self.resetMultiballStats()
		self.delay(delay=self.multiballIntroLength,handler=self.multiballRun)

	def multiballRun(self):
		self.game.utilities.enableGI()
		self.game.sound.play('centerRampComplete')
		self.game.sound.play_music('multiball_loop',loops=-1,music_volume=.6)
		self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		self.game.trough.launch_balls(num=2)
		self.multiballStarting = False
		self.game.update_lamps()

	def stopMultiball(self):
		self.game.utilities.set_player_stats('multiball_running',False)
		self.game.sound.stop_music()
		self.game.sound.play_music('main',loops=-1,music_volume=.5)
		self.resetMultiballStats()
		self.game.update_lamps()
		self.game.coils.quakeMotor.disable()
		self.callback()

	def resetMultiballStats(self):
		self.game.utilities.set_player_stats('lock1_lit',False)
		self.game.utilities.set_player_stats('lock2_lit',False)
		self.game.utilities.set_player_stats('lock3_lit',False)
		self.game.utilities.set_player_stats('balls_locked',0)
		self.getUserStats()
		
	def sw_underPlayfieldDrop1_active(self, sw):
		if (self.ballLock1Lit == True):
			self.lockBall1()
		elif (self.ballLock2Lit == True):
			self.lockBall2()
		elif (self.ballLock3Lit == True):
			self.startMultiball()
		else:
			pass

	def sw_ballPopperBottom_closed(self, sw):
		if(self.multiballStarting == True):
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_outhole_closed_for_500ms(self, sw):
		#if (self.game.trough.num_balls_in_play == 2):
			#Last ball - Need to stop multiball
			#self.stopMultiball()
		return procgame.game.SwitchContinue



