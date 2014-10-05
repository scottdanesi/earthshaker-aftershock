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
##    _____ __  __________  ________________ 
##   / ___// / / / ____/ / /_  __/ ____/ __ \
##   \__ \/ /_/ / __/ / /   / / / __/ / /_/ /
##  ___/ / __  / /___/ /___/ / / /___/ _, _/ 
## /____/_/ /_/_____/_____/_/ /_____/_/ |_|  
## 
#################################################################################

import procgame
from procgame import *
import locale
import logging
from random import choice
from random import seed

class Shelter(game.Mode):
	"""docstring for Bonus"""
	def __init__(self, game, priority):
			super(Shelter, self).__init__(game, priority)
			# Settings Variables #
			self.enterSwitch1Triggered = False
			self.enterSwitch2Triggered = False
			self.modeSelectorActive = False

			self.allModes = []
			self.allModes.append('mode1_status')
			self.allModes.append('mode2_status')
			self.allModes.append('mode3_status')
			self.allModes.append('mode4_status')
			self.allModes.append('mode5_status')
			self.allModes.append('mode6_status')
			self.allModes.append('mode7_status')
			self.allModes.append('mode8_status')
			self.allModes.append('mode9_status')

			self.allModeLamps = []
			self.allModeLamps.append('building1')
			self.allModeLamps.append('building2')
			self.allModeLamps.append('building3')
			self.allModeLamps.append('building4')
			self.allModeLamps.append('building5')
			self.allModeLamps.append('building6')
			self.allModeLamps.append('building7')
			self.allModeLamps.append('building8')
			self.allModeLamps.append('building9')
			
	def mode_started(self):
		self.game.utilities.log('Select Mode - Mode Started','info')
		self.refreshPlayerInfo()
		self.update_lamps()
		return super(Shelter, self).mode_started()

	def mode_stopped(self):
		pass

	def update_lamps(self):
		print "Update Lamps: Select Modes"
		self.game.utilities.log('Select Mode - Update Lamps','info')
		#Disable all zone lamps#
		for item in self.allModeLamps:
			self.game.lamps[item].disable()

		#Enable active Zones#
		for item in self.activeModes:
			if (item == 'mode1_status'):
				self.game.lamps.building1.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode2_status'):
				self.game.lamps.building2.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode3_status'):
				self.game.lamps.building3.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode4_status'):
				self.game.lamps.building4.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode5_status'):
				self.game.lamps.building5.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode6_status'):
				self.game.lamps.building6.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode7_status'):
				self.game.lamps.building7.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode8_status'):
				self.game.lamps.building8.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
			elif (item == 'mode9_status'):
				self.game.lamps.building9.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
		
		#Enable completed zones#
		for item in self.completedModes:
			if (item == 'mode1_status'):
				self.game.lamps.building1.enable()
			elif (item == 'mode2_status'):
				self.game.lamps.building2.enable()
			elif (item == 'mode3_status'):
				self.game.lamps.building3.enable()
			elif (item == 'mode4_status'):
				self.game.lamps.building4.enable()
			elif (item == 'mode5_status'):
				self.game.lamps.building5.enable()
			elif (item == 'mode6_status'):
				self.game.lamps.building6.enable()
			elif (item == 'mode7_status'):
				self.game.lamps.building7.enable()
			elif (item == 'mode8_status'):
				self.game.lamps.building8.enable()
			elif (item == 'mode9_status'):
				self.game.lamps.building9.enable()

	def resetPlayerModes(self):
		self.game.utilities.log('Select Mode - Reset Player Zones','info')
		for item in self.allModes:
			self.game.utilities.set_player_stats(item,-1)

	def refreshPlayerInfo(self):
		self.game.utilities.log('Select Mode - Refesh Player Zones','info')
		self.updateAvailableModeList()
		self.updateActiveModeList()
		self.updateCompletedModeList()


	def updateAvailableModeList(self):
		self.game.utilities.log('Select Mode - Update Player Available mode List','info')
		self.availableModes = []
		for item in self.allModes:
			if (self.game.utilities.get_player_stats(item) == -1):
				self.availableModes.append(item)

	def updateActiveModeList(self):
		self.game.utilities.log('Select Mode - Update Player Active mode List','info')
		self.activeModes = []
		for item in self.allModes:
			if (self.game.utilities.get_player_stats(item) == 0):
				self.activeModes.append(item)

	def updateCompletedModeList(self):
		self.game.utilities.log('Select Mode - Update Player Completed Zone List','info')
		self.completedModes = []
		for item in self.allModes:
			if (self.game.utilities.get_player_stats(item) == 1):
				self.completedModes.append(item)

	def setNewActiveMode(self):
		self.game.utilities.log('Select Mode - Set New Active Zones','info')
		#self.activeModes = []
		seed()
		if (len(self.availableModes) <> 0):
			self.newSelectedMode = choice(self.availableModes)
			#self.activeModes.append(self.newSelectedMode)
			#for item in self.activeModes: ### To ensure that player data is up-to-date ###  MAYBE REMOVE...
			self.game.utilities.set_player_stats(self.newSelectedMode,0)
			self.refreshPlayerInfo()

			### Small Lampshow for newly Selected Mode ###
			if (self.newSelectedMode == 'mode1_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='25K POINTS',seconds=4.0,justify='center')
				self.game.lamps.building1.pulse(100)
				self.game.modes.remove(self.game.mode_1)
				self.game.modes.add(self.game.mode_1)
				self.delay(delay=.15,handler=self.game.lamps.building1.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building1.pulse,param=100)
			elif (self.newSelectedMode == 'mode2_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='50K POINTS',seconds=4.0,justify='center')
				self.game.lamps.building2.pulse(100)
				self.game.modes.remove(self.game.mode_2)
				self.game.modes.add(self.game.mode_2)
				self.delay(delay=.15,handler=self.game.lamps.building2.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building2.pulse,param=100)
			elif (self.newSelectedMode == 'mode3_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='100K POINTS',seconds=4.0,justify='center')
				self.game.lamps.building3.pulse(100)
				self.game.modes.remove(self.game.mode_3)
				self.game.modes.add(self.game.mode_3)
				self.delay(delay=.15,handler=self.game.lamps.building3.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building3.pulse,param=100)
			elif (self.newSelectedMode == 'mode4_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='CENTER RAMP 50K',seconds=4.0,justify='center')
				self.game.lamps.building4.pulse(100)
				self.game.modes.remove(self.game.mode_4)
				self.game.modes.add(self.game.mode_4)
				self.delay(delay=.15,handler=self.game.lamps.building4.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building4.pulse,param=100)
			elif (self.newSelectedMode == 'mode5_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='200K POINTS',seconds=4.0,justify='center')
				self.game.lamps.building5.pulse(100)
				self.game.modes.remove(self.game.mode_5)
				self.game.modes.add(self.game.mode_5)
				self.delay(delay=.15,handler=self.game.lamps.building5.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building5.pulse,param=100)
			elif (self.newSelectedMode == 'mode6_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='6K SPINNER',seconds=4.0,justify='center')
				self.game.lamps.building6.pulse(100)
				self.game.modes.remove(self.game.mode_6)
				self.game.modes.add(self.game.mode_6)
				self.delay(delay=.15,handler=self.game.lamps.building6.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building6.pulse,param=100)
			elif (self.newSelectedMode == 'mode7_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='MODE 7',seconds=4.0,justify='center')
				self.game.lamps.building7.pulse(100)
				self.game.modes.remove(self.game.mode_7)
				self.game.modes.add(self.game.mode_7)
				self.delay(delay=.15,handler=self.game.lamps.building7.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building7.pulse,param=100)
			elif (self.newSelectedMode == 'mode8_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='BONUS X',seconds=4.0,justify='center')
				self.game.lamps.building8.pulse(100)
				self.game.modes.remove(self.game.mode_8)
				self.game.modes.add(self.game.mode_8)
				self.delay(delay=.15,handler=self.game.lamps.building8.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building8.pulse,param=100)
			elif (self.newSelectedMode == 'mode9_status'):
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='MODE 9',seconds=4.0,justify='center')
				self.game.lamps.building9.pulse(100)
				self.game.modes.remove(self.game.mode_9)
				self.game.modes.add(self.game.mode_9)
				self.delay(delay=.15,handler=self.game.lamps.building9.pulse,param=100)
				self.delay(delay=.3,handler=self.game.lamps.building9.pulse,param=100)

			self.game.sound.play('mode_selected')
			#self.delay(delay=.15,handler=self.game.sound.play,param='mode_select')
			#self.delay(delay=.3,handler=self.game.sound.play,param='mode_select')
			
			self.delay(delay=.4,handler=self.update_lamps)
			self.delay(delay=.4,handler=self.setModeSelectorActive,param=False)
		else:
			self.update_lamps()

	def setModeSelectorActive(self,activeValue):
		self.modeSelectorActive = activeValue

	def disableBuldingLamps(self):
		self.game.lamps.building1.disable()
		self.game.lamps.building2.disable()
		self.game.lamps.building3.disable()
		self.game.lamps.building4.disable()
		self.game.lamps.building5.disable()
		self.game.lamps.building6.disable()
		self.game.lamps.building7.disable()
		self.game.lamps.building8.disable()
		self.game.lamps.building9.disable()

	def randomModeDisplayer(self):
		if (len(self.availableModes) <> 0):
			seed()
			self.displayMode = choice(self.availableModes)
			if (self.displayMode == 'mode1_status'):
				self.game.lamps.building1.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='25K POINTS',seconds=.3,justify='center')
			elif (self.displayMode == 'mode2_status'):
				self.game.lamps.building2.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='50K POINTS',seconds=.3,justify='center')
			elif (self.displayMode == 'mode3_status'):
				self.game.lamps.building3.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='100K POINTS',seconds=.3,justify='center')
			elif (self.displayMode == 'mode4_status'):
				self.game.lamps.building4.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='CENTER RAMP 50K',seconds=.3,justify='center')
			elif (self.displayMode == 'mode5_status'):
				self.game.lamps.building5.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='200K POINTS',seconds=.3,justify='center')
			elif (self.displayMode == 'mode6_status'):
				self.game.lamps.building6.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='6K SPINNER',seconds=.3,justify='center')
			elif (self.displayMode == 'mode7_status'):
				self.game.lamps.building7.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='MODE 7',seconds=.3,justify='center')
			elif (self.displayMode == 'mode8_status'):
				self.game.lamps.building8.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='BONUS X',seconds=.3,justify='center')
			elif (self.displayMode == 'mode9_status'):
				self.game.lamps.building9.pulse(100)
				self.game.utilities.displayText(199,topText='AWARD SELECTION',bottomText='MODE 9',seconds=.3,justify='center')
			self.game.sound.play('mode_select')
		else:
			pass

	def modeSelector(self):

		if (len(self.availableModes) == 0):
			self.resetPlayerModes()
			self.refreshPlayerInfo()

		### Mode Select Lampshow ###
		if (self.game.utilities.get_player_stats('multiball_running') == False): # Do not disable GI when Multiball is running #
			self.game.utilities.disableGI()
		self.disableBuldingLamps()
		### Loop through Random Modes x10 ###
		for i in range(0, 9):
			self.delayedTime = i / 5.0
			if (self.delayedTime == 0):
				self.randomModeDisplayer()
			else:
				self.delay(delay=self.delayedTime,handler=self.randomModeDisplayer)
		### Select New Active Mode ###
		self.delay(delay=self.delayedTime+.20,handler=self.setNewActiveMode)
		### Launch Ball Back Into Play ###
		self.delay(delay=self.delayedTime+1,handler=self.ejectBall)
		### Update Lamps ###
		self.delay(delay=self.delayedTime+1,handler=self.game.utilities.enableGI)
		self.delay(delay=self.delayedTime+1,handler=self.update_lamps)

	def ballEnteredShelter(self):
		### Scan for Active Ball Locks ###
		if (self.game.multiball_mode.ballLock1Lit == True):
			self.game.multiball_mode.lockBall1()
		elif (self.game.multiball_mode.ballLock2Lit == True):
			self.game.multiball_mode.lockBall2()
		elif (self.game.multiball_mode.ballLock3Lit == True):
			self.game.multiball_mode.startMultiball()
		else:
			if (self.modeSelectorActive == False):
				self.setModeSelectorActive(True)
				self.modeSelector()

	def ejectBall(self):
		self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		self.delay(delay=.2,handler=self.game.sound.play,param='eject')
		self.delay(delay=.5,handler=self.checkForStuckBallInShelter)

	def checkForStuckBallInShelter(self):
		if (self.modeSelectorActive == False):
			if (self.game.switches.ballPopperBottom.is_active() == True):
				self.ejectBall()

	def sw_underPlayfieldDrop1_active(self, sw):
		self.ballEnteredShelter()
		self.enterSwitch1Triggered = True
		return procgame.game.SwitchStop

	def sw_underPlayfieldDrop2_active(self, sw):
		if self.enterSwitch1Triggered == False:
			self.ballEnteredShelter()
			### Throw Operator Message ###
		self.enterSwitch2Triggered = True
		return procgame.game.SwitchStop

	def sw_ballPopperBottom_closed_for_200ms(self, sw):
		### Check for broken Shelter switches ###
		if (self.enterSwitch1Triggered == False or self.enterSwitch2Triggered == False):
			pass
			### Throw Operator Message ###

		### Handle ball locking if both switches are broken ###
		if (self.enterSwitch1Triggered == False and self.enterSwitch2Triggered == False):
			self.ballEnteredShelter()

		### Reset Switch Monitors ###
		self.enterSwitch1Triggered = False
		self.enterSwitch2Triggered = False

		if(self.game.multiball_mode.multiballStarting == True):
			### Multiball is Starting, let that function handle ball kickouts ###
			return procgame.game.SwitchStop
		else:
			### Multiball is NOT Starting ###
			if (self.modeSelectorActive == False):
				self.ejectBall()
			#self.game.utilities.score(250)
			return procgame.game.SwitchContinue