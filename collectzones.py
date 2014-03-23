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
##    __________  __    __    __________________   _____   ____  _   _____________
##   / ____/ __ \/ /   / /   / ____/ ____/_  __/  /__  /  / __ \/ | / / ____/ ___/
##  / /   / / / / /   / /   / __/ / /     / /       / /  / / / /  |/ / __/  \__ \ 
## / /___/ /_/ / /___/ /___/ /___/ /___  / /       / /__/ /_/ / /|  / /___ ___/ / 
## \____/\____/_____/_____/_____/\____/ /_/       /____/\____/_/ |_/_____//____/  
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
from random import choice
from random import seed

class CollectZones(game.Mode):
	def __init__(self, game, priority):
			super(CollectZones, self).__init__(game, priority)
			self.allZones = []
			self.allZones.append('zone1_status')
			self.allZones.append('zone2_status')
			self.allZones.append('zone3_status')
			self.allZones.append('zone4_status')
			self.allZones.append('zone5_status')
			self.allZones.append('zone6_status')
			self.allZones.append('zone7_status')
			self.allZones.append('zone8_status')
			self.allZones.append('zone9_status')

			self.allZoneLamps = []
			self.allZoneLamps.append('standupLeft1')
			self.allZoneLamps.append('standupRightHigh2')
			self.allZoneLamps.append('standupRightLow3')
			self.allZoneLamps.append('standupCenter4')
			self.allZoneLamps.append('ejectTop5')
			self.allZoneLamps.append('underFaultLoop6')
			self.allZoneLamps.append('inlaneRight7')
			self.allZoneLamps.append('inlaneLeft8')
			self.allZoneLamps.append('captiveArrow9')

			self.activeZoneLimit = self.game.user_settings['Feature']['Active Zone Limit']


	def mode_started(self):
		self.refreshAllZoneLists()
		if (len(self.activeZones) == 0):
			self.setNewActiveZones()
		return super(CollectZones, self).mode_started()

	def mode_stopped(self):
		return super(CollectZones, self).mode_stopped()

	def update_lamps(self):
		#Disable all zone lamps#
		for item in self.allZoneLamps:
			self.game.lamps[item].disable()

		#Enable active Zones#
		for item in self.activeZones:
			if (item == 'zone1_status'):
				self.game.lamps.standupLeft1.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone2_status'):
				self.game.lamps.standupRightHigh2.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone3_status'):
				self.game.lamps.standupRightLow3.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone4_status'):
				self.game.lamps.standupCenter4.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone5_status'):
				self.game.lamps.ejectTop5.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone6_status'):
				self.game.lamps.underFaultLoop6.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone7_status'):
				self.game.lamps.inlaneRight7.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone8_status'):
				self.game.lamps.inlaneLeft8.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'zone9_status'):
				self.game.lamps.captiveArrow9.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
		
		#Enable completed zones#
		for item in self.completedZones:
			if (item == 'zone1_status'):
				self.game.lamps.standupLeft1.enable()
			elif (item == 'zone2_status'):
				self.game.lamps.standupRightHigh2.enable()
			elif (item == 'zone3_status'):
				self.game.lamps.standupRightLow3.enable()
			elif (item == 'zone4_status'):
				self.game.lamps.standupCenter4.enable()
			elif (item == 'zone5_status'):
				self.game.lamps.ejectTop5.enable()
			elif (item == 'zone6_status'):
				self.game.lamps.underFaultLoop6.enable()
			elif (item == 'zone7_status'):
				self.game.lamps.inlaneRight7.enable()
			elif (item == 'zone8_status'):
				self.game.lamps.inlaneLeft8.enable()
			elif (item == 'zone9_status'):
				self.game.lamps.captiveArrow9.enable()

	def resetPlayerZones(self):
		for item in self.allZones:
			self.game.utilities.set_player_stats(item,-1)

	def refreshAllZoneLists(self):
		self.updateAvailableZoneList()
		self.updateActiveZoneList()
		self.updateCompletedZoneList()
		self.checkForAllCompletedZones()
		#if (len(self.activeZones) == 0):
			#self.setNewActiveZones()
		self.update_lamps()

	def checkForAllCompletedZones(self):
		if (len(self.activeZones) == 0):
			#All active zones completed
			self.game.multiball_mode.liteLock(self.game.collect_mode.setNewActiveZones)
			pass

	def updateAvailableZoneList(self):
		self.availableZones = []
		for item in self.allZones:
			if (self.game.utilities.get_player_stats(item) == -1):
				self.availableZones.append(item)

	def updateActiveZoneList(self):
		self.activeZones = []
		for item in self.allZones:
			if (self.game.utilities.get_player_stats(item) == 0):
				self.activeZones.append(item)

	def updateCompletedZoneList(self):
		self.completedZones = []
		for item in self.allZones:
			if (self.game.utilities.get_player_stats(item) == 1):
				self.completedZones.append(item)

	def setNewActiveZones(self):
		self.activeZones = []
		seed()
		if (len(self.availableZones) < self.activeZoneLimit):
			self.resetPlayerZones()
			self.updateAvailableZoneList()
			self.updateActiveZoneList()
			self.updateCompletedZoneList()
		for i in range(1,self.activeZoneLimit + 1):
			self.activeZones.append(choice(self.availableZones))
			for item in self.activeZones:
				self.game.utilities.set_player_stats(item,0)
			self.updateAvailableZoneList()
		self.update_lamps()

	def scoreZoneCollected(self):
		self.game.utilities.score(2500)
		self.game.utilities.set_player_stats('zones_visited',self.game.utilities.get_player_stats('zones_visited') + 1)
		self.game.sound.play('zone_awarded')
		self.game.utilities.shakerPulseLow()

	def zoneNotAwarded(self):
		self.game.utilities.score(250)
		


	#############################
	## Zone Switches
	#############################
	def sw_leftStandup1_closed(self, sw):
		if ('zone1_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone1_status',1)
			self.game.utilities.acFlashSchedule(coilname='californiaFault_CenterRampFlashers3',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('zone_na')
		return procgame.game.SwitchContinue

	def sw_rightStandupHigh2_closed(self, sw):
		if ('zone2_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone2_status',1)
			self.game.utilities.acFlashSchedule(coilname='outholeKicker_CaptiveFlashers',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('zone_na')
		return procgame.game.SwitchContinue

	def sw_rightStandupLow3_closed(self, sw):
		if ('zone3_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone3_status',1)
			self.game.utilities.acFlashSchedule(coilname='outholeKicker_CaptiveFlashers',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('zone_na')
		return procgame.game.SwitchContinue
		
	def sw_centerStandup4_closed(self, sw):
		if ('zone4_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone4_status',1)
			self.game.utilities.acFlashSchedule(coilname='ballReleaseShooterLane_CenterRampFlashers1',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('zone_na')
		return procgame.game.SwitchContinue
		
	def sw_ejectHole5_closed_for_100ms(self, sw):
		if ('zone5_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone5_status',1)
			self.game.utilities.acFlashSchedule(coilname='californiaFault_CenterRampFlashers3',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			pass
			#self.zoneNotAwarded()
		return procgame.game.SwitchContinue
		
	def sw_rightLoop6_closed(self, sw):
		if ('zone6_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone6_status',1)
			self.game.utilities.acFlashSchedule(coilname='bottomBallPopper_RightRampFlashers1',schedule=0x0000000E, cycle_seconds=1, now=True)
			self.game.utilities.acFlashSchedule(coilname='knocker_RightRampFlashers2',schedule=0x000000E0, cycle_seconds=1, now=True)
			self.game.utilities.acFlashSchedule(coilname='unused_RightRampFlashers3',schedule=0x00000E00, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			#self.zoneNotAwarded()
			pass
		return procgame.game.SwitchContinue
		
	def sw_rightInsideReturn7_closed(self, sw):
		if ('zone7_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone7_status',1)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('inlane')
		return procgame.game.SwitchContinue
		
	def sw_leftReturnLane8_closed(self, sw):
		if ('zone8_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone8_status',1)
			self.game.utilities.acFlashSchedule(coilname='ejectHole_CenterRampFlashers4',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('inlane')
		return procgame.game.SwitchContinue
		
	def sw_captiveBall9_closed(self, sw):
		if ('zone9_status' in self.activeZones):
			self.game.utilities.set_player_stats('zone9_status',1)
			self.game.utilities.acFlashSchedule(coilname='outholeKicker_CaptiveFlashers',schedule=0x000000CC, cycle_seconds=1, now=True)
			self.scoreZoneCollected()
			self.refreshAllZoneLists()
		else:
			self.zoneNotAwarded()
			self.game.sound.play('zone_na')
		return procgame.game.SwitchContinue