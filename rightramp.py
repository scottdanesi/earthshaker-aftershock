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
##     ____  ____________  ________   ____  ___    __  _______ 
##    / __ \/  _/ ____/ / / /_  __/  / __ \/   |  /  |/  / __ \
##   / /_/ // // / __/ /_/ / / /    / /_/ / /| | / /|_/ / /_/ /
##  / _, _// // /_/ / __  / / /    / _, _/ ___ |/ /  / / ____/ 
## /_/ |_/___/\____/_/ /_/ /_/    /_/ |_/_/  |_/_/  /_/_/      
## 
#################################################################################

import procgame.game
from procgame import *
import pinproc
import scoredisplay
from scoredisplay import AlphaScoreDisplay
#from base import AlphaScoreDisplay

class RightRampMode(game.Mode):
	def __init__(self, game, priority):
			super(RightRampMode, self).__init__(game, priority)
			## Global Setting Variables ##
			pass

	def mode_started(self):
		## Global System Variables ##
		#self.rightRampShotStarted = False
		self.update_lamps()

	def mode_stopped(self):
		self.disableRightRampLamps()

	def update_lamps(self):
		
		print "Update Lamps: Right Ramp"

	def disableRightRampLamps(self):
		self.game.coils.jackpotFlasher.disable()
		self.game.lamps.rightRampJackpot.disable()

	def rightRampShotCompleted(self):
		self.game.lampctrlflash.play_show('center_ramp_1', repeat=False, callback=self.game.update_lamps)

		# Score it! #
		if (self.game.utilities.get_player_stats('multiball_running') == True):
			if (self.game.utilities.get_player_stats('jackpot_lit') == True):
				# Score Jackpot
				self.game.jackpot_mode.awardJackpot()
				self.sendBallToShelter()
			else:			
				self.game.utilities.score(50000)
				# Sound FX #
				self.game.sound.play('centerRampComplete')
				self.game.coils.topBallPopper.pulse(50)
		else:
			if (self.game.utilities.get_player_stats('lock1_lit') == True or self.game.utilities.get_player_stats('lock2_lit') == True or self.game.utilities.get_player_stats('lock3_lit') == True):
				self.sendBallToShelter()
				self.game.utilities.score(250)
			else:
				# Sound FX #
				self.game.sound.play('centerRampComplete')
				self.game.coils.topBallPopper.pulse(50)
				self.game.coils.quakeInstitute.enable()
				self.game.collect_mode.spotZone()
				self.game.utilities.score(250)
		

		# Add Fault Visit #
		self.game.utilities.set_player_stats('fault_visits',self.game.utilities.get_player_stats('fault_visits') + 1)

	def sw_rightRampEntry_active(self, sw):
		# Sound FX #
		self.game.sound.play('centerRampEnter')

		self.game.utilities.acFlashSchedule(coilname='bottomBallPopper_RightRampFlashers1',schedule=0x00000CCC, cycle_seconds=1, now=True) # This needs to be replaced with a lampshow for better AC Relay control 
		return procgame.game.SwitchContinue

	def openFault(self):
		if (self.game.switches.faultOpen.is_active() == False):
			self.game.utilities.acCoilPulse('californiaFault_CenterRampFlashers3')

	def closeFault(self):
		if (self.game.switches.faultOpen.is_active() == True):
			self.game.utilities.acCoilPulse('californiaFault_CenterRampFlashers3')

	def sendBallToShelter(self):
		self.openFault()
		self.delay(delay=2,handler=self.closeFault)
		self.delay(delay=.5,handler=self.game.coils.topBallPopper.pulse)

	def sw_ballPopperTop_closed(self, sw):
		self.game.utilities.acFlashSchedule(coilname='bottomBallPopper_RightRampFlashers1',schedule=0x0000C00C, cycle_seconds=1, now=True) # This needs to be replaced with a lampshow for better AC Relay control 
		self.game.utilities.acFlashSchedule(coilname='knocker_RightRampFlashers2',schedule=0x00C0C0C0, cycle_seconds=1, now=True) # This needs to be replaced with a lampshow for better AC Relay control 
		self.game.utilities.acFlashSchedule(coilname='unused_RightRampFlashers3',schedule=0x0C000C00, cycle_seconds=1, now=True) # This needs to be replaced with a lampshow for better AC Relay control 
		# Sound FX #
		#self.game.sound.play('rightRampComplete')

	def sw_ballPopperTop_closed_for_500ms(self, sw):
		# if (self.game.utilities.get_player_stats('lock1_lit') == True or self.game.utilities.get_player_stats('lock2_lit') == True or self.game.utilities.get_player_stats('lock3_lit') == True):
			#self.openFault()
			#self.delay(delay=2,handler=self.closeFault)
			#self.delay(delay=.5,handler=self.game.coils.topBallPopper.pulse)
		#else:
			#self.game.coils.topBallPopper.pulse(50)
		#self.game.coils.quakeInstitute.enable()
		#self.game.utilities.score(250)
		#self.game.collect_mode.spotZone()
		self.rightRampShotCompleted()
		return procgame.game.SwitchStop




	