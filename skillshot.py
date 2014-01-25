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
##    _____ __ __ ______    __   _____ __  ______  ______
##   / ___// //_//  _/ /   / /  / ___// / / / __ \/_  __/
##   \__ \/ ,<   / // /   / /   \__ \/ /_/ / / / / / /   
##  ___/ / /| |_/ // /___/ /______/ / __  / /_/ / / /    
## /____/_/ |_/___/_____/_____/____/_/ /_/\____/ /_/     
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import scoredisplay
from scoredisplay import AlphaScoreDisplay
#from base import AlphaScoreDisplay

class SkillshotMode(game.Mode):
	def __init__(self, game, priority):
			super(SkillshotMode, self).__init__(game, priority)
			####################
			#Mode Setup
			####################
			
			#self.score_display = AlphaScoreDisplay(self.game,0)
			#gameover_mode = GameOver(game)
			
			#self.checkForStuckBalls()

	def mode_started(self):
		#self.delay(delay=.5,handler=self.enableACSelect)
		self.startSkillshotLamps()

		return super(SkillshotMode, self).mode_started()

	def enableACSelect(self):
		self.game.coils.acSelect.enable() #for Flashers

	def mode_stopped(self):
		self.stopSkillshotLamps()
		return super(SkillshotMode, self).mode_stopped()

	#def update_display(self):
		#self.p = self.game.current_player()
		#self.game.score_display.set_text(str(self.p.score),0)
		#self.game.score_display.set_text("Ball "+str(self.game.ball),1)
		
	def startSkillshotLamps(self):
		self.game.lamps.captive25k.schedule(schedule=0x0000000F, cycle_seconds=0, now=False)
		self.game.lamps.captive50k.schedule(schedule=0x000000F0, cycle_seconds=0, now=False)
		self.game.lamps.captive100k.schedule(schedule=0x00000F00, cycle_seconds=0, now=False)
		self.game.lamps.captive150k.schedule(schedule=0x0000F000, cycle_seconds=0, now=False)
		self.game.lamps.captive250k.schedule(schedule=0x000F0000, cycle_seconds=0, now=False)
		self.game.lamps.captiveArrow9.schedule(schedule=0xCCC00000, cycle_seconds=0, now=False)
		#self.game.coils.outholeKicker_CaptiveFlashers.schedule(schedule=0x00C00000, cycle_seconds=0, now=False)

	def stopSkillshotLamps(self):
		self.game.lamps.captive25k.disable()
		self.game.lamps.captive50k.disable()
		self.game.lamps.captive100k.disable()
		self.game.lamps.captive150k.disable()
		self.game.lamps.captive250k.disable()
		self.game.lamps.captiveArrow9.disable()
		#self.game.coils.outholeKicker_CaptiveFlashers.disable()

	def score(self, points):
		p = self.game.current_player()
		p.score += points
		#self.cancel_delayed('updatescore')
		#self.delay(name='updatescore',delay=0.5,handler=self.game.utilities.updateBaseDisplay)

	##############################
	## Skillshot Handling Modes ##
	##############################
	def superSkillshotMissed(self):
		self.game.utilities.displayText(100,'SUPER SKILLSHOT','MISSED',seconds=3,justify='center')
		self.game.modes.remove(self)

	def superSkillshotAwarded(self):
		self.game.sound.play_voice('skillshotAwarded')
		self.game.utilities.displayText(100,'SUPER SKILLSHOT','250,000 POINTS',seconds=3,justify='center')
		self.score(250000)
		self.game.modes.remove(self)

	def skillshotMissed(self):
		self.game.utilities.displayText(100,'SKILLSHOT','MISSED',seconds=3,justify='center')
		self.game.modes.remove(self)

	def skillshotAwarded(self):
		#self.game.utilities.displayText(100,'SKILLSHOT','250,000 POINTS',seconds=3,justify='center')
		self.game.modes.remove(self)

	###########################
	## Switch Handling Modes ##
	###########################

	def sw_outhole_closed_for_1s(self, sw):
		#### Remove Skillshot Mode ####
		self.game.modes.remove(self.game.skillshot_mode)
		return procgame.game.SwitchContinue

	def sw_onRamp50k_active(self, sw):
		self.game.utilities.displayText(100,'SKILLSHOT','50,000 POINTS',seconds=3,justify='center')
		self.skillshotAwarded()
		return procgame.game.SwitchContinue

	def sw_onRamp25k_active(self, sw):
		self.game.utilities.displayText(100,'SKILLSHOT','25,000 POINTS',seconds=3,justify='center')
		self.skillshotAwarded()
		return procgame.game.SwitchContinue

	def sw_onRamp100k_active(self, sw):
		self.game.utilities.displayText(100,'SKILLSHOT','100,000 POINTS',seconds=3,justify='center')
		self.skillshotAwarded()
		return procgame.game.SwitchContinue

	def sw_onRampBypass_active(self, sw):
		#need to score
		self.skillshotMissed()
		return procgame.game.SwitchContinue

	def sw_centerRampMiddle_active(self, sw):
		#self.game.coils.outholeKicker_CaptiveFlashers.pulse(5)
		#self.skillshotMissed()
		return procgame.game.SwitchContinue

	def sw_centerRampEnd_active(self, sw):
		#self.game.coils.outholeKicker_CaptiveFlashers.pulse(5)
		#self.skillshotMissed()
		return procgame.game.SwitchContinue

	def sw_captiveBall9_closed(self, sw):
		#self.game.coils.outholeKicker_CaptiveFlashers.schedule(schedule=0x33330000, cycle_seconds=1, now=True)
		self.superSkillshotAwarded()
		return procgame.game.SwitchContinue