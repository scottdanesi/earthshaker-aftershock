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
##     ___  ________________  ___   ____________   __  _______  ____  ______
##    /   |/_  __/_  __/ __ \/   | / ____/_  __/  /  |/  / __ \/ __ \/ ____/
##   / /| | / /   / / / /_/ / /| |/ /     / /    / /|_/ / / / / / / / __/   
##  / ___ |/ /   / / / _, _/ ___ / /___  / /    / /  / / /_/ / /_/ / /___   
## /_/  |_/_/   /_/ /_/ |_/_/  |_\____/ /_/    /_/  /_/\____/_____/_____/   
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc

class AttractMode(game.Mode):
	def __init__(self, game):
			super(AttractMode, self).__init__(game=game, priority=5)

	def mode_started(self):
		self.resetQuakeInstitute()
		self.startAttractLamps2()
		self.setDisplayContent()

	def mode_stopped(self):
		for lamp in self.game.lamps:
			lamp.disable()
		#Cancel Display Script
		#self.game.score_display.cancel_script() #Does not work...
			
	def setDisplayContent(self):
		#Script initialization
		script=[]

		#Title Screen
		script.append({'top':'<<<< Earthshaker','bottom':'Aftershock  >>>>','timer':5,'transition':3})

		#About
		script.append({'top':'software by','bottom':'scott danesi','timer':5,'transition':1})

		#Special Thanks
		script.append({'top':'SPECIAL THANKS','bottom':'myPinballs','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'Mark Sunnucks','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'Multimorphic','timer':3,'transition':2})
		
		#Cancel any score display scripts that may be running
		#self.game.score_display.cancel_script()

		#Start new display script
		self.game.score_display.set_script(script)
		
	def startAttractLamps(self):
		i = 0
		for lamp in self.game.lamps:
			if i % 4 == 3:
				lamp.schedule(schedule=0xf000f000, cycle_seconds=0, now=False)
			elif i % 4 == 2:
				lamp.schedule(schedule=0x0f000f00, cycle_seconds=0, now=False)
			elif i % 4 == 1:
				lamp.schedule(schedule=0x00f000f0, cycle_seconds=0, now=False)
			elif i % 4 == 0:
				lamp.schedule(schedule=0x000f000f, cycle_seconds=0, now=False)
			i = i + 1

	def startAttractLamps2(self):
		i = 0
		for lamp in self.game.lamps:
			if i % 8 == 7:
				lamp.schedule(schedule=0xf0000000, cycle_seconds=0, now=False)
			elif i % 8 == 6:
				lamp.schedule(schedule=0x0f000000, cycle_seconds=0, now=False)
			elif i % 8 == 5:
				lamp.schedule(schedule=0x00f00000, cycle_seconds=0, now=False)
			elif i % 8 == 4:
				lamp.schedule(schedule=0x000f0000, cycle_seconds=0, now=False)
			elif i % 8 == 3:
				lamp.schedule(schedule=0x0000f000, cycle_seconds=0, now=False)
			elif i % 8 == 2:
				lamp.schedule(schedule=0x00000f00, cycle_seconds=0, now=False)
			elif i % 8 == 1:
				lamp.schedule(schedule=0x000000f0, cycle_seconds=0, now=False)
			elif i % 8 == 0:
				lamp.schedule(schedule=0x0000000f, cycle_seconds=0, now=False)
			i = i + 1
		
	def resetQuakeInstitute(self):
		if self.game.switches.instituteUp.is_active()==False:
			self.game.coils.quakeInstitute.enable()

	def sw_instituteUp_open(self, sw):
		self.game.coils.quakeInstitute.disable()
		return procgame.game.SwitchStop
		
	def sw_startButton_active_for_50ms(self, sw):
		#if self.troughIsFull()==True:
			#Game Starting
			#self.game.modes.remove(self)
			return procgame.game.SwitchContinue

	def sw_outhole_active_for_1s(self, sw):
		self.game.coils.acSelect.disable()
		self.game.coils.flipperEnable.disable()
		self.game.coils.outholeKicker_CaptiveFlashers.pulse(50)
		self.game.score_display.set_text("GAME OVER",0)
		self.game.score_display.set_text("Press Start",1)
		return procgame.game.SwitchStop

	def sw_jetLeft_active(self, sw):
		return procgame.game.SwitchStop

	def sw_jetRight_active(self, sw):
		return procgame.game.SwitchStop

	def sw_jetTop_active(self, sw):
		return procgame.game.SwitchStop

	def sw_slingL_active(self, sw):
		return procgame.game.SwitchStop

	def sw_slingR_active(self, sw):
		return procgame.game.SwitchStop