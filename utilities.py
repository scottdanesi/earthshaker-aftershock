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

class UtilitiesMode(game.Mode):
	def __init__(self, game, priority):
			super(UtilitiesMode, self).__init__(game, priority)

	def mode_started(self):
		## Set Global Variables ##
		self.currentDisplayPriority = 0

	def mode_stopped(self):
		pass

	def troughIsFull(self): #should be moved globally
		if (self.game.switches.trough1.is_active()==True and self.game.switches.trough2.is_active()==True and self.game.switches.trough3.is_active()==True):
			return True
		else:
			return False

	def releaseStuckBalls(self):
		#Checks for balls in locks or outhole and kicks them out
		if self.game.switches.outhole.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='outholeKicker_CaptiveFlashers',pulsetime=50)
		if self.game.switches.ejectHole5.is_active()==True:
			self.game.utilities.acCoilPulse(coilname='ejectHole_CenterRampFlashers4',pulsetime=50)
		if self.game.switches.ballPopperBottom.is_active()==True:
			selfgame.utilities.acCoilPulse(coilname='bottomBallPopper_RightRampFlashers1',pulsetime=50)
		if self.game.switches.ballPopperTop.is_active()==True:
			self.game.coils.topBallPopper.pulse(50) #Does not need AC Relay logic
		if self.game.switches.ballShooter.is_active()==True:
			self.game.coils.autoLauncher.pulse(100) #Does not need AC Relay logic

	def acCoilPulse(self,coilname,pulsetime):
		self.acSelectTimeBuffer = .2
		self.acSelectEnableBuffer = (pulsetime/1000)+(self.acSelectTimeBuffer*2)
		#Insert placeholder to stop flasher lampshows and schedules?
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()
		self.delay(name='coilDelay',event_type=None,delay=self.acSelectTimeBuffer,handler=self.game.coils[coilname].pulse,param=pulsetime)
		self.delay(name='acEnableDelay',delay=self.acSelectEnableBuffer,handler=self.game.coils.acSelect.enable)

	def launch_ball(self):
		if self.game.switches.ballShooter.is_active()==True:
			self.game.coils.autoLauncher.pulse(100)

	def displayText(self,priority,topText=' ',bottomText=' ',seconds=2,justify='left'):
		# This function will be used as a very basic display prioritizing helper
		# Check if anything with a higher priority is running
		if (priority >= self.currentDisplayPriority):
			self.game.alpha_score_display.cancel_script()
			self.game.alpha_score_display.set_text(topText,0,justify)
			self.game.alpha_score_display.set_text(bottomText,1,justify)
			self.delay(name='resetDisplayPriority',event_type=None,delay=seconds,handler=self.resetDisplayPriority)
			self.currentDisplayPriority = priority

	def resetDisplayPriority(self):
		self.currentDisplayPriority = 0

	def updateBaseDisplay(self):
		print "Update Base Display Called"
		if (self.currentDisplayPriority == 0):
			self.p = self.game.current_player()
			self.game.alpha_score_display.cancel_script()
			self.game.alpha_score_display.set_text(locale.format("%d", self.p.score, grouping=True),0,justify='left')
			self.game.alpha_score_display.set_text(self.p.name.upper() + "  BALL "+str(self.game.ball),1,justify='right')
			print self.p.name
			print "Ball " + str(self.game.ball)