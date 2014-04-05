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
##     ____  ___    __    __       _____ ___ _    ____________ 
##    / __ )/   |  / /   / /      / ___//   | |  / / ____/ __ \
##   / __  / /| | / /   / /       \__ \/ /| | | / / __/ / /_/ /
##  / /_/ / ___ |/ /___/ /___    ___/ / ___ | |/ / /___/ _, _/ 
## /_____/_/  |_/_____/_____/   /____/_/  |_|___/_____/_/ |_|  
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc

class BallSaver(game.Mode):
	def __init__(self, game, priority):
			super(BallSaver, self).__init__(game, priority)

			self.ballSaverTime = 15 #This needs to be moved to pull from the configuration file
			self.ballSaverGracePeriodThreshold = 3 #This needs to be moved to pull from the configuration file
			self.ballSaveLampsActive = True #Probably should move to mode started instead of init...
			self.ballSavedEarly = False 

	############################
	#### Standard Functions ####
	############################
	def mode_started(self):
		self.cancel_delayed('stopballsavelamps')
		self.game.utilities.set_player_stats('ballsave_active',True)
		self.ballSaveLampsActive = True
		self.game.trough.ball_save_active = True
		self.update_lamps()

	def mode_stopped(self):
		self.game.trough.ball_save_active = False
		return super(BallSaver, self).mode_stopped()

	def update_lamps(self):
		print "Update Lamps: Ball Saver"
		if (self.game.utilities.get_player_stats('ballsave_active') == True and self.ballSaveLampsActive == True):
			self.startBallSaverLamps()
		else:
			self.stopBallSaverLamps()
		
	def startBallSaverLamps(self):
		self.game.lamps.shootAgain.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=False)

	def startBallSaverLampsWarning(self):
		self.game.lamps.shootAgain.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=False)

	def stopBallSaverLamps(self):
		self.ballSaveLampsActive = False
		self.game.lamps.shootAgain.disable()

	def stopBallSaverMode(self):
		self.game.utilities.set_player_stats('ballsave_active',False)
		self.stopBallSaverTimers()
		self.update_lamps()
		self.game.modes.remove(self)

	def startBallSaverTimers(self):
		self.game.utilities.set_player_stats('ballsave_timer_active',True)
		self.delay(name='ballsaver',delay=self.ballSaverTime,handler=self.stopBallSaverMode)
		self.delay(name='stopballsavelamps',delay=self.ballSaverTime - self.ballSaverGracePeriodThreshold,handler=self.stopBallSaverLamps)

	def stopBallSaverTimers(self):
		self.game.utilities.set_player_stats('ballsave_timer_active',False)
		self.cancel_delayed('stopballsavelamps')
		self.cancel_delayed('ballsaver')

	def kickBallToTrough(self):
		self.game.utilities.acCoilPulse(coilname='outholeKicker_CaptiveFlashers',pulsetime=50)

	def kickBallToShooterLane(self):
		self.game.utilities.acCoilPulse(coilname='ballReleaseShooterLane_CenterRampFlashers1',pulsetime=100)

	def saveBall(self):
		self.game.utilities.displayText(199,topText='BALL SAVED',bottomText=' ',seconds=3,justify='center')

		#Stop Skillshot
		self.game.modes.remove(self.game.skillshot_mode)

		self.game.sound.play('ball_saved')

		#These are from the original code
		#self.kickBallToTrough()
		#self.kickBallToShooterLane()
		self.game.trough.launch_balls(num=1)
		self.stopBallSaverMode()

	def saveBallEarly(self): #Need to work on this...
		self.game.utilities.displayText(199,topText='BALL SAVED',bottomText=' ',seconds=3,justify='center')

		#Stop Skillshot
		self.game.modes.remove(self.game.skillshot_mode)

		self.game.sound.play('ball_saved')

		#These are from the original code
		#self.kickBallToTrough()
		#self.kickBallToShooterLane()
		self.game.trough.launch_balls(num=1)
		self.stopBallSaverMode()

	def sw_outhole_closed_for_1s(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_active') == True):
			self.saveBall()
			self.game.utilities.log('BALLSAVE - Ouhole closed for 1s - SwitchStop','info')
			return procgame.game.SwitchStop
		else:
			self.game.utilities.log('BALLSAVE - Ouhole closed for 1s - SwitchContinue','info')
			return procgame.game.SwitchContinue

	def sw_outhole_closed(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_active') == True):
			self.game.utilities.log('BALLSAVE - Ouhole closed - SwitchStop - Disabling timers','info')
			self.cancel_delayed('ballsaver')
			return procgame.game.SwitchStop
		else:
			self.game.utilities.log('BALLSAVE - Ouhole closed - SwitchContinue','info')
			return procgame.game.SwitchContinue

	##################################################
	## Skillshot Switches
	## These will set the ball in play when tripped
	##################################################
	def sw_onRamp25k_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_onRamp50k_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_onRamp100k_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_onRampBypass_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_centerRampMiddle_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	def sw_centerRampEnd_active(self, sw):
		if (self.game.utilities.get_player_stats('ballsave_timer_active') == False):
			self.startBallSaverTimers()
		return procgame.game.SwitchContinue

	##################################################
	## Early Ballsave Switches
	## These will save the ball early if the trough has enough balls to support
	## WORK IN PROGRESS
	##################################################

	#def sw_rightOutlane_active(self, sw):
		#if (self.game.utilities.get_player_stats('ballsave_active') == True):
