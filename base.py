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
##     ____  ___   _____ ______   __  _______  ____  ______
##    / __ )/   | / ___// ____/  /  |/  / __ \/ __ \/ ____/
##   / __  / /| | \__ \/ __/    / /|_/ / / / / / / / __/   
##  / /_/ / ___ |___/ / /___   / /  / / /_/ / /_/ / /___   
## /_____/_/  |_/____/_____/  /_/  /_/\____/_____/_____/    
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc 
import random
import time
import sys
#import scoredisplay
#from scoredisplay import *
import attract
from attract import *
import skillshot
from skillshot import SkillshotMode

class BaseGameMode(game.Mode):
	def __init__(self, game):
			super(BaseGameMode, self).__init__(game=game, priority=2)
			
	def mode_started(self):
			#Start Attract Mode
			self.attract_mode = AttractMode(self.game)
			self.game.modes.add(self.attract_mode)
			self.checkForStuckBalls()

	###############################################################
	# UTILITY FUNCTIONS
	###############################################################
	def troughIsFull(self): #should be moved globally
		if (self.game.switches.trough1.is_active()==True and self.game.switches.trough2.is_active()==True and self.game.switches.trough3.is_active()==True):
			return True
		else:
			return False

	def checkForStuckBalls(self):
		#Checks for balls in locks or outhole and kicks them out
		if self.game.switches.outhole.is_active()==True:
			self.coilPulse(coilname='outholeKicker_CaptiveFlashers',pulsetime=50)
		if self.game.switches.ejectHole5.is_active()==True:
			self.coilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		if self.game.switches.ballPopperBottom.is_active()==True:
			self.coilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		if self.game.switches.ballPopperTop.is_active()==True:
			self.game.coils.topBallPopper.pulse(50) #Does not need AC Relay logic

	def coilPulse(self,coilname,pulsetime):
		self.acselecttime = .2
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()
		self.delay(name='coilDelay',event_type=None,delay=self.acselecttime,handler=self.game.coils[coilname].pulse,param=pulsetime)
		self.delay(name='acEnableDelay',delay=1,handler=self.game.coils.acSelect.enable)

	def score(self, points):
		self.p = self.game.current_player()
		self.p.score += points
		self.cancel_delayed('updatescore')
		self.delay(name='updatescore',delay=0.5,handler=self.update_display)

	def queueGameStartModes(self):
		#Skillshot Mode
		skillshot_mode = SkillshotMode(self.game)
		self.game.modes.add(skillshot_mode)

	def launch_ball(self):
		self.game.score_display.set_text("LAUNCH TEST",0)
		self.game.coils.autoLauncher.pulse(100)

	def update_display(self):
		self.p = self.game.current_player()
		self.game.score_display.set_text(str(self.p.score),0)
		self.game.score_display.set_text("Ball "+str(self.game.ball),1,justify='right')
		
	###############################################################
	# MAIN GAME HANDLING FUNCTIONS
	###############################################################
	def start_game(self):
		#This function is to be used when starting a new game, player 1 and ball 1

		#Clean Up
		self.game.modes.remove(self.attract_mode)
		
		self.game.add_player() #will be first player at this point
		self.game.ball = 1
		
		#Reset Player Score - Might not be needed
		self.p = self.game.current_player()
		self.p.score = 0

		self.queueGameStartModes()
		self.start_ball()
		self.update_display()
		#self.game.sound.load_music('main')
		#print gameMusicPath+'twerk.wav'
		
	def start_ball(self):
		self.coilPulse(coilname='ballReleaseShooterLane_CenterRampFlashers1',pulsetime=50)
		
	def end_ball(self):
		self.game.ball += 1

	def end_game(self):
		self.game.ball = 0
		self.game.coils.flipperEnable.disable()

		#disable AC Relay
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()

		self.game.modes.add(self.attract_mode)
		self.game.sound.fadeout_music(time_ms=450)

	###############################################################
	# BASE SWITCH HANDLING FUNCTIONS
	###############################################################		
	def sw_instituteDown_closed(self, sw):
		self.game.coils.quakeInstitute.disable()
		return procgame.game.SwitchStop
		
	def sw_startButton_active_for_20ms(self, sw):
		print 'Player: ' + str(self.game.players.index)
		print 'Ball' + str(self.game.ball)
		if self.troughIsFull()==True:
			#Trough is full!
			if self.game.ball == 0:
				#########################
				#Start Game
				#########################
				self.start_game()
				#self.game.sound.play_music('main')
				self.delay(name='lauchball',delay=2,handler=self.launch_ball)
			elif self.game.ball == 1 and len(self.game.players) < 4:
				self.game.add_player()
			else:
				pass
			#Enable Flippers
			self.game.coils.flipperEnable.enable()
		else:
			self.checkForStuckBalls()
			self.game.score_display.set_text("Missing Pinballs",0)
			self.game.score_display.set_text("Please Wait",1)
		return procgame.game.SwitchStop

	def sw_startButton_active_for_1s(self, sw):
		#will put launcher in here eventually
		pass
		
	def sw_outhole_closed_for_1s(self, sw):
		self.coilPulse(coilname='outholeKicker_CaptiveFlashers',pulsetime=50)
		if self.game.ball == self.game.balls_per_game:
			self.end_game()
		return procgame.game.SwitchStop

	def sw_ejectHole5_closed_for_1s(self, sw):
		self.coilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		self.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperBottom_closed_for_1s(self, sw):
		self.coilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		self.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperTop_closed_for_1s(self, sw):
		self.game.coils.topBallPopper.pulse(50)
		self.game.coils.quakeMotor.pulse(50)
		self.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperTop_closed(self, sw):
		self.game.coils.quakeMotor.pulse(100)
		self.game.coils.quakeInstitute.enable()
		self.score(250)
		return procgame.game.SwitchStop

	def sw_jetLeft_active(self, sw):
		self.game.coils.jetLeft.pulse(30)
		self.game.lamps.jetLeftLamp.enable()
		self.score(50)
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		self.game.coils.jetRight.pulse(30)
		self.game.lamps.jetRightLamp.enable()
		self.score(50)
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		self.game.coils.jetTop.pulse(30)
		self.game.lamps.jetTopLamp.enable()
		self.score(50)
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		self.game.coils.slingL.pulse(30)
		self.score(100)
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		self.game.coils.slingR.pulse(30)
		self.score(100)
		return procgame.game.SwitchStop

	def sw_spinner_active(self, sw):
		self.game.coils.dropReset_CenterRampFlashers2.pulse(50)
		self.game.sound.play_voice('spinner')
		self.score(100)
		return procgame.game.SwitchStop

	#############################
	# Zone Switches
	#############################
	def sw_leftStandup1_closed(self, sw):
		self.game.lamps.standupLeft1.enable()
		self.game.lamps.building1.enable()
		self.score(250)
		return procgame.game.SwitchStop

	def sw_rightStandupHigh2_closed(self, sw):
		self.game.lamps.standupRightHigh2.enable()
		self.game.lamps.building2.enable()
		self.score(250)
		return procgame.game.SwitchStop

	def sw_rightStandupLow3_closed(self, sw):
		self.game.lamps.standupRightLow3.enable()
		self.game.lamps.building3.enable()
		self.score(250)
		return procgame.game.SwitchStop
		
	def sw_centerStandup4_closed(self, sw):
		self.game.lamps.standupCenter4.enable()
		self.game.lamps.building4.enable()
		self.score(250)
		return procgame.game.SwitchStop
		
	def sw_ejectHole5_closed(self, sw):
		self.game.lamps.ejectTop5.enable()
		self.game.lamps.building5.enable()
		self.score(250)
		return procgame.game.SwitchStop
		
	def sw_rightLoop6_closed(self, sw):
		self.game.lamps.underFaultLoop6.enable()
		self.game.lamps.building6.enable()
		self.score(250)
		return procgame.game.SwitchStop
		
	def sw_rightInsideReturn7_closed(self, sw):
		self.game.lamps.inlaneRight7.enable()
		self.game.lamps.building7.enable()
		self.score(250)
		return procgame.game.SwitchStop
		
	def sw_leftReturnLane8_closed(self, sw):
		self.game.lamps.inlaneLeft8.enable()
		self.game.lamps.building8.enable()
		self.score(250)
		return procgame.game.SwitchStop
		
	def sw_captiveBall9_closed(self, sw):
		self.game.lamps.captiveArrow9.enable()
		self.game.lamps.building9.enable()
		self.score(250)
		return procgame.game.SwitchStop