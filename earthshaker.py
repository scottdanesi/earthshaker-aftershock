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
##     __  ______    _____   __   _________    __  _________
##    /  |/  /   |  /  _/ | / /  / ____/   |  /  |/  / ____/
##   / /|_/ / /| |  / //  |/ /  / / __/ /| | / /|_/ / __/   
##  / /  / / ___ |_/ // /|  /  / /_/ / ___ |/ /  / / /___   
## /_/  /_/_/  |_/___/_/ |_/   \____/_/  |_/_/  /_/_____/   
##
#################################################################################

###################################
# SYSTEM IMPORTS
###################################
import procgame.game
import pinproc
import locale
import yaml
import sys
import os
import logging

###################################
# MODE IMPORTS
###################################
import base
from base import *
#import attract
#from attract import *
import scoredisplay
from scoredisplay import AlphaScoreDisplay

# Import and Setup Logging
logging.basicConfig(level=logging.WARN, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

################################################
# GLOBAL PATH VARIABLES
################################################
game_machine_type = 'wpcAlphanumeric'
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
user_game_data_path = curr_file_path + "/config/game_data.yaml"
game_data_defaults_path = curr_file_path + "/config/game_data_template.yaml"
settings_defaults_path = curr_file_path + "/config/settings_template.yaml"
user_settings_path = curr_file_path + "/config/user_settings.yaml"
game_machine_yaml = curr_file_path + "/config/es.yaml"
game_music_path = curr_file_path + "/assets/music/"
game_sound_path = curr_file_path + "/assets/sound/"

ballsPerGame = 3 # this will eventually be called from the config file

################################################
# GAME CLASS
################################################
class EarthshakerAftershock(game.BasicGame):
	def __init__(self, machine_type):
		super(EarthshakerAftershock, self).__init__(machine_type)
		self.load_config(game_machine_yaml)
		self.logging_enabled=True
		self.balls_per_game = ballsPerGame
		
		

		# Setup Sound Controller
		self.sound = procgame.sound.SoundController(self)
		self.RegisterSound()

	def reset(self):
		super(EarthshakerAftershock, self).reset()

		self.ball = 0
		self.old_players = []
		self.old_players = self.players[:]
		self.players = []
		self.current_player_index = 0
		self.modes.modes = []

		#Setup Alphanumeric Display Controller
		self.alpha_score_display = AlphaScoreDisplay(game=self,priority=1)

		# software version number
		self.revision = "1.0.0"

		#boot into Base Mode
		self.base_mode = BaseGameMode(game)
		self.modes.add(self.base_mode)
		
		#could potentially put Attract mode here too
		#self.attract_mode = AttractMode(game)
		#self.modes.add(self.attract_mode)

	def RegisterSound(self):
		self.sound.music_volume_offset = 10 #This will be hardcoded at 10 since I have external volume controls I will be using
		self.sound.register_music('main', game_music_path + 'test.mp3')
		self.sound.register_sound('spinner', game_sound_path + 'spinner.wav')
		
################################################
# GAME DEFINITION
################################################
game = EarthshakerAftershock(machine_type=game_machine_type)
game.reset()
game.run_loop()