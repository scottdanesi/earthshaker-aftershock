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
##   ____________  ______
##  /_  __/  _/ / /_  __/
##   / /  / // /   / /   
##  / / _/ // /___/ /    
## /_/ /___/_____/_/     
## 
##	To Do:
##		Stop all switches in lower priority modes
#################################################################################

import procgame.game
from procgame import *
import pinproc


class Tilt(game.Mode):
	def __init__(self, game, priority):
			super(Tilt, self).__init__(game, priority)
			#Get number of tilt warnings - Hardcoded for now
			self.game.tiltWarnings = 2

	def mode_started(self):
		self.reset()

	def reset(self):
		self.game.tiltStatus = 0
		self.game.times_warned = 0
		self.game.allowWarnings = True

	def disableAllBallModes(self):
		#### Remove Ball Modes ####
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.modes.remove(self.game.centerramp_mode)
		self.game.modes.remove(self.game.ballsaver_mode)
		self.game.modes.remove(self.game.drops_mode)
		self.game.modes.remove(self.game.collect_mode)
		self.game.modes.remove(self.game.spinner_mode)
		self.game.modes.remove(self.game.multiball_mode)

	def playTiltSounds(self):
		self.game.sound.play('tilt_fx')
		self.delay(name='tiltVoice',delay=.5,handler=self.game.sound.play_voice,param='tilt_vox')

	def playWarningSounds(self):
		self.game.sound.play_voice('warning_vox')

	def warning(self):
		self.game.times_warned += 1
		#Need to Play sound here
		self.playWarningSounds()

		#Flash GI - Not using schedule
		self.flashDelay = .1 #used for the delay between GI flashes
		self.flashDelayGap = .1
		self.game.utilities.disableGI()
		self.delay(name='reenableGI',delay=self.flashDelay,handler=self.game.utilities.enableGI)
		self.delay(name='disableGI',delay=(self.flashDelay*2)+self.flashDelayGap,handler=self.game.utilities.disableGI)
		self.delay(name='reenableGI',delay=(self.flashDelay*3)+self.flashDelayGap,handler=self.game.utilities.enableGI)

		#### Update Audits ####
		#self.game.game_data['Audits']['Warnings'] += 1
		#self.game.save_game_data()

		#Update Display
		time=2
		self.game.utilities.displayText(200,topText='WARNING '+str(self.game.times_warned)+'/'+str(self.game.tiltWarnings),bottomText=' ',seconds=time,justify='center',topBlinkRate=1)

	def tilt(self):
		#check if already in a tilt state
		if self.game.tiltStatus == 0:
			self.game.tiltStatus = 1

			self.game.sound.stop_music()

			#Remove all ball modes
			self.disableAllBallModes()

			#Update Display
			#######################################################################
			## This Tilt message will stay on until the ball ends since it       ##
			## will not allow other messages with lower priority to be displayed ##
			## until the start of a new ball when the tilt status resets.        ##
			#######################################################################
			self.game.utilities.displayText(200,topText='TILT',bottomText=' ',seconds=1,justify='center')

			#### Disable Bumpers ####
			self.game.coils.flipperEnable.disable()

			#### Disable Bumpers ####
			self.game.enable_bumpers(enable=False)

			#self.game.utilities.releaseStuckBalls()

			#turn off all lamps
			for lamp in self.game.lamps:
				lamp.disable()

			#Disable GI
			self.game.utilities.disableGI()

			#Stop Music
			self.game.sound.stop_music()

			#Play Sounds
			self.playTiltSounds()

			#Need to release stuck balls
			self.game.utilities.releaseStuckBalls()

			#### Update Audits ####
			#self.game.game_data['Audits']['Tilts'] += 1
			#self.game.save_game_data()

			#Wait for balls to empty
				#self.waitUntilTroughIsFull()

	def waitUntilTroughIsFull(self):
		if (self.game.utilities.troughIsFull() == False):
			self.game.utilities.releaseStuckBalls()
			self.delay(name='waitForTrough',delay=2,handler=self.waitUntilTroughIsFull)
		else:
			self.game.utilities.displayText(200,topText='TILT',bottomText=' ',seconds=1,justify='center')

	def resetWarningBuffer(self):
		self.game.allowWarnings = True

	def sw_tilt_active(self, sw):
		self.tiltBuffer = .5 #need to add logic for this
		if (self.game.times_warned >= self.game.tiltWarnings and self.game.allowWarnings == True):
			self.tilt()
			#self.game.allowWarnings = 0
			#self.delay(name='resetwarningbuffer',delay=self.tiltBuffer,handler=self.resetWarningBuffer)
		elif(self.game.allowWarnings == True):
			self.warning()
			self.game.allowWarnings = False
			self.delay(name='resetwarningbuffer',delay=self.tiltBuffer,handler=self.resetWarningBuffer)


