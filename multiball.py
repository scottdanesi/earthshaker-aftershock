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

			### Active Multiball Variables ###
			self.zone1Staus = -1
			self.zone2Staus = -1
			self.zone3Staus = -1
			self.zone4Staus = -1
			self.zone5Staus = -1
			self.zone6Staus = -1
			self.zone7Staus = -1
			self.zone8Staus = -1
			self.zone9Staus = -1

	def mode_started(self):
		self.getUserStats()
		self.update_lamps()
		return super(Multiball, self).mode_started()

	def mode_stopped(self):
		pass

	def update_lamps(self):
		print "Update Lamps: Multiball"
		self.disableLockLamps()
		if (self.ballLock1Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			self.game.lamps.ejectLock.schedule(schedule=0x0FF00FF0, cycle_seconds=0, now=True)
			print "Lock 1 is Lit"
		elif (self.ballLock2Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			print "Lock 2 is Lit"
		elif (self.ballLock3Lit == True):
			self.game.lamps.dropHoleLock.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=True)
			self.game.lamps.rightRampLock.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
			print "Lock 3 is Lit"

		if (self.game.utilities.get_player_stats('multiball_running') == True):
			self.refreshMultiballZones()

			if (self.zone1Staus == -1):
				self.game.lamps.standupLeft1.disable()
			if (self.zone2Staus == -1):
				self.game.lamps.standupRightHigh2.disable()
			if (self.zone3Staus == -1):
				self.game.lamps.standupRightLow3.disable()
			if (self.zone4Staus == -1):
				self.game.lamps.standupCenter4.disable()
			if (self.zone5Staus == -1):
				self.game.lamps.ejectTop5.disable()
			if (self.zone6Staus == -1):
				self.game.lamps.underFaultLoop6.disable()
			if (self.zone7Staus == -1):
				self.game.lamps.inlaneRight7.disable()
			if (self.zone8Staus == -1):
				self.game.lamps.inlaneLeft8.disable()
			if (self.zone9Staus == -1):
				self.game.lamps.captiveArrow9.disable()

			if (self.zone1Staus == 0):
				self.game.lamps.standupLeft1.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone2Staus == 0):
				self.game.lamps.standupRightHigh2.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone3Staus == 0):
				self.game.lamps.standupRightLow3.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone4Staus == 0):
				self.game.lamps.standupCenter4.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone5Staus == 0):
				self.game.lamps.ejectTop5.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone6Staus == 0):
				self.game.lamps.underFaultLoop6.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone7Staus == 0):
				self.game.lamps.inlaneRight7.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone8Staus == 0):
				self.game.lamps.inlaneLeft8.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)
			if (self.zone9Staus == 0):
				self.game.lamps.captiveArrow9.schedule(schedule=0xCCCCCCCC, cycle_seconds=0, now=True)

			if (self.zone1Staus == 1):
				self.game.lamps.standupLeft1.enable()
			if (self.zone2Staus == 1):
				self.game.lamps.standupRightHigh2.enable()
			if (self.zone3Staus == 1):
				self.game.lamps.standupRightLow3.enable()
			if (self.zone4Staus == 1):
				self.game.lamps.standupCenter4.enable()
			if (self.zone5Staus == 1):
				self.game.lamps.ejectTop5.enable()
			if (self.zone6Staus == 1):
				self.game.lamps.underFaultLoop6.enable()
			if (self.zone7Staus == 1):
				self.game.lamps.inlaneRight7.enable()
			if (self.zone8Staus == 1):
				self.game.lamps.inlaneLeft8.enable()
			if (self.zone9Staus == 1):
				self.game.lamps.captiveArrow9.enable()

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
		self.game.sound.play('ball_lock_1')
		self.game.utilities.set_player_stats('balls_locked',1)
		self.game.utilities.set_player_stats('lock1_lit',False)
		self.getUserStats()
		self.update_lamps()
		self.callback()

	def lockBall2(self):
		self.game.sound.play('ball_lock_2')
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
		self.cancel_delayed('dropReset')
		self.game.utilities.disableGI()
		self.game.sound.stop_music()
		self.game.lampctrlflash.play_show('multiball_intro_1', repeat=False)
		self.game.utilities.randomLampPulse(100)
		# Sound FX #
		self.game.sound.play('earthquake_1')
		self.game.sound.play_music('multiball_intro',loops=1,music_volume=.5)
		#Short Out Noises
		self.delay(delay=2,handler=self.game.sound.play,param='short_out_2')
		self.delay(delay=3,handler=self.game.sound.play,param='short_out_1')
		self.delay(delay=4.5,handler=self.game.sound.play,param='short_out_1')
		self.delay(delay=6,handler=self.game.sound.play,param='short_out_2')
		self.delay(delay=8,handler=self.game.sound.play,param='short_out_1')
		self.delay(delay=9,handler=self.game.sound.play,param='short_out_2')
		self.delay(delay=10,handler=self.game.sound.play,param='short_out_1')
		
		#self.game.coils.quakeMotor.schedule(schedule=0x08080808,cycle_seconds=-1,now=True)
		self.resetMultiballStats()
		self.delay(delay=self.multiballIntroLength,handler=self.multiballRun)

	def multiballRun(self):
		self.game.utilities.enableGI()
		#self.game.coils.quakeMotor.patter(on_time=15,off_time=100)
		self.game.utilities.enableMultiballQuake()
		self.game.sound.play('centerRampComplete')
		self.game.sound.play_music('multiball_loop',loops=-1,music_volume=.6)
		self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		self.game.trough.launch_balls(num=2)
		self.multiballStarting = False
		self.game.update_lamps()

	def stopMultiball(self):
		self.game.utilities.set_player_stats('multiball_running',False)
		self.game.utilities.set_player_stats('jackpot_lit',False)
		self.game.sound.stop_music()
		self.game.sound.play_music('main',loops=-1,music_volume=.5)
		self.resetMultiballStats()
		self.game.bonusmultiplier_mode.incrementBonusMultiplier()
		self.game.update_lamps()
		self.game.coils.quakeMotor.disable()
		self.callback()

	def resetMultiballStats(self):
		self.game.utilities.set_player_stats('lock1_lit',False)
		self.game.utilities.set_player_stats('lock2_lit',False)
		self.game.utilities.set_player_stats('lock3_lit',False)
		self.game.utilities.set_player_stats('balls_locked',0)
		self.getUserStats()

	def resetMultiballZones(self):
		self.zone1Staus = self.game.utilities.set_player_stats('super_jackpot_zone1_status',0)
		self.zone2Staus = self.game.utilities.set_player_stats('super_jackpot_zone2_status',-1)
		self.zone3Staus = self.game.utilities.set_player_stats('super_jackpot_zone3_status',-1)
		self.zone4Staus = self.game.utilities.set_player_stats('super_jackpot_zone4_status',-1)
		self.zone5Staus = self.game.utilities.set_player_stats('super_jackpot_zone5_status',-1)
		self.zone6Staus = self.game.utilities.set_player_stats('super_jackpot_zone6_status',-1)
		self.zone7Staus = self.game.utilities.set_player_stats('super_jackpot_zone7_status',-1)
		self.zone8Staus = self.game.utilities.set_player_stats('super_jackpot_zone8_status',-1)
		self.zone9Staus = self.game.utilities.set_player_stats('super_jackpot_zone9_status',-1)

	def refreshMultiballZones(self):
		self.zone1Staus = self.game.utilities.get_player_stats('super_jackpot_zone1_status')
		self.zone2Staus = self.game.utilities.get_player_stats('super_jackpot_zone2_status')
		self.zone3Staus = self.game.utilities.get_player_stats('super_jackpot_zone3_status')
		self.zone4Staus = self.game.utilities.get_player_stats('super_jackpot_zone4_status')
		self.zone5Staus = self.game.utilities.get_player_stats('super_jackpot_zone5_status')
		self.zone6Staus = self.game.utilities.get_player_stats('super_jackpot_zone6_status')
		self.zone7Staus = self.game.utilities.get_player_stats('super_jackpot_zone7_status')
		self.zone8Staus = self.game.utilities.get_player_stats('super_jackpot_zone8_status')
		self.zone9Staus = self.game.utilities.get_player_stats('super_jackpot_zone9_status')

	def incrementMultiballZones(self):
		if (self.zone1Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone1_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone2_status',0)
		elif (self.zone2Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone2_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone3_status',0)
		elif (self.zone3Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone3_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone4_status',0)
		elif (self.zone4Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone4_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone5_status',0)
		elif (self.zone5Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone5_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone6_status',0)
		elif (self.zone6Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone6_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone7_status',0)
		elif (self.zone7Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone7_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone8_status',0)
		elif (self.zone8Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone8_status',1)
			self.game.utilities.set_player_stats('super_jackpot_zone9_status',0)
			### Light Super Jackpot ###
			self.game.utilities.set_player_stats('super_jackpot_lit',True)
		elif (self.zone9Staus == 0):
			self.game.utilities.set_player_stats('super_jackpot_zone9_status',1)
			

		self.game.update_lamps()

	def sw_outhole_closed_for_500ms(self, sw):
		#if (self.game.trough.num_balls_in_play == 2):
			#Last ball - Need to stop multiball
			#self.stopMultiball()
		return procgame.game.SwitchContinue

	def sw_leftStandup1_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone1Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_rightStandupHigh2_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone2Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_rightStandupLow3_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone3Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_centerStandup4_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone4Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_ejectHole5_closed_for_400ms(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone5Staus == 0):
				self.incrementMultiballZones()
		return procgame.game.SwitchContinue

	def sw_rightLoop6_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone6Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_rightInsideReturn7_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone7Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_leftReturnLane8_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone8Staus == 0):
				self.incrementMultiballZones()
			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue

	def sw_captiveBall9_closed(self, sw):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.zone9Staus == 0):
				self.incrementMultiballZones()
			
			if (self.game.utilities.get_player_stats('super_jackpot_lit') == True):
				self.game.jackpot_mode.awardSuperJackpot()
				self.resetMultiballZones()

			return procgame.game.SwitchStop
		else:
			return procgame.game.SwitchContinue



