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
			super(BaseGameMode, self).__init__(game, priority)
			self.finishingBall = False
			self.missingBalls = False
			
	def mode_started(self):
			#Start Attract Mode
			self.game.modes.add(self.game.attract_mode)
			self.game.utilities.releaseStuckBalls()

	def update_lamps(self):
		self.game.lamps.jetLeftLamp.enable()
		self.game.lamps.jetRightLamp.enable()
		self.game.lamps.jetTopLamp.enable()
			
	###############################################################
	# MAIN GAME HANDLING FUNCTIONS
	###############################################################
	def start_game(self):
		self.game.utilities.log('Start Game','info')

		self.game.sound.stop_music()

		#Reset Prior Game Scores
		self.game.game_data['LastGameScores']['LastPlayer1Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer3Score'] = ' '
		self.game.game_data['LastGameScores']['LastPlayer4Score'] = ' '

		#This function is to be used when starting a NEW game, player 1 and ball 1
		#Clean Up
		self.game.modes.remove(self.game.attract_mode)
		
		self.game.add_player() #will be first player at this point
		self.game.ball = 1

		self.start_ball()
		self.game.utilities.updateBaseDisplay()
		self.game.sound.play('game_start_rev')
		self.delay(delay=1.2,handler=self.game.sound.play,param='game_start')

		self.game.rightramp_mode.resetFault()
		
		print "Game Started"
		
	def start_ball(self):
		self.game.utilities.log('Start Ball','info')

		#### Update Audits ####
		self.game.game_data['Audits']['Balls Played'] += 1
		self.game.save_game_data()
		
		#### Set Diagnostic LED ####
		self.game.utilities.setDiagLED(self.game.current_player_index + 1)

		#### Enable Flippers ####
		self.game.coils.flipperEnable.enable()

		self.game.enable_bumpers(enable=True)

		#### Ensure GI is on ####
		self.game.utilities.enableGI()

		#### Kick Out Ball ####
		self.game.trough.launch_balls(num=1)

		#### Queue Ball Modes ####
		self.loadBallModes()

		#### Update Player Display ####
		self.game.utilities.updateBaseDisplay()

		#### Enable GI in case it is disabled from TILT ####
		self.game.utilities.enableGI()

		#### Start Shooter Lane Music ####
		self.game.sound.play_music('shooter',loops=-1,music_volume=.5)
		self.game.shooter_lane_status = 1

		self.game.update_lamps()

		#### Debug Info ####
		print "Ball Started"

	def finish_ball(self):
		if (self.finishingBall == False):
			self.finishingBall = True

			# Remove Drops and Mini Modes because of delay issue #
			self.game.modes.remove(self.game.drops_mode)

			#### Remove Skillshot Mode ####
			self.game.modes.remove(self.game.skillshot_mode)

			self.unloadMiniModes()

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

		#### Reset Multiball Identifier in case something went wrong ####
		self.game.utilities.set_player_stats('multiball_running',False)

		self.game.sound.stop_music()

		if self.game.current_player_index == len(self.game.players) - 1:
			#Last Player or Single Player Drained
			if self.game.ball == self.game.balls_per_game:
				#Last Ball Drained
				print "Last ball drained, ending game"
				#self.end_game()
				self.finish_game()
			else:
				#Increment Current Ball
				self.game.current_player_index = 0
				self.game.ball += 1
				self.start_ball()
		else:
			#Not Last Player Drained
			print "Not last player drained"
			self.game.current_player_index += 1
			self.start_ball()

		self.finishingBall = False

	def finish_game(self):
		self.game.modes.add(self.game.highscore_mode)
		self.game.highscore_mode.checkScores(self.game.base_mode.end_game)

	def end_game(self):
		self.game.utilities.log('Game Ended','info')

		self.game.modes.remove(self.game.highscore_mode)

		self.game.rightramp_mode.closeFault()

		#### Disable Flippers ####
		self.game.coils.flipperEnable.disable()

		#### Disable Bumpers ####
		self.game.enable_bumpers(enable=False)

		#### Disable AC Relay ####
		self.cancel_delayed(name='acEnableDelay')
		#self.game.coils.acSelect.disable()

		#### Update Gmaes Played Stats ####
		self.game.game_data['Audits']['Games Played'] += 1

		#### Save Game Audit Data ####
		self.game.save_game_data()

		self.game.sound.play_music('game_over',loops=1,music_volume=1)
		
		self.game.reset()

	def loadBallModes(self):
		self.game.modes.add(self.game.skillshot_mode)
		self.game.modes.add(self.game.centerramp_mode)
		self.game.modes.add(self.game.rightramp_mode)
		self.game.modes.add(self.game.tilt)
		self.game.modes.add(self.game.ballsaver_mode)
		self.game.modes.add(self.game.drops_mode)
		self.game.modes.add(self.game.jackpot_mode)
		self.game.modes.add(self.game.million_mode)
		self.game.modes.add(self.game.spinner_mode)
		self.game.modes.add(self.game.combo_mode)
		self.game.modes.add(self.game.multiball_mode)
		self.game.modes.add(self.game.collect_mode)
		self.game.modes.add(self.game.shelter_mode)
		self.game.modes.add(self.game.bonusmultiplier_mode)
		self.game.modes.add(self.game.switch_tracker_mode)

	def unloadBallModes(self):
		self.game.modes.remove(self.game.skillshot_mode)
		self.game.modes.remove(self.game.centerramp_mode)
		self.game.modes.remove(self.game.rightramp_mode)
		self.game.modes.remove(self.game.tilt)
		self.game.modes.remove(self.game.ballsaver_mode)
		self.game.modes.remove(self.game.drops_mode)
		self.game.modes.remove(self.game.jackpot_mode)
		self.game.modes.remove(self.game.million_mode)
		self.game.modes.remove(self.game.spinner_mode)
		self.game.modes.remove(self.game.combo_mode)
		self.game.modes.remove(self.game.multiball_mode)
		self.game.modes.remove(self.game.collect_mode)
		self.game.modes.remove(self.game.shelter_mode)
		self.game.modes.remove(self.game.bonusmultiplier_mode)
		self.game.modes.remove(self.game.switch_tracker_mode)
		self.unloadMiniModes()

	def unloadMiniModes(self):
		### Unload All Mini Modes ###
		self.game.modes.remove(self.game.mode_1)
		self.game.modes.remove(self.game.mode_2)
		self.game.modes.remove(self.game.mode_3)
		self.game.modes.remove(self.game.mode_4)
		self.game.modes.remove(self.game.mode_5)
		self.game.modes.remove(self.game.mode_6)
		self.game.modes.remove(self.game.mode_7)
		self.game.modes.remove(self.game.mode_8)
		self.game.modes.remove(self.game.mode_9)

	def ejectZone5(self):
		self.game.utilities.acFlashPulse('californiaFault_CenterRampFlashers3')
		self.delay(delay=.2,handler=self.game.utilities.acFlashPulse,param='californiaFault_CenterRampFlashers3')
		self.delay(delay=.4,handler=self.game.utilities.acCoilPulse,param='ejectHole_CenterRampFlashers4')
		self.delay(delay=.6,handler=self.game.sound.play,param='ejectsaucer')

	###############################################################
	# BASE SWITCH HANDLING FUNCTIONS
	###############################################################		

	def sw_startButton_active_for_1000ms(self, sw):
		#########################
		#Force Stop Game
		#########################
		self.game.utilities.log('Force Stop Game','warning')

		#### Remove Ball Modes ####
		self.unloadBallModes()

		self.game.sound.stop_music()

		self.end_game()
		
	def sw_startButton_active_for_20ms(self, sw):
		print 'Player: ' + str(self.game.players.index)
		print 'Ball' + str(self.game.ball)

		if self.game.ball == 0:
			if self.game.utilities.troughIsFull()==True:
				#########################
				#Start New Game
				#########################
				self.start_game()
			else:
				#########################
				#Missing Balls
				#########################
				self.game.utilities.displayText(100,'MISSING BALLS','PLEASE WAIT',seconds=4,justify='center')
				self.game.utilities.executeBallSearch()
		elif self.game.ball == 1 and len(self.game.players) < 4:
			#########################
			#Add Player
			#########################
			self.game.add_player()
			print 'Player Added - Total Players = ' + str(len(self.game.players))
			if (len(self.game.players) == 2):
				self.game.sound.play_voice('player_2_vox')
				self.game.utilities.displayText(200,topText='PLAYER 2',bottomText='ADDED',seconds=1,justify='center')
			elif (len(self.game.players) == 3):
				self.game.sound.play_voice('player_3_vox')
				self.game.utilities.displayText(200,topText='PLAYER 3',bottomText='ADDED',seconds=1,justify='center')
			elif (len(self.game.players) == 4):
				self.game.sound.play_voice('player_4_vox')
				self.game.utilities.displayText(200,topText='PLAYER 4',bottomText='ADDED',seconds=1,justify='center')
		else:
			#########################
			#Do Nothing
			#########################
			pass		
		return procgame.game.SwitchStop

	def sw_startButton_active_for_1s(self, sw):
		#will put launcher in here eventually
		pass
		
	def sw_outhole_closed_for_1s(self, sw):
		return procgame.game.SwitchStop

	def sw_ejectHole5_closed_for_200ms(self, sw):
		return procgame.game.SwitchStop

	def sw_jetLeft_active(self, sw):
		self.game.sound.play('jet')
		self.game.utilities.score(1000)
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		self.game.sound.play('jet')
		self.game.utilities.score(1000)
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		self.game.sound.play('jet')
		self.game.utilities.score(1000)
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		self.game.sound.play('sling')
		self.game.utilities.score(200)
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		self.game.sound.play('sling')
		self.game.utilities.score(200)
		return procgame.game.SwitchStop

	def sw_spinner_active(self, sw):
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

	def sw_ballShooter_open_for_30ms(self, sw):
		# This will play the car take off noise when the ball leaves the shooter lane
		if (self.game.utilities.get_player_stats('ball_in_play') == False and len(self.game.players) > 0):
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
		return procgame.game.SwitchStop

	def sw_leftOutlane_closed(self, sw):
		self.game.sound.play('outlane')
		return procgame.game.SwitchStop

	#############################
	## Institute Switch
	#############################
	def sw_instituteUp_open_for_100ms(self, sw):
		self.game.coils.quakeInstitute.disable()
		return procgame.game.SwitchStop