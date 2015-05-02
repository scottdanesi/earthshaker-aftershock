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
##    __  ______________    _________________________
##   / / / /_  __/  _/ /   /  _/_  __/  _/ ____/ ___/
##  / / / / / /  / // /    / /  / /  / // __/  \__ \ 
## / /_/ / / / _/ // /____/ /  / / _/ // /___ ___/ / 
## \____/ /_/ /___/_____/___/ /_/ /___/_____//____/  
## 
## This mode will be used to house all the global functions that will be used
## throughout the Aftershock project.
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

class UtilitiesMode(game.Mode):
	def __init__(self, game, priority):
			super(UtilitiesMode, self).__init__(game, priority)
			##############################
			#### Set Global Variables ####
			##############################
			self.currentDisplayPriority = 0	
			self.randomLampPulseCount = 0
			self.randomRGBPulseCount = 0
			self.ACCoilInProgress = False
			self.ACNameArray = []
			self.ACNameArray.append('outholeKicker_CaptiveFlashers')
			self.ACNameArray.append('ballReleaseShooterLane_CenterRampFlashers1')
			self.ACNameArray.append('dropReset_CenterRampFlashers2')
			self.ACNameArray.append('californiaFault_CenterRampFlashers3')
			self.ACNameArray.append('ejectHole_CenterRampFlashers4')
			self.ACNameArray.append('bottomBallPopper_RightRampFlashers1')
			self.ACNameArray.append('knocker_RightRampFlashers2')

			self.displayWithInfoFlag = False

	def mode_started(self):
		self.baseDisplayTicker()

	def mode_stopped(self):
		self.cancel_delayed('displayTicker')


	#######################
	#### Log Functions ####
	#######################
	def log(self,text,level='info'):
		if (level == 'error'):
			pass
			#logging.error(text)
		elif (level == 'warning'):
			pass
			#logging.warning(text)
		else:
			pass
			#logging.info(text)
		#print level + " - " + text


	#################################
	#### Ball Location Functions ####
	#################################
	def troughIsFull(self): #should be moved globally
		if (self.game.switches.trough1.is_active()==True and self.game.switches.trough2.is_active()==True and self.game.switches.trough3.is_active()==True):
			return True
		else:
			return False

	def releaseStuckBalls(self):
		#Checks for balls in locks or outhole and kicks them out
		if self.game.switches.outhole.is_active()==True and self.game.tiltStatus == 0: #Exception for when in tilt
			self.game.utilities.acCoilPulse(coilname='outholeKicker_CaptiveFlashers',pulsetime=50)
		if self.game.switches.ejectHole5.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		if self.game.switches.ballPopperBottom.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		if self.game.switches.ballPopperTop.is_active()==True:
			self.game.coils.topBallPopper.pulse(50) #Does not need AC Relay logic
		if self.game.switches.ballShooter.is_active()==True:
			self.game.coils.autoLauncher.pulse(100) #Does not need AC Relay logic
		#self.game.coils.quakeInstitute.enable()

	def executeBallSearch(self):
		delayTime = .7
		self.game.coils.quakeInstitute.enable()
		self.acCoilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		#self.delay(delay=delayTime*1,handler=self.game.coils.jetLeft.pulse,param=50)
		#self.delay(delay=delayTime*2,handler=self.game.coils.jetRight.pulse,param=50)
		#self.delay(delay=delayTime*3,handler=self.game.coils.jetTop.pulse,param=50)
		self.delay(delay=delayTime*3,handler=self.acCoilPulse,param='bottomBallPopper_RightRampFlashers1')
		#self.delay(delay=delayTime*5,handler=self.game.coils.slingL.pulse,param=50)
		#self.delay(delay=delayTime*6,handler=self.game.coils.slingR.pulse,param=50)
		self.delay(delay=delayTime*1,handler=self.game.coils.topBallPopper.pulse,param=50)
		self.delay(delay=delayTime*2,handler=self.game.coils.autoLauncher.pulse,param=100)
		self.delay(delay=delayTime*4,handler=self.game.update_lamps)

	def launch_ball(self):
		if self.game.switches.ballShooter.is_active()==True:
			self.game.coils.autoLauncher.pulse(100)

	def setBallInPlay(self,ballInPlay=True):
		self.previousBallInPlay = self.get_player_stats('ball_in_play')
		if (ballInPlay == True and self.previousBallInPlay == False):
			self.set_player_stats('ball_in_play',True)
			self.stopShooterLaneMusic()
		elif (ballInPlay == False and self.previousBallInPlay == True):
			self.set_player_stats('ball_in_play',False)

	############################
	#### AC Relay Functions ####
	############################
	def ACRelayEnable(self):
		self.game.coils.acSelect.enable()
		self.ACCoilInProgress = False

	def acCoilPulse(self,coilname,pulsetime=50):
		### Setup variables ###
		self.ACCoilInProgress = True
		self.acSelectTimeBuffer = .3
		self.acSelectEnableBuffer = (pulsetime/1000)+(self.acSelectTimeBuffer*2)
		self.updateLampsBuffer = self.acSelectEnableBuffer + .2

		### Remove any scheduling of the AC coils ###
		for item in self.ACNameArray:
			self.game.coils[item].disable()

		### Stop any flashlamp lampshows
		self.game.lampctrlflash.stop_show()

		### Start the pulse process ###
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()
		self.delay(name='coilDelay',event_type=None,delay=self.acSelectTimeBuffer,handler=self.game.coils[coilname].pulse,param=pulsetime)
		self.delay(name='acEnableDelay',delay=self.acSelectEnableBuffer,handler=self.ACRelayEnable)

		### Update lamps since some of the flashers may have been disabled ###
		self.delay(delay=self.updateLampsBuffer,handler=self.game.update_lamps)

	def acFlashPulse(self,coilname,pulsetime=50):
		if (self.ACCoilInProgress == False or coilname not in self.ACNameArray):
			self.game.coils[coilname].pulse(pulsetime)
		else:
			#Should this try again or just cancel?
			#cannot since the delay function does not allow me to pass more than 1 parameter :(
			pass

	def acFlashSchedule(self,coilname,schedule,cycle_seconds,now=True):
		if (self.ACCoilInProgress == False or coilname not in self.ACNameArray):
			self.game.coils[coilname].disable()
			self.game.coils[coilname].schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)
		else:
			#Should this try again or just cancel?
			#cannot since the delay function does not allow me to pass more than 1 parameter :(
			pass

	
	###########################
	#### Display Functions ####
	###########################

	def displayText(self,priority,topText=' ',bottomText=' ',seconds=2,justify='left',topBlinkRate=0,bottomBlinkRate=0):
		# This function will be used as a very basic display prioritizing helper
		# Check if anything with a higher priority is running
		if (priority >= self.currentDisplayPriority):
			self.cancel_delayed('resetDisplayPriority')
			self.game.alpha_score_display.cancel_script()
			self.game.alpha_score_display.set_text(topText,0,justify)
			self.game.alpha_score_display.set_text(bottomText,1,justify)
			if seconds > 0:
				self.delay(name='resetDisplayPriority',event_type=None,delay=seconds,handler=self.resetDisplayPriority)
			self.currentDisplayPriority = priority

	def resetDisplayPriority(self):
		self.currentDisplayPriority = 0
		self.updateBaseDisplay()

	def updateBaseDisplay(self):
		print "Update Base Display Called"
		if (self.currentDisplayPriority == 0 and self.game.tiltStatus == 0 and self.game.ball <> 0):

			self.player1Score = ''
			self.player2Score = ''
			self.player3Score = ''
			self.player4Score = ''

			self.player1ScoreFormatted = ''
			self.player2ScoreFormatted = ''
			self.player3ScoreFormatted = ''
			self.player4ScoreFormatted = ''

			self.currentNumPlayers = len(self.game.players)
			if (self.currentNumPlayers > 0):
				self.player1Score = self.game.players[0].score
			if (self.currentNumPlayers > 1):
				self.player2Score = self.game.players[1].score
			if (self.currentNumPlayers > 2):
				self.player3Score = self.game.players[2].score
			if (self.currentNumPlayers > 3):
				self.player4Score = self.game.players[3].score

			if (self.player1Score <> ''):
				self.player1ScoreFormatted = str(locale.format("%d", self.player1Score, grouping=True))
			if (self.player2Score <> ''):
				self.player2ScoreFormatted = str(locale.format("%d", self.player2Score, grouping=True))
			if (self.player3Score <> ''):
				self.player3ScoreFormatted = str(locale.format("%d", self.player3Score, grouping=True))
			if (self.player4Score <> ''):
				self.player4ScoreFormatted = str(locale.format("%d", self.player4Score, grouping=True))
			
			if (self.displayWithInfoFlag):
				self.displayWithInfo()
			else:
				self.displayWithPlayers()

	def displayWithInfo(self):
		self.p = self.game.current_player()

		#Top Line#
		if(self.p.name.upper() == 'PLAYER 1'):
			self.topScoresText = self.player1ScoreFormatted
			self.game.alpha_score_display.set_text(self.topScoresText,0,justify='left')
		elif(self.p.name.upper() == 'PLAYER 2'):
			self.topScoresText = self.player2ScoreFormatted
			self.game.alpha_score_display.set_text(self.topScoresText,0,justify='right')
		else:
			self.game.alpha_score_display.set_text(self.p.name.upper() + "  BALL "+str(self.game.ball),0,justify='left')

		#Bottom Line#
		if(self.p.name.upper() == 'PLAYER 3'):
			self.bottomScoresText = self.player3ScoreFormatted
			self.game.alpha_score_display.set_text(self.bottomScoresText,1,justify='left')
		elif(self.p.name.upper() == 'PLAYER 4'):
			self.bottomScoresText = self.player4ScoreFormatted
			self.game.alpha_score_display.set_text(self.bottomScoresText,1,justify='right')
		else:
			self.game.alpha_score_display.set_text(self.p.name.upper() + "  BALL "+str(self.game.ball),1,justify='left')

	def displayWithPlayers(self):

		self.scoreSpaceCount = 16 - (len(str(self.player1Score)) + len(str(self.player2Score)))
		if self.scoreSpaceCount < 0: # Just in case scores get very large (over 8 characters each)
			self.scoreSpaceCount = 0
		self.topScoresText = self.player1ScoreFormatted
		for i in range (0,self.scoreSpaceCount): # Puts a space between the scores for i places
			self.topScoresText += ' ' 
		self.topScoresText += self.player2ScoreFormatted # Add the score to the end

		# Set Bottom Text
		self.scoreSpaceCount = 16 - (len(str(self.player3Score)) + len(str(self.player4Score)))
		if self.scoreSpaceCount < 0: # Just in case scores get very large (over 8 characters each)
			self.scoreSpaceCount = 0
		self.bottomScoresText = self.player3ScoreFormatted
		for i in range (0,self.scoreSpaceCount):
			self.bottomScoresText += ' '
		self.bottomScoresText += self.player4ScoreFormatted

		self.game.alpha_score_display.set_text(self.topScoresText,0,justify='left')
		self.game.alpha_score_display.set_text(self.bottomScoresText,1,justify='left')
	
	def baseDisplayTicker(self):
		self.displayWithInfoFlag = not self.displayWithInfoFlag
		self.delay(name='displayTicker',delay=3,handler=self.baseDisplayTicker)
		self.updateBaseDisplay()

	def validateCurrentPlayer(self):
		### This function is to verify that the player has initiated fully ###
		self.p = self.game.current_player()
		if (self.p.name.upper() == 'PLAYER 1' or self.p.name.upper() == 'PLAYER 2' or self.p.name.upper() == 'PLAYER 3' or self.p.name.upper() == 'PLAYER 4'):
			return True
		else:
			return False
	
	######################
	#### GI Functions ####
	######################
	def disableGI(self):
		self.game.coils.giUpper.enable()
		self.game.coils.giLower.enable()
		self.game.coils.giBackbox.enable()

	def enableGI(self):
		self.game.coils.giUpper.disable()
		self.game.coils.giLower.disable()
		self.game.coils.giBackbox.disable()

	############################
	#### Lighting Functions ####
	############################

	def randomLampPulse(self, numPulses):
		randomInt = randint(1,64)
		i = 1
		for lamp in self.game.lamps:
			if randomInt == i:
				lamp.pulse(200)
			i += 1
		self.randomLampPulseCount += 1
		if (self.randomLampPulseCount <= numPulses):
			self.delay(delay=.1,handler=self.randomLampPulse,param=numPulses)
		else:
			self.randomLampPulseCount = 0

	def randomBackboxPulse(self, numPulses):
		randomIntRed = randint(0,255)
		randomIntGreen = randint(0,255)
		randomIntBlue = randint(0,255)
				
		self.setBackboxLED(r=randomIntRed,g=randomIntGreen,b=randomIntBlue,pulsetime=100)

		self.randomRGBPulseCount += 1
		if (self.randomRGBPulseCount <= numPulses):
			self.delay(delay=.2,handler=self.randomBackboxPulse,param=numPulses)
		else:
			self.randomRGBPulseCount = 0



	###################################
	#### Music and Sound Functions ####
	###################################
	def stopShooterLaneMusic(self):
		if (self.game.shooter_lane_status == 1):
			self.game.sound.stop_music()
			self.game.sound.play_music('main',loops=-1,music_volume=.5)
			self.game.shooter_lane_status = 0


	##########################
	#### Player Functions ####
	##########################
	def set_player_stats(self,id,value):
		if (self.game.ball <> 0):
			self.p = self.game.current_player()
			self.p.player_stats[id]=value

	def get_player_stats(self,id):
		if (self.game.ball <> 0):
			self.p = self.game.current_player()
			return self.p.player_stats[id]
		else:
			return False

	def score(self, points):
		if (self.game.ball <> 0): #in case score() gets called when not in game
			self.p = self.game.current_player()
			self.p.score += points
			# Update the base display with the current players score
			self.cancel_delayed('updatescore')
			self.delay(name='updatescore',delay=0.05,handler=self.game.utilities.updateBaseDisplay)	

	def currentPlayerScore(self):
		if (self.game.ball <> 0): #in case score() gets called when not in game
			self.p = self.game.current_player()
			return self.p.score
		else:
			return 0
			
	def setDiagLED(self, player_num):
		if (player_num == 1):
			### Player 1 ###
			self.game.coils.diagLED.schedule(schedule=0x0000000F, cycle_seconds=0, now=False)
		elif (player_num == 2):
			### Player 2 ###
			self.game.coils.diagLED.schedule(schedule=0x00000F0F, cycle_seconds=0, now=False)
		elif (player_num == 3):
			### Player 2 ###
			self.game.coils.diagLED.schedule(schedule=0x000F0F0F, cycle_seconds=0, now=False)
		elif (player_num == 4):
			### Player 2 ###
			self.game.coils.diagLED.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)
		elif (player_num == 0):
			### Player 2 ###
			self.game.coils.diagLED.schedule(schedule=0x33333333, cycle_seconds=0, now=False)
		elif (player_num == -1):
			### Player 2 ###
			self.game.coils.diagLED.disable

	##########################
	#### Shaker Functions ####
	##########################
	def shakerPulseLow(self):
		self.game.coils.quakeMotor.pulsed_patter(on_time=5,off_time=25,run_time=255)
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			self.delay(delay=.255,handler=self.enableMultiballQuake)

	def shakerPulseMedium(self):
		self.game.coils.quakeMotor.pulsed_patter(on_time=15,off_time=15,run_time=255)
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			self.delay(delay=.255,handler=self.enableMultiballQuake)

	def shakerPulseHigh(self):
		self.game.coils.quakeMotor.pulse(255)
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			self.delay(delay=.255,handler=self.enableMultiballQuake)

	def enableMultiballQuake(self):
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			self.game.coils.quakeMotor.patter(on_time=15,off_time=100)

	###############################
	#### Backbox LED Functions ####
	###############################
	def setBackboxLED(self,r=0,g=0,b=0,pulsetime=0,schedule=0x00000000):
		#Global Constants
		self.totalResolutionMS = 10
		self.divisor = 255 / self.totalResolutionMS
		#Check for Reset
		if(r==0 and g==0 and b==0):
			self.game.coils.backboxLightingR.disable()
			self.game.coils.backboxLightingG.disable()
			self.game.coils.backboxLightingB.disable()
			return
		#RED Color Evaluation
		self.rOn = math.floor(r/self.divisor)
		self.rOff = self.totalResolutionMS - self.rOn
		if(self.rOn == self.totalResolutionMS):
			if(pulsetime == 0):
				self.game.coils.backboxLightingR.enable()
			else:
				self.game.coils.backboxLightingR.pulse(pulsetime)
		elif(self.rOn == 0):
			self.game.coils.backboxLightingR.disable()
		else:
			if(pulsetime == 0):
				self.game.coils.backboxLightingR.patter(self.rOn,self.rOff)
			else:
				self.game.coils.backboxLightingR.pulsed_patter(self.rOn,self.rOff,run_time=pulsetime)
		#GREEN Color Evaluation
		self.gOn = math.floor(g/self.divisor)
		self.gOff = self.totalResolutionMS - self.gOn
		if(self.gOn == self.totalResolutionMS):
			if(pulsetime == 0):
				self.game.coils.backboxLightingG.enable()
			else:
				self.game.coils.backboxLightingG.pulse(pulsetime)
		elif(self.gOn == 0):
			self.game.coils.backboxLightingG.disable()
		else:
			if(pulsetime == 0):
				self.game.coils.backboxLightingG.patter(self.gOn,self.gOff)
			else:
				self.game.coils.backboxLightingG.pulsed_patter(self.gOn,self.gOff,run_time=pulsetime)
		#BLUE Color Evaluation
		self.bOn = math.floor(b/self.divisor)
		self.bOff = self.totalResolutionMS - self.bOn
		if(self.bOn == self.totalResolutionMS):
			if(pulsetime == 0):
				self.game.coils.backboxLightingB.enable()
			else:
				self.game.coils.backboxLightingB.pulse(pulsetime)
		elif(self.bOn == 0):
			self.game.coils.backboxLightingB.disable()
		else:
			if(pulsetime == 0):
				self.game.coils.backboxLightingB.patter(self.bOn,self.bOff)
			else:
				self.game.coils.backboxLightingB.pulsed_patter(self.bOn,self.bOff,run_time=pulsetime)


