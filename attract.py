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
import locale
import math
import random

#### Set Locale ####
locale.setlocale(locale.LC_ALL, "")

class AttractMode(game.Mode):
	def __init__(self, game, priority):
			super(AttractMode, self).__init__(game, priority)
			self.modeTickCounter = 0

	def mode_started(self):
		#### Reset Quake Instituet ####
		#### Be sure it is in the upright position ####
		self.resetQuakeInstitute()

		#### Start Attract Mode Lamps ####
		self.startAttractLamps2()

		#### Create and Set Display Content ####
		self.setDisplayContent()

		#### Ensure GI is on ####
		self.game.utilities.enableGI()

		#### Enable Backbox Lighting ####
		self.game.utilities.setBackboxLED(127,0,255)

	#def mode_tick(self):
		#This will cycle random colors through the backbox during Attract Mode
		#if(self.modeTickCounter == 1000):
			#self.game.utilities.setBackboxLED(random.randint(0,255),random.randint(0,255),random.randint(0,255))
			#self.modeTickCounter = 0
		#else:
			#self.modeTickCounter += 1

	def mode_stopped(self):
		#### Disable All Lamps ####
		for lamp in self.game.lamps:
			lamp.disable()

		#### Cancel Display Script ####
		self.game.alpha_score_display.cancel_script()

		#### Enable AC Relay for Flashers ####
		#### This is only needed for using lampshows that contain flashers on the AC Relay ####
		self.game.coils.acSelect.enable()

		#### Disable Backbox Lighting ####
		self.game.utilities.setBackboxLED()
			
	def setDisplayContent(self):
		#### Script List Variable Initialization ####
		script=[]

		################################################
		#### Earthshaker Title Animation Definition ####
		################################################
		animEarthshaker=[] # This is a temporary placeholder until we define new transitions
		animEarthshaker.append({'top':'                ','bottom':'                ','timer':.5,'transition':0})
		animEarthshaker.append({'top':'               E','bottom':'                ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'              EA','bottom':'K               ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'             EAR','bottom':'CK              ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'            EART','bottom':'OCK             ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'           EARTH','bottom':'HOCK            ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'          EARTHS','bottom':'SHOCK           ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'         EARTHSH','bottom':'RSHOCK          ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'        EARTHSHA','bottom':'ERSHOCK         ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'       EARTHSHAK','bottom':'TERSHOCK        ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'      EARTHSHAKE','bottom':'FTERSHOCK       ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'     EARTHSHAKER','bottom':'AFTERSHOCK      ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'    EARTHSHAKER ','bottom':' AFTERSHOCK     ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'   EARTHSHAKER  ','bottom':'  AFTERSHOCK    ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'  EARTHSHAKER   ','bottom':'   AFTERSHOCK   ','timer':2,'transition':0})
		animEarthshaker.append({'top':' EARTHsHAKER    ','bottom':'    AFTERSHOCK  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  EARTHsHAKER   ','bottom':'   aFTERSHOCK   ','timer':.1,'transition':0})
		animEarthshaker.append({'top':' EARThsHAKEr    ','bottom':'    aFTErSHOCK  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  EArThsHakEr   ','bottom':'   aFTErShOCK   ','timer':.1,'transition':0})
		animEarthshaker.append({'top':' EArThshakEr    ','bottom':'    aFTErShoCK  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  eArThshakEr   ','bottom':'   afTErShoCk   ','timer':.1,'transition':0})
		animEarthshaker.append({'top':' earThshakEr    ','bottom':'    afTErshoCk  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  earThshakEr   ','bottom':'   aftErshoCk   ','timer':.1,'transition':0})
		animEarthshaker.append({'top':' earThshakEr    ','bottom':'    aftershoCk  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  earThshakEr   ','bottom':'   aftershoCk   ','timer':.1,'transition':0})
		animEarthshaker.append({'top':' earThshakEr    ','bottom':'    aftershock  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  earthshakEr   ','bottom':'   aftershock   ','timer':.1,'transition':0})
		animEarthshaker.append({'top':' earthshaker    ','bottom':'    aftershock  ','timer':.1,'transition':0})
		animEarthshaker.append({'top':'  earthshaker   ','bottom':'   aftershock   ','timer':2,'transition':0})
		animEarthshaker.append({'top':' earthshaker    ','bottom':'    aftershock  ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'earthshaker     ','bottom':'     aftershock ','timer':.05,'transition':0})
		animEarthshaker.append({'top':'arthshaker      ','bottom':'      aftershock','timer':.05,'transition':0})
		animEarthshaker.append({'top':'rthshaker       ','bottom':'       aftershoc','timer':.05,'transition':0})
		animEarthshaker.append({'top':'thshaker        ','bottom':'        aftersho','timer':.05,'transition':0})
		animEarthshaker.append({'top':'hshaker         ','bottom':'         aftersh','timer':.05,'transition':0})
		animEarthshaker.append({'top':'shaker          ','bottom':'          afters','timer':.05,'transition':0})
		animEarthshaker.append({'top':'haker           ','bottom':'           after','timer':.05,'transition':0})
		animEarthshaker.append({'top':'aker            ','bottom':'            afte','timer':.05,'transition':0})
		animEarthshaker.append({'top':'ker             ','bottom':'             aft','timer':.05,'transition':0})
		animEarthshaker.append({'top':'er              ','bottom':'              af','timer':.05,'transition':0})
		animEarthshaker.append({'top':'r               ','bottom':'               a','timer':.05,'transition':0})
		animEarthshaker.append({'top':'                ','bottom':'                ','timer':.5,'transition':0})

		######################################################
		#### Earthshaker Original Animation ##################
		#### This animation is currently not used, but was the 
		#### original test that was created for animating on 
		#### the alphanumeric display.
		######################################################
		animEarthshaker2=[] # This is a temporary placeholder until we define new transitions
		animEarthshaker2.append({'top':'                ','bottom':'                ','timer':.5,'transition':0})
		animEarthshaker2.append({'top':'               E','bottom':'                ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'              EA','bottom':'K               ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'             EAR','bottom':'CK              ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'            EART','bottom':'OCK             ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'           EARTH','bottom':'HOCK            ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'          EARTHS','bottom':'SHOCK           ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'         EARTHSH','bottom':'RSHOCK          ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'        EARTHSHA','bottom':'ERSHOCK         ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'       EARTHSHAK','bottom':'TERSHOCK        ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'      EARTHSHAKE','bottom':'FTERSHOCK       ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'     EARTHSHAKER','bottom':'AFTERSHOCK      ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'    EARTHSHAKER ','bottom':' AFTERSHOCK     ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'   EARTHSHAKER  ','bottom':'  AFTERSHOCK    ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'  EARTHSHAKER   ','bottom':'   AFTERSHOCK   ','timer':2,'transition':0})
		animEarthshaker2.append({'top':' Earthshaker    ','bottom':'    Aftershock  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  Earthshaker   ','bottom':'   Aftershock   ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':' EarWhshaker    ','bottom':'    AfterXhock  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  EarWhshaker   ','bottom':'   AfterXhock   ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':' EarWhs9aker    ','bottom':'    AfterXhock  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  EarWhs9aker   ','bottom':'   Af*erXhock   ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':' KarWhs9(ker    ','bottom':'    Af*erXhock  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  KarWhs9(ker   ','bottom':'   Af*erXhoc7   ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':' KarWhF9(ker    ','bottom':'    Af*erXhoc7  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  KarWhF9(ker   ','bottom':'   Af*erXho>7   ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':' KGrWhF9(ker    ','bottom':'    Af*erXho>7  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  KGrWhF9(keU   ','bottom':'   Af*erXho>7   ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':' KGrWhF9(keU    ','bottom':'    Zf*erXho>7  ','timer':.1,'transition':0})
		animEarthshaker2.append({'top':'  KGrWhF9(keU   ','bottom':'   Zf*erXho>7   ','timer':2,'transition':0})
		animEarthshaker2.append({'top':' KGrWhF9(keU    ','bottom':'    Zf*erXho>7  ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'KGrWhF9(keU     ','bottom':'     Zf*erXho>7 ','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'GrWhF9(keU      ','bottom':'      Zf*erXho>7','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'rWhF9(keU       ','bottom':'       Zf*erXho>','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'WhF9(keU        ','bottom':'        Zf*erXho','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'hF9(keU         ','bottom':'         Zf*erXh','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'F9(keU          ','bottom':'          Zf*erX','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'9(keU           ','bottom':'           Zf*er','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'(keU            ','bottom':'            Zf*e','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'keU             ','bottom':'             Zf*','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'eU              ','bottom':'              Zf','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'U               ','bottom':'               Z','timer':.05,'transition':0})
		animEarthshaker2.append({'top':'                ','bottom':'                ','timer':.5,'transition':0})

		########################################################
		#### Title Screen Animation ############################
		#### Adds the animation defined above to the script list
		########################################################
		script=script + animEarthshaker

		########################
		#### About Game Software
		########################
		script.append({'top':'SOFTWARE BY','bottom':'SCOTT DANESI','timer':5,'transition':1})

		#########################
		#### Previous Game Scores
		#########################
		self.player1Score = self.game.game_data['LastGameScores']['LastPlayer1Score']
		self.player2Score = self.game.game_data['LastGameScores']['LastPlayer2Score']
		self.player3Score = self.game.game_data['LastGameScores']['LastPlayer3Score']
		self.player4Score = self.game.game_data['LastGameScores']['LastPlayer4Score']

		#######################################################################
		#### Set Top and Bottom Text for Previous Game Scores #################
		#### This section will create a string of 16 characters for the top 
		#### and bottom score displays that contains 2 scores for for each row.  
		#### It also contains error checking for when both scores on 1 line are 
		#### larger than 16 characters.
		#######################################################################
		self.scoreSpaceCount = 16 - (len(str(self.player1Score)) + len(str(self.player2Score)))
		if self.scoreSpaceCount < 0: # Just in case scores get very large (over 8 characters each)
			self.scoreSpaceCount = 0
		self.topScoresText = str(self.player1Score)
		for i in range (0,self.scoreSpaceCount): # Puts a space between the scores for i places
			self.topScoresText += ' ' 
		self.topScoresText += str(self.player2Score) # Add the score to the end
		# Set Bottom Text
		self.scoreSpaceCount = 16 - (len(str(self.player3Score)) + len(str(self.player4Score)))
		if self.scoreSpaceCount < 0: # Just in case scores get very large (over 8 characters each)
			self.scoreSpaceCount = 0
		self.bottomScoresText = str(self.player3Score)
		for i in range (0,self.scoreSpaceCount):
			self.bottomScoresText += ' '
		self.bottomScoresText += str(self.player4Score)

		# Append Prev Game Scores to Script
		script.append({'top':self.topScoresText,'bottom':self.bottomScoresText,'timer':7,'transition':0})

		##############
		#### Game Over
		##############
		script.append({'top':'GAME OVER','bottom':'PRESS START','timer':5,'transition':1})

		################
		#### High Scores
		################
		for category in self.game.highscore_categories:
			for index, score in enumerate(category.scores):
				score_str = locale.format("%d", score.score, True)
				ranking = str(index)
				name = str(score.inits)
				data={'score':score_str, 'ranking':ranking}

				#### Classic High Score Data ####
				if category.game_data_key == 'ClassicHighScoreData':
					if index == 0:
						text1 = 'GRAND CHAMPION'
						text2 = name + ' ' + score_str
					else:
						text1 = 'HIGH SCORE ' + ranking
						text2 = name + ' ' + score_str
				#### Mileage Champion ####
				elif category.game_data_key == 'MilesChampion':
					if index == 0:
						text1 = 'MILEAGE CHAMP'
						text2 = name + ' ' + score_str + ' MILES'

				script.append({'top':text1,'bottom':text2,'timer':5,'transition':1})

		#####################################################
		#### Previous Game Scores #2 ########################
		#### This is used to append the previous game scores 
		#### defined above to the script again after the high 
		#### scores have been displayed.
		##################################################### 
		script.append({'top':self.topScoresText,'bottom':self.bottomScoresText,'timer':7,'transition':0})

		###################
		#### Special Thanks
		###################
		script.append({'top':'SPECIAL THANKS','bottom':'MYPINBALLS','timer':3,'transition':1})
		script.append({'top':'SPECIAL THANKS','bottom':'MARK SUNNUCKS','timer':3,'transition':2})
		script.append({'top':'SPECIAL THANKS','bottom':'MULTIMORPHIC','timer':3,'transition':2})
		
		#############################
		#### Start New Display Script
		#############################
		#Cancel any score display scripts that may be running
		self.game.alpha_score_display.cancel_script()
		self.game.alpha_score_display.set_script(script)
		
	def startAttractLamps(self):
		##############################################################
		#### Start Attract Lamps Version 1 ###########################
		#### This basic attract lamp show uses a schedule to cycle 
		#### through the lamps in the game.  This surprisingly creates 
		#### a nice attract mode for those looking to get something 
		#### basic up and running.  It uses a mod function to cycle 
		#### through every 4 lamps.
		##############################################################
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
		##############################################################
		#### Start Attract Lamps Version 2 ###########################
		#### This basic attract lamp show uses a schedule to cycle 
		#### through the lamps in the game.  This surprisingly creates 
		#### a nice attract mode for those looking to get something 
		#### basic up and running.  It uses a mod function to cycle 
		#### through every 8 lamps.
		##############################################################
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

	def sw_outhole_closed(self, sw):
		return procgame.game.SwitchStop

	def sw_outhole_active_for_1s(self, sw):
		self.game.coils.acSelect.disable()
		self.game.coils.flipperEnable.disable()
		self.game.coils.outholeKicker_CaptiveFlashers.pulse(50)
		self.game.alpha_score_display.set_text("GAME OVER",0)
		self.game.alpha_score_display.set_text("PRESS START",1)
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

	#############################
	## Skillshot Switches
	#############################
	def sw_onRamp25k_active(self, sw):
		return procgame.game.SwitchStop

	def sw_onRamp50k_active(self, sw):
		return procgame.game.SwitchStop

	def sw_onRamp100k_active(self, sw):
		return procgame.game.SwitchStop

	def sw_onRampBypass_active(self, sw):
		return procgame.game.SwitchStop