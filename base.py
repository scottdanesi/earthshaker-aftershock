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
import scoredisplay
from scoredisplay import *
import attract
from attract import *
import skillshot
from skillshot import SkillshotMode

#################################
## GLOBAL VARIABLES
#################################


#################################
## SYSTEM VARIABLES
#################################


class BaseGameMode(game.Mode):
	def __init__(self, game):
			super(BaseGameMode, self).__init__(game=game, priority=6)
			#self.score_display = AlphaScoreDisplay(self.game,0)
			#Start Attract Mode
			#self.attract_mode = AttractMode(self.game)
			#self.game.modes.add(self.attract_mode)

	def mode_started(self):
			self.score_display = AlphaScoreDisplay(self.game,0)
			#Start Attract Mode
			self.attract_mode = AttractMode(self.game)
			self.game.modes.add(self.attract_mode)
			self.checkForStuckBalls()

	def troughIsFull(self): #should be moved globally
		if (self.game.switches.trough1.is_active()==True and self.game.switches.trough2.is_active()==True and self.game.switches.trough3.is_active()==True):
			return True
		else:
			return False

	def checkForStuckBalls(self):
		if self.game.switches.outhole.is_active()==True:
			self.game.coils.acSelect.disable()
			self.game.coils.outholeKicker_CaptiveFlashers.pulse(50)
		if self.game.switches.ejectHole5.is_active()==True:
			self.game.coils.acSelect.disable()
			self.game.coils.ejectHole_CenterRampFlashers4.pulse(50)
		if self.game.switches.ballPopperBottom.is_active()==True:
			self.game.coils.acSelect.disable()
			self.game.coils.bottomBallPopper_RightRampFlashers1.pulse(50)
		if self.game.switches.ballPopperTop.is_active()==True:
			self.game.coils.topBallPopper.pulse(50)

	def score(self, points):
		"""Convenience method to add *points* to the current player."""
		p = self.game.current_player()
		p.score += points
		self.cancel_delayed('updatescore')
		self.delay(name='updatescore',delay=0.5,handler=self.update_display)

	def queueModes(self):
		skillshot_mode = SkillshotMode(self.game)
		self.game.modes.add(skillshot_mode)
		
	def start_game(self):
		self.game.modes.remove(self.attract_mode)
		for lamp in self.game.lamps:
			lamp.disable()
		#self.game.ball_starting()
		self.game.add_player()
		self.p = self.game.current_player()
		self.game.ball = 1
		self.p.score = 0
		#self.start_ball()
		self.game.coils.ballReleaseShooterLane_CenterRampFlashers1.pulse(50)
		self.queueModes()
		self.update_display()

	def end_game(self):
		self.game.ball = 0
		self.game.coils.flipperEnable.disable()
		self.game.modes.add(self.attract_mode)

	def update_display(self):
		self.p = self.game.current_player()
		self.score_display.set_text(str(self.p.score),0)
		self.score_display.set_text("Ball "+str(self.game.ball),1)

	def sw_instituteDown_closed(self, sw):
		self.game.coils.quakeInstitute.disable()
		return procgame.game.SwitchStop
		
	def sw_startButton_active_for_20ms(self, sw):
		print self.game.ball
		if self.troughIsFull()==True:
			#Trough is full!
			if self.game.ball == 0:
				#########################
				#Start Game
				#########################
				self.start_game()
			elif self.game.ball == 1 and len(self.game.players) < 4:
				self.game.add_player()
			else:
				pass
			#Enable Flippers
			self.game.coils.flipperEnable.enable()
		else:
			self.checkForStuckBalls()
			self.score_display.set_text("Missing Pinballs",0,seconds=1)
			self.score_display.set_text("Please Wait",1,seconds=1)
		return procgame.game.SwitchStop
		

	def sw_outhole_closed_for_1s(self, sw):
		#self.attract_mode = AttractMode(game)
		self.game.coils.acSelect.disable()
		self.game.coils.outholeKicker_CaptiveFlashers.pulse(50)
		#self.game.modes.add(self.attract_mode)
		#self.game.modes.remove(basic_mode)
		self.end_game()
		return procgame.game.SwitchStop

	def sw_ejectHole5_closed_for_1s(self, sw):
		self.game.coils.acSelect.disable()
		self.game.coils.ejectHole_CenterRampFlashers4.pulse(50)
		#self.game.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperBottom_closed_for_1s(self, sw):
		self.game.coils.acSelect.disable()
		self.game.coils.bottomBallPopper_RightRampFlashers1.pulse(50)
		#self.game.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperTop_closed_for_1s(self, sw):
		self.game.coils.topBallPopper.pulse(50)
		self.game.coils.quakeMotor.pulse(100)
		#self.game.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperTop_closed(self, sw):
		self.game.coils.quakeMotor.pulse(100)
		self.game.coils.quakeInstitute.enable()
		#self.game.score(250)
		return procgame.game.SwitchStop

	def sw_jetLeftSwitch_active(self, sw):
		self.game.coils.jetLeftCoil.pulse(30)
		self.game.lamps.jetLeftLamp.enable()
		self.score(50)
		return procgame.game.SwitchStop

	def sw_jetRightSwitch_active(self, sw):
		self.game.coils.jetRightCoil.pulse(30)
		self.game.lamps.jetRightLamp.enable()
		self.score(50)
		return procgame.game.SwitchStop

	def sw_jetTopSwitch_active(self, sw):
		self.game.coils.jetTopCoil.pulse(30)
		self.game.lamps.jetTopLamp.enable()
		self.score(50)
		return procgame.game.SwitchStop

	def sw_slingLeftSwitch_active(self, sw):
		self.game.coils.slingLeftCoil.pulse(30)
		self.score(100)
		return procgame.game.SwitchStop

	def sw_slingRightSwitch_active(self, sw):
		self.game.coils.slingRightCoil.pulse(30)
		self.score(100)
		return procgame.game.SwitchStop

	def sw_spinner_active(self, sw):
		self.game.lamps.spinner.pulse(30)
		#game.coils.acSelect.disable()
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