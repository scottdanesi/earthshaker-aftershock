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
import locale

class BaseGameMode(game.Mode):
	def __init__(self, game, priority):
			#locale.setlocale(locale.LC_ALL, '') #Might not be needed
			super(BaseGameMode, self).__init__(game, priority)
			
			
	def mode_started(self):
			#Start Attract Mode
			self.game.modes.add(self.game.attract_mode)
			self.game.utilities.releaseStuckBalls()
			
	###############################################################
	# UTILITY FUNCTIONS
	###############################################################

	#def score(self, points):
		#self.p = self.game.current_player()
		#self.p.score += points
		#self.cancel_delayed('updatescore')
		#self.delay(name='updatescore',delay=0.05,handler=self.game.utilities.updateBaseDisplay)

	def queueGameStartModes(self):
		#Might use in the future
		pass

	#def update_display(self):
		#self.p = self.game.current_player()
		#self.game.alpha_score_display.set_text(locale.format("%d", self.p.score, grouping=True),0,justify='left')
		#self.game.alpha_score_display.set_text(self.p.name.upper() + "  BALL "+str(self.game.ball),1,justify='right')
		#print self.p.name
		#print "Ball " + str(self.game.ball)

	###############################################################
	# MAIN GAME HANDLING FUNCTIONS
	###############################################################
	def start_game(self):
		self.game.utilities.log('Start Game','info')
		#This function is to be used when starting a NEW game, player 1 and ball 1
		#Clean Up
		self.game.modes.remove(self.game.attract_mode)
		#self.game.modes.add(self.game.tilt)
		
		self.game.add_player() #will be first player at this point
		self.game.ball = 1

		self.queueGameStartModes()
		self.start_ball()
		self.game.utilities.updateBaseDisplay()
		#self.game.sound.load_music('main')
		
		print "Game Started"
		
	def start_ball(self):
		self.game.utilities.log('Start Ball','info')
		#### Queue Ball Modes ####
		self.game.modes.add(self.game.skillshot_mode)
		self.game.modes.add(self.game.centerramp_mode)
		self.game.modes.add(self.game.tilt)
		self.game.modes.add(self.game.ballsaver_mode)

		#### Enable Flippers ####
		self.game.coils.flipperEnable.enable()

		#### Kick Out Ball ####
		self.game.utilities.acCoilPulse(coilname='ballReleaseShooterLane_CenterRampFlashers1',pulsetime=50)

		#### Update Player Display ####
		self.game.utilities.updateBaseDisplay()

		#### Enable GI in case it is disabled from TILT ####
		self.game.utilities.enableGI()

		#### Start Shooter Lane Music ####
		self.game.sound.play_music('shooter',loops=-1)
		self.game.shooter_lane_status = 1

		#### Debug Info ####
		print "Ball Started"
		
	def end_ball(self):
		self.game.utilities.log("End of Ball " + str(self.game.ball) + " Called",'info')
		self.game.utilities.log("Total Players: " + str(len(self.game.players)),'info')
		self.game.utilities.log("Current Player: " + str(self.game.current_player_index),'info')
		self.game.utilities.log("Balls Per Game: " + str(self.game.balls_per_game),'info')
		self.game.utilities.log("Current Ball: " + str(self.game.ball),'info')

		#### Remove Ball Modes ####
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.modes.remove(self.game.centerramp_mode)
		self.game.modes.remove(self.game.tilt)

		#self.game.sound.fadeout_music(time_ms=1000) #This is causing delay issues with the AC Relay
		self.game.sound.stop_music()

		

		if self.game.current_player_index == len(self.game.players) - 1:
			#Last Player or Single Player Drained
			#print "Last player or single player drained"
			if self.game.ball == self.game.balls_per_game:
				#Last Ball Drained
				print "Last ball drained, ending game"
				self.end_game()
			else:
				#Increment Current Ball
				#print "Increment current ball and set player back to 1"
				self.game.current_player_index = 0
				self.game.ball += 1
				self.start_ball()
		else:
			#Not Last Player Drained
			print "Not last player drained"
			self.game.current_player_index += 1
			self.start_ball()


	def end_game(self):
		self.game.utilities.log('Game Ended','info')
		
		self.game.coils.flipperEnable.disable()

		#disable AC Relay
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()

		self.game.reset()

	###############################################################
	# BASE SWITCH HANDLING FUNCTIONS
	###############################################################		
	def sw_instituteDown_closed(self, sw):
		self.game.coils.quakeInstitute.disable()
		return procgame.game.SwitchStop
		
	def sw_startButton_active_for_20ms(self, sw):
		print 'Player: ' + str(self.game.players.index)
		print 'Ball' + str(self.game.ball)
		#Trough is full!
		if self.game.ball == 0:
			if self.game.utilities.troughIsFull()==True:
				#########################
				#Start New Game
				#########################
				self.start_game()
			else:
				#missing balls
				self.game.utilities.releaseStuckBalls()
				self.game.alpha_score_display.set_text("MISSING PINBALLS",0)
				self.game.alpha_score_display.set_text("PLEASE WAIT",1)
		elif self.game.ball == 1 and len(self.game.players) < 4:
			self.game.add_player()
		else:
			pass		
		return procgame.game.SwitchStop

	def sw_startButton_active_for_1s(self, sw):
		#will put launcher in here eventually
		pass
		
	def sw_outhole_closed_for_1s(self, sw):
		### Ball handling ###
		self.game.utilities.setBallInPlay(False)
		self.game.utilities.acCoilPulse('outholeKicker_CaptiveFlashers')
		self.delay('endBall',delay=1,handler=self.end_ball)
		return procgame.game.SwitchStop

	def sw_ejectHole5_closed_for_1s(self, sw):
		self.game.utilities.acCoilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperBottom_closed_for_1s(self, sw):
		self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperTop_closed_for_1s(self, sw):
		self.game.coils.topBallPopper.pulse(50)
		self.game.coils.quakeMotor.pulse(50)
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_ballPopperTop_closed(self, sw):
		self.game.coils.quakeMotor.pulse(50)
		self.game.coils.quakeInstitute.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_jetLeft_active(self, sw):
		self.game.coils.jetLeft.pulse(30)
		self.game.sound.play('jet')
		self.game.lamps.jetLeftLamp.enable()
		self.game.utilities.score(500)
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		self.game.coils.jetRight.pulse(30)
		self.game.sound.play('jet')
		self.game.lamps.jetRightLamp.enable()
		self.game.utilities.score(500)
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		self.game.coils.jetTop.pulse(30)
		self.game.sound.play('jet')
		self.game.lamps.jetTopLamp.enable()
		self.game.utilities.score(500)
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		self.game.coils.slingL.pulse(30)
		self.game.sound.play('sling')
		self.game.utilities.score(100)
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		self.game.coils.slingR.pulse(30)
		self.game.sound.play('sling')
		self.game.utilities.score(100)
		return procgame.game.SwitchStop

	def sw_spinner_active(self, sw):
		self.game.coils.dropReset_CenterRampFlashers2.pulse(40)
		self.game.sound.play('spinner')
		self.game.utilities.score(100)
		return procgame.game.SwitchStop

	##################################################
	## Skillshot Switches
	## These will set the ball in play when tripped
	##################################################
	def sw_onRamp25k_active(self, sw):
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_onRamp50k_active(self, sw):
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_onRamp100k_active(self, sw):
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_onRampBypass_active(self, sw):
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_centerRampMiddle_active(self, sw):
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	def sw_centerRampEnd_active(self, sw):
		self.game.utilities.setBallInPlay(True)
		return procgame.game.SwitchStop

	#############################
	## Zone Switches
	#############################
	def sw_leftStandup1_closed(self, sw):
		self.game.lamps.standupLeft1.enable()
		self.game.lamps.building1.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_rightStandupHigh2_closed(self, sw):
		self.game.lamps.standupRightHigh2.enable()
		self.game.lamps.building2.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_rightStandupLow3_closed(self, sw):
		self.game.lamps.standupRightLow3.enable()
		self.game.lamps.building3.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop
		
	def sw_centerStandup4_closed(self, sw):
		self.game.lamps.standupCenter4.enable()
		self.game.lamps.building4.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop
		
	def sw_ejectHole5_closed(self, sw):
		self.game.lamps.ejectTop5.enable()
		self.game.lamps.building5.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop
		
	def sw_rightLoop6_closed(self, sw):
		self.game.lamps.underFaultLoop6.enable()
		self.game.lamps.building6.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop
		
	def sw_rightInsideReturn7_closed(self, sw):
		self.game.lamps.inlaneRight7.enable()
		self.game.lamps.building7.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop
		
	def sw_leftReturnLane8_closed(self, sw):
		self.game.lamps.inlaneLeft8.enable()
		self.game.lamps.building8.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop
		
	def sw_captiveBall9_closed(self, sw):
		self.game.lamps.captiveArrow9.enable()
		self.game.lamps.building9.enable()
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_ballShooter_closed_for_1s(self, sw):
		if (self.game.utilities.get_player_stats('ball_in_play') == True):
			#Kick the ball into play
			self.game.utilities.launch_ball()
		return procgame.game.SwitchStop