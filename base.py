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

#from bonus import *

class BaseGameMode(game.Mode):
	def __init__(self, game, priority):
			#locale.setlocale(locale.LC_ALL, '') #Might not be needed
			super(BaseGameMode, self).__init__(game, priority)
			
			
	def mode_started(self):
			#Start Attract Mode
			self.game.modes.add(self.game.attract_mode)
			self.game.utilities.releaseStuckBalls()
			
	###############################################################
	# MAIN GAME HANDLING FUNCTIONS
	###############################################################
	def start_game(self):
		self.game.utilities.log('Start Game','info')

		#Reset Prior Game Scores
		self.game.game_data['LastGameScores']['LastPlayer1Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer3Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer4Score'] = ' '

		#This function is to be used when starting a NEW game, player 1 and ball 1
		#Clean Up
		self.game.modes.remove(self.game.attract_mode)
		#self.game.modes.add(self.game.tilt)
		
		self.game.add_player() #will be first player at this point
		self.game.ball = 1

		self.start_ball()
		self.game.utilities.updateBaseDisplay()
		self.game.sound.play('game_start_rev')
		self.delay(delay=1.2,handler=self.game.sound.play,param='game_start')
		#self.game.sound.play('game_start')

		self.game.rightramp_mode.resetFault()
		
		print "Game Started"
		
	def start_ball(self):
		self.game.utilities.log('Start Ball','info')

		#### Update Audits ####
		self.game.game_data['Audits']['Balls Played'] += 1
		self.game.save_game_data()

		#### Queue Ball Modes ####
		self.loadBallModes()

		#### Enable Flippers ####
		self.game.coils.flipperEnable.enable()

		self.game.enable_bumpers(enable=True)

		#### Ensure GI is on ####
		self.game.utilities.enableGI()

		#### Kick Out Ball ####
		# This is from the original code.  Replacing with the trough mode functions
		#self.game.utilities.acCoilPulse(coilname='ballReleaseShooterLane_CenterRampFlashers1',pulsetime=50)
		#self.game.trough.num_balls_in_play = 1
		#self.game.trough.num_balls_to_launch = 1
		self.game.trough.launch_balls(num=1)


		#### Update Player Display ####
		self.game.utilities.updateBaseDisplay()

		#### Enable GI in case it is disabled from TILT ####
		self.game.utilities.enableGI()

		#### Start Shooter Lane Music ####
		self.game.sound.play_music('shooter',loops=-1,music_volume=.5)
		self.game.shooter_lane_status = 1

		#### Debug Info ####
		print "Ball Started"

	def finish_ball(self):
		# Remove Drops mode because of delay issue #
		self.game.modes.remove(self.game.drops_mode)

		self.game.modes.add(self.game.bonus_mode)
		if self.game.tiltStatus == 0:
			self.game.bonus_mode.calculate(self.game.base_mode.end_ball)
		else:
			self.end_ball()
		
	def end_ball(self):
		#Remove Bonus
		self.game.modes.remove(self.game.bonus_mode)

		#update games played stats
		self.game.game_data['Audits']['Balls Played'] += 1

		#Update Last Game Scores in game data file
		if self.game.ball == self.game.balls_per_game:
			self.playerAuditKey = 'LastPlayer' + str(self.game.current_player_index + 1) + 'Score'
			self.game.game_data['LastGameScores'][self.playerAuditKey] = self.game.utilities.currentPlayerScore()

		#save game audit data
		self.game.save_game_data()

		self.game.utilities.log("End of Ball " + str(self.game.ball) + " Called",'info')
		self.game.utilities.log("Total Players: " + str(len(self.game.players)),'info')
		self.game.utilities.log("Current Player: " + str(self.game.current_player_index),'info')
		self.game.utilities.log("Balls Per Game: " + str(self.game.balls_per_game),'info')
		self.game.utilities.log("Current Ball: " + str(self.game.ball),'info')

		#### Remove Ball Modes ####
		self.unloadBallModes()

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

		self.game.rightramp_mode.closeFault()

		#### Disable Flippers ####
		self.game.coils.flipperEnable.disable()

		#### Disable Bumpers ####
		self.game.enable_bumpers(enable=False)

		#### Disable AC Relay ####
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()

		#### Update Gmaes Played Stats ####
		self.game.game_data['Audits']['Games Played'] += 1

		#### Save Game Audit Data ####
		self.game.save_game_data()

		self.game.reset()

	def loadBallModes(self):
		self.game.modes.add(self.game.skillshot_mode)
		self.game.modes.add(self.game.centerramp_mode)
		self.game.modes.add(self.game.rightramp_mode)
		self.game.modes.add(self.game.tilt)
		self.game.modes.add(self.game.ballsaver_mode)
		self.game.modes.add(self.game.drops_mode)
		self.game.modes.add(self.game.jackpot_mode)
		self.game.modes.add(self.game.spinner_mode)
		self.game.modes.add(self.game.multiball_mode)
		self.game.modes.add(self.game.collect_mode)

	def unloadBallModes(self):
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.modes.remove(self.game.centerramp_mode)
		self.game.modes.remove(self.game.rightramp_mode)
		self.game.modes.remove(self.game.tilt)
		self.game.modes.remove(self.game.ballsaver_mode)
		self.game.modes.remove(self.game.drops_mode)
		self.game.modes.remove(self.game.jackpot_mode)
		self.game.modes.remove(self.game.spinner_mode)
		self.game.modes.remove(self.game.multiball_mode)
		self.game.modes.remove(self.game.collect_mode)

	###############################################################
	# BASE SWITCH HANDLING FUNCTIONS
	###############################################################		
	def sw_instituteDown_closed(self, sw):
		self.game.coils.quakeInstitute.disable()
		return procgame.game.SwitchStop

	def sw_startButton_active_for_1000ms(self, sw):
		#########################
		#Force Stop Game
		#########################
		self.game.utilities.log('Force Stop Game','warning')

		#### Remove Ball Modes ####
		self.unloadBallModes()

		#self.game.sound.fadeout_music(time_ms=1000) #This is causing delay issues with the AC Relay
		self.game.sound.stop_music()

		self.end_game()
		
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
				#self.game.alpha_score_display.set_text("MISSING PINBALLS",0)
				#self.game.alpha_score_display.set_text("PLEASE WAIT",1)
		elif self.game.ball == 1 and len(self.game.players) < 4:
			self.game.add_player()
			print 'Player Added - Total Players = ' + str(len(self.game.players))
			if (len(self.game.players) == 2):
				self.game.sound.play('player_2_vox')
				self.game.utilities.displayText(200,topText='PLAYER 2',bottomText='ADDED',seconds=1,justify='center')
			elif (len(self.game.players) == 3):
				self.game.sound.play('player_3_vox')
				self.game.utilities.displayText(200,topText='PLAYER 3',bottomText='ADDED',seconds=1,justify='center')
			elif (len(self.game.players) == 4):
				self.game.sound.play('player_4_vox')
				self.game.utilities.displayText(200,topText='PLAYER 4',bottomText='ADDED',seconds=1,justify='center')
		else:
			pass		
		return procgame.game.SwitchStop

	def sw_startButton_active_for_1s(self, sw):
		#will put launcher in here eventually
		pass
		
	def sw_outhole_closed_for_1s(self, sw):
		### Ball handling ###
		if self.game.trough.num_balls_in_play == 1: #Last ball in play
			self.game.utilities.setBallInPlay(False) # Will need to use the trough mode for this
			#self.game.utilities.acCoilPulse('outholeKicker_CaptiveFlashers')
			self.delay('finishBall',delay=1,handler=self.finish_ball)
		return procgame.game.SwitchStop

	def sw_ejectHole5_closed_for_1s(self, sw):
		self.game.utilities.acCoilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		return procgame.game.SwitchStop

	def sw_ballPopperBottom_closed_for_1s(self, sw):
		self.game.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		self.delay(delay=.2,handler=self.game.sound.play,param='eject')
		self.game.utilities.score(250)
		return procgame.game.SwitchStop

	def sw_jetLeft_active(self, sw):
		#self.game.coils.jetLeft.pulse(30)
		self.game.sound.play('jet')
		self.game.lamps.jetLeftLamp.enable()
		self.game.utilities.score(500)
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		#self.game.coils.jetRight.pulse(30)
		self.game.sound.play('jet')
		self.game.lamps.jetRightLamp.enable()
		self.game.utilities.score(500)
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		#self.game.coils.jetTop.pulse(30)
		self.game.sound.play('jet')
		self.game.lamps.jetTopLamp.enable()
		self.game.utilities.score(500)
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		#self.game.coils.slingL.pulse(30)
		self.game.sound.play('sling')
		self.game.utilities.score(100)
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		#self.game.coils.slingR.pulse(30)
		self.game.sound.play('sling')
		self.game.utilities.score(100)
		return procgame.game.SwitchStop

	def sw_spinner_active(self, sw):
		#self.game.utilities.acFlashPulse(coilname='dropReset_CenterRampFlashers2',pulsetime=40)
		#self.game.coils.dropReset_CenterRampFlashers2.pulse(40)
		#self.game.sound.play('spinner')
		#self.game.utilities.score(100)
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

	def sw_ballShooter_open(self, sw):
		# This will play the car take off noise when the ball leaves the shooter lane
		if (self.game.utilities.get_player_stats('ball_in_play') == False):
			self.game.sound.play('game_start_takeoff')

	#############################
	## Zone Switches
	#############################
	def sw_leftStandup1_closed(self, sw):
		return procgame.game.SwitchStop

	def sw_rightStandupHigh2_closed(self, sw):
		return procgame.game.SwitchStop

	def sw_rightStandupLow3_closed(self, sw):
		return procgame.game.SwitchStop
		
	def sw_centerStandup4_closed(self, sw):
		return procgame.game.SwitchStop
		
	def sw_ejectHole5_closed(self, sw):
		return procgame.game.SwitchStop
		
	def sw_rightLoop6_closed(self, sw):
		return procgame.game.SwitchStop
		
	def sw_rightInsideReturn7_closed(self, sw):
		return procgame.game.SwitchStop
		
	def sw_leftReturnLane8_closed(self, sw):
		return procgame.game.SwitchStop
		
	def sw_captiveBall9_closed(self, sw):
		return procgame.game.SwitchStop

	def sw_ballShooter_closed_for_1s(self, sw):
		if (self.game.utilities.get_player_stats('ball_in_play') == True):
			#Kick the ball into play
			self.game.utilities.launch_ball()
		return procgame.game.SwitchStop

	#############################
	## Outlane Switches
	#############################
	def sw_rightOutlane_closed(self, sw):
		self.game.sound.play('outlane')

	def sw_leftOutlane_closed(self, sw):
		self.game.sound.play('outlane')
