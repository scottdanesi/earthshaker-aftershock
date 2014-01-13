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

ballSaverTime = 15
clearForLaunch = False

class BallSaver(game.Mode):
	def __init__(self, game):
			super(BallSaver, self).__init__(game=game, priority=100)

	def mode_started(self):
		self.startBallSaverLamps()

	def mode_stopped(self):
		self.stopBallSaverLamps()

	def acCoilPulse(self,coilname,pulsetime=50):
		self.acSelectTimeBuffer = .2
		#Insert placeholder to stop flasher lampshows and schedules?
		self.cancel_delayed(name='acEnableDelay')
		self.game.coils.acSelect.disable()
		self.delay(name='coilDelay',event_type=None,delay=self.acSelectTimeBuffer,handler=self.game.coils[coilname].pulse,param=pulsetime)
		self.delay(name='acEnableDelay',delay=pulsetime+(self.acSelectTimeBuffer*2),handler=self.game.coils.acSelect.enable)

	def update_display(self):
		pass
		
	def startBallSaverLamps(self):
		self.game.lamps.shootAgain.schedule(schedule=0xFF00FF00, cycle_seconds=0, now=False)

	def stopBallSaverLamps(self):
		self.game.lamps.shootAgain.disable()

	def stopBallSaverMode(self):
		self.game.modes.remove(self)

	def sw_outhole_closed_for_1s(self, sw):
		#Kick another ball
		clearForLaunch = True
		self.game.score_display.set_text("BALL SAVED",0,justify='center')
		self.game.score_display.set_text(" ",1,justify='center')
		self.acCoilPulse(coilname='outholeKicker_CaptiveFlashers',pulsetime=50)
		if self.game.switches.trough1.is_active()==True:
			self.acCoilPulse(coilname='ballReleaseShooterLane_CenterRampFlashers1',pulsetime=50)
		else:
			#this might cause an error
			self.delay(delay=1,handler=self.acCoilPulse,param='ballReleaseShooterLane_CenterRampFlashers1')
		self.delay(delay=2,handler=self.stopBallSaverMode)
		return procgame.game.SwitchStop

	def sw_outhole_closed(self, sw):
		return procgame.game.SwitchStop

	def sw_ballShooter_closed_for_1s(self, sw):
		if clearForLaunch == True:
			#launch Ball
			self.game.coils.autoLauncher.pulse(100)
		return procgame.game.SwitchStop

	def sw_ballShooter_open_for_1s(self, sw):
		self.delay('ballsaver',delay=ballSaverTime,handler=self.stopBallSaverMode)