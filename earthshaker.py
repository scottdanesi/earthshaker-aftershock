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
from time import strftime

###################################
# MODE IMPORTS
###################################
from base import *
from attract import *
import scoredisplay
from scoredisplay import AlphaScoreDisplay #test and see about converting this to *
from skillshot import *
from utilities import *
from tilt import *
from centerramp import *
from player import *
from ballsaver import *
from bonus import *
from droptargets import *
from collectzones import *
from spinner import *
from multiball import *
from trough import *

# Used to put commas in the score.
locale.setlocale(locale.LC_ALL, "")

################################################
# GLOBAL PATH VARIABLES
################################################
game_machine_type = 'wpcAlphanumeric'
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
settings_path = curr_file_path + "/config/settings.yaml"
game_data_path = curr_file_path + "/config/game_data.yaml"
game_data_template_path = curr_file_path + "/config/game_data_template.yaml"
settings_template_path = curr_file_path + "/config/settings_template.yaml"
game_machine_yaml = curr_file_path + "/config/es.yaml"
game_music_path = curr_file_path + "/assets/music/"
game_sound_path = curr_file_path + "/assets/sound/"
game_lampshows = curr_file_path + "/lamps/"

ballsPerGame = 3 # this will eventually be called from the config file

################################################
# GAME CLASS
################################################
class EarthshakerAftershock(game.BasicGame):
	def __init__(self, machine_type):
		super(EarthshakerAftershock, self).__init__(machine_type)
		self.load_config(game_machine_yaml)
		self.logging_enabled = True
		self.balls_per_game = ballsPerGame

		### Set Logging Info ###
		logging.basicConfig(filename='aftershockLog.txt',level=logging.INFO)

		#### Settings and Game Data ####
		self.load_settings(settings_template_path, settings_path)
		self.load_game_data(game_data_template_path, game_data_path)

		#update audit data on boot up time
		self.game_data['Time Stamps']['Last Boot-Up'] =str(strftime("%d %b %Y %H:%M"))
		if self.game_data['Time Stamps']['First Boot-Up']=='Not Set':
			self.game_data['Time Stamps']['First Boot-Up'] = self.game_data['Time Stamps']['Last Boot-Up']
		self.save_game_data()

	def reset(self):
		#super(EarthshakerAftershock, self).reset()

		self.ball = 0
		self.old_players = []
		self.old_players = self.players[:]
		self.players = []
		self.current_player_index = 0
		self.modes.modes = []
		self.shooter_lane_status = 0
		self.tiltStatus = 0

		#setup high scores
		self.highscore_categories = []

		#### Classic High Score Data ####
		cat = highscore.HighScoreCategory()
		cat.game_data_key = 'ClassicHighScoreData'
		self.highscore_categories.append(cat)

		#### Mileage Champ ####
		cat = highscore.HighScoreCategory()
		cat.game_data_key = 'MilesChampion'
		self.highscore_categories.append(cat)

		for category in self.highscore_categories:
			category.load_from_game(self)

		#### Setup Alphanumeric Display Controller ####
		self.alpha_score_display = AlphaScoreDisplay(self,0)
		self.modes.add(self.alpha_score_display)
		
		#### Setup Sound Controller ####
		self.sound = procgame.sound.SoundController(self)
		self.RegisterSound()

		#### Setup Lamp Controller ####
		self.lampctrl = procgame.lamps.LampController(self)
		self.lampctrlflash = procgame.lamps.LampController(self)
		self.RegisterLampshows()

		#### software version number ####
		self.revision = "1.0.0"

		#### Mode Definitions ####
		self.utilities = UtilitiesMode(self,0)
		self.trough = Trough(self,2000)
		self.base_mode = BaseGameMode(self,2)
		self.attract_mode = AttractMode(self,5)
		self.centerramp_mode = CenterRampMode(self,8)
		self.drops_mode = DropTargets(self,9)
		self.collect_mode = CollectZones(self,10)
		self.spinner_mode = Spinner(self,11)
		self.skillshot_mode = SkillshotMode(self,100)
		self.ballsaver_mode = BallSaver(self,199)
		self.tilt = Tilt(self,200)
		self.bonus_mode = Bonus(self,1000)
		self.multiball_mode = Multiball(self,101)
		
		#### Initial Mode Queue ####
		self.modes.add(self.utilities)
		self.modes.add(self.trough)
		self.modes.add(self.base_mode)

	def save_settings(self):
			super(EarthshakerAftershock, self).save_settings(settings_path)

	def save_game_data(self):
			super(EarthshakerAftershock, self).save_game_data(game_data_path)

	def RegisterSound(self):
		# Sound Settings:
		#self.sound.music_volume_offset = 10 #This will be hardcoded at 10 since I have external volume controls I will be using
		# Music Registration
		self.sound.register_music('main', game_music_path + 'music_001_main_loop.wav')
		self.sound.register_music('shooter', game_music_path + 'music_001_shooter_loop.wav')
		self.sound.register_music('multiball_intro', game_music_path + 'music_001_multiball_start.wav')
		self.sound.register_music('multiball_loop', game_music_path + 'music_001_multiball_loop.wav')
		#self.sound.register_music('main', game_music_path + 'music_001_main_loop.wav')
		#self.sound.register_music('shooter', game_music_path + 'music_001_shooter_loop.wav')
		#self.sound.register_music('main', game_music_path + 'music_002_main_loop.wav')
		#self.sound.register_music('shooter', game_music_path + 'music_002_shooter_loop.wav')
		# Sound FX Registration
		self.sound.register_sound('spinner', game_sound_path + 'spinner2.wav')
		self.sound.register_sound('super_spinner', game_sound_path + 'spinner3.wav')
		self.sound.register_sound('super_spinner_lit', game_sound_path + 'dirty_kick.wav')
		self.sound.register_sound('sling', game_sound_path + 'sling2.wav')
		self.sound.register_sound('jet', game_sound_path + 'jet_a.wav')
		self.sound.register_sound('skillshotAwarded', game_sound_path + 'skillshotAwarded.wav')
		self.sound.register_sound('centerRampEnter', game_sound_path + 'centerRampEntry.wav')
		self.sound.register_sound('centerRampComplete', game_sound_path + 'centerRampComplete.wav')
		# Tilt Sounds #
		self.sound.register_sound('tilt_fx', game_sound_path + 'tilt_stern.wav')
		self.sound.register_sound('tilt_vox', game_sound_path + 'vocal_tilt_killed_a_guy.wav')
		self.sound.register_sound('tilt_vox', game_sound_path + 'vocal_tilt_seriously.wav')
		self.sound.register_sound('tilt_vox', game_sound_path + 'vocal_tilt_wtf.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_easy_there.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_hey.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_watch_it.wav')
		# BallSaver Sounds #
		self.sound.register_sound('ball_saved', game_sound_path + 'vocal_ballsaver_1.wav')
		self.sound.register_sound('ball_saved', game_sound_path + 'vocal_ballsaver_2.wav')
		# Bonus Sounds #
		self.sound.register_sound('bonus_features', game_sound_path + 'bonus_feature.wav')
		self.sound.register_sound('bonus_total', game_sound_path + 'bonus_total.wav')
		self.sound.register_sound('bonus_music', game_music_path + 'music_001_bonus.wav',new_sound_volume=.5)
		# Zone Sounds #
		self.sound.register_sound('zone_na', game_sound_path + 'zone_na.wav')
		self.sound.register_sound('zone_awarded', game_sound_path + 'zone_awarded.wav')
		# Drop Sounds #
		self.sound.register_sound('drop', game_sound_path + 'drop_1.wav')
		# Outlane Sounds #
		self.sound.register_sound('outlane', game_sound_path + 'outlane1.wav')
		self.sound.register_sound('inlane', game_sound_path + 'zone_na2.wav')
		# Game Start Voice #
		self.sound.register_sound('game_start', game_sound_path + 'vocal_game_start_1.wav')
		self.sound.register_sound('game_start', game_sound_path + 'vocal_game_start_2.wav')
		self.sound.register_sound('game_start', game_sound_path + 'vocal_game_start_3.wav')
		self.sound.register_sound('game_start', game_sound_path + 'vocal_game_start_4.wav')
		# Game Start Car Sounds #
		self.sound.register_sound('game_start_rev', game_sound_path + 'car_rev_1.wav')
		self.sound.register_sound('game_start_takeoff', game_sound_path + 'car_takeoff_1.wav')
		# Player Voice #
		self.sound.register_sound('player_1_vox', game_sound_path + 'vocal_player_1.wav')
		self.sound.register_sound('player_2_vox', game_sound_path + 'vocal_player_2.wav')
		self.sound.register_sound('player_3_vox', game_sound_path + 'vocal_player_3.wav')
		self.sound.register_sound('player_4_vox', game_sound_path + 'vocal_player_4.wav')

		self.sound.set_volume(10)

	def RegisterLampshows(self):
		self.lampctrl.register_show('attract1', game_lampshows + 'attract_random.lampshow')
		self.lampctrl.register_show('center_ramp_1', game_lampshows + 'center_ramp_complete.lampshow')
		self.lampctrlflash.register_show('bonus_total', game_lampshows + 'bonus_total.lampshow')

	def create_player(self, name):
		return Player(name)
		
################################################
# GAME DEFINITION
################################################
game = EarthshakerAftershock(machine_type=game_machine_type)
game.reset()
game.run_loop()