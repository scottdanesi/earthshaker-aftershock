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
from rightramp import *
from player import *
from ballsaver import *
from bonus import *
from droptargets import *
from collectzones import *
from spinner import *
from multiball import *
from trough import *
from jackpot import *
from shelter import *
from highscore import *
from bonusmultiplier import *
from switchtracker import *
from combo import *
from million import *
#from healthcheck import *

#### Mini Modes ####
from mode_1 import *
from mode_2 import *
from mode_3 import *
from mode_4 import *
from mode_5 import *
from mode_6 import *
from mode_7 import *
from mode_8 import *
from mode_9 import *

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
coinOp = -1

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
		#self.healthcheck_mode = HealthCheckMode(self,0)
		
		self.base_mode = BaseGameMode(self,2)
		self.attract_mode = AttractMode(self,5)
		self.centerramp_mode = CenterRampMode(self,7)
		self.rightramp_mode = RightRampMode(self,8)
		self.drops_mode = DropTargets(self,9)
		self.collect_mode = CollectZones(self,10)
		self.spinner_mode = Spinner(self,11)
		self.jackpot_mode = Jackpot(self,12)
		self.million_mode = Million(self,14)
		self.bonusmultiplier_mode = BonusMultiplier(self,98)
		self.shelter_mode = Shelter(self,99)
		self.skillshot_mode = SkillshotMode(self,100)
		self.multiball_mode = Multiball(self,101)
		self.combo_mode = Combo(self,102)
		self.ballsaver_mode = BallSaver(self,199)
		self.tilt = Tilt(self,200)
		self.bonus_mode = Bonus(self,1000)
		self.highscore_mode = HighScore(self,1001)
		self.switch_tracker_mode = SwitchTrackerMode(self,1999)
		self.trough = Trough(self,2000)

		#### Mini Mode Definitions ####
		self.mode_1 = Mode1(self,30)
		self.mode_2 = Mode2(self,31)
		self.mode_3 = Mode3(self,32)
		self.mode_4 = Mode4(self,33)
		self.mode_5 = Mode5(self,34)
		self.mode_6 = Mode6(self,35)
		self.mode_7 = Mode7(self,36)
		self.mode_8 = Mode8(self,37)
		self.mode_9 = Mode9(self,38)
		
		
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
		#self.sound.register_music('game_over', game_music_path + 'music_001_game_over.wav') #Fractal - Breathe
		#self.sound.register_music('game_over', game_music_path + 'music_003_highscore_loop.wav') #Fred V & Graphix - Hydra
		self.sound.register_music('highscore_loop', game_music_path + 'music_003_highscore_loop.wav')
		self.sound.register_music('game_over', game_music_path + 'music_002_game_over.wav') #Calvertron
		#self.sound.register_music('main', game_music_path + 'music_001_main_loop.wav')
		#self.sound.register_music('shooter', game_music_path + 'music_001_shooter_loop.wav')
		#self.sound.register_music('main', game_music_path + 'music_002_main_loop.wav')
		#self.sound.register_music('shooter', game_music_path + 'music_002_shooter_loop.wav')
		# Sound FX Registration
		self.sound.register_sound('spinner', game_sound_path + 'spinner2.wav')
		self.sound.register_sound('super_spinner', game_sound_path + 'spinner3.wav')
		self.sound.register_sound('super_spinner_lit', game_sound_path + 'spinner_super_enable.wav')
		self.sound.register_sound('sling', game_sound_path + 'sling2.wav')
		self.sound.register_sound('jet', game_sound_path + 'jet_a.wav')
		self.sound.register_sound('jet_super', game_sound_path + 'jet_c.wav')
		self.sound.register_sound('skillshotAwarded', game_sound_path + 'skillshotAwarded.wav')
		self.sound.register_sound('centerRampEnter', game_sound_path + 'centerRampEntry.wav')
		self.sound.register_sound('centerRampComplete', game_sound_path + 'centerRampComplete.wav')
		self.sound.register_sound('rightRampComplete', game_sound_path + 'sweep1.wav',new_sound_volume=.1) #Very loud sample
		# Tilt Sounds #
		self.sound.register_sound('tilt_fx', game_sound_path + 'tilt_stern.wav')
		self.sound.register_sound('tilt_vox', game_sound_path + 'vocal_tilt_killed_a_guy.wav')
		self.sound.register_sound('tilt_vox', game_sound_path + 'vocal_tilt_seriously.wav')
		self.sound.register_sound('tilt_vox', game_sound_path + 'vocal_tilt_wtf.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_easy_there.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_hey.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_watch_it.wav')
		self.sound.register_sound('warning_vox', game_sound_path + 'vocal_warning_chill.wav')
		# BallSaver Sounds #
		self.sound.register_sound('ball_saved', game_sound_path + 'vocal_ballsaver_2.wav')
		self.sound.register_sound('ball_saved', game_sound_path + 'vocal_ballsaver_3.wav')
		# Bonus Sounds #
		self.sound.register_sound('bonus_features', game_sound_path + 'bonus_feature_v8.wav')
		self.sound.register_sound('bonus_total', game_sound_path + 'bonus_total_v5.wav')
		self.sound.register_sound('bonus_music', game_music_path + 'music_001_bonus.wav',new_sound_volume=.5)
		self.sound.register_sound('bonus_multiplier_vox', game_sound_path + 'vocal_bonus_multiplier_increase.wav')
		# Zone Sounds #
		self.sound.register_sound('zone_na', game_sound_path + 'zone_na.wav')
		#self.sound.register_sound('zone_awarded', game_sound_path + 'zone_awarded.wav')
		self.sound.register_sound('zone_awarded', game_sound_path + 'earthquake1.wav',new_sound_volume=.8)
		# Drop Sounds #
		self.sound.register_sound('drop', game_sound_path + 'drop_1.wav')
		# Eject Sounds #
		self.sound.register_sound('eject', game_sound_path + 'eject4.wav')
		self.sound.register_sound('ejectsaucer', game_sound_path + 'eject5.wav')
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
		self.sound.register_sound('player_1_up_vox', game_sound_path + 'vocal_player_1_up.wav')
		self.sound.register_sound('player_2_up_vox', game_sound_path + 'vocal_player_2_up.wav')
		self.sound.register_sound('player_3_up_vox', game_sound_path + 'vocal_player_3_up.wav')
		self.sound.register_sound('player_4_up_vox', game_sound_path + 'vocal_player_4_up.wav')
		# Multiball Sounds #
		self.sound.register_sound('earthquake_1', game_sound_path + 'multiball_intro_earthquake_1.wav')
		self.sound.register_sound('main_loop_tape_stop', game_sound_path + 'music_001_main_loop_stop.wav',new_sound_volume=.5)
		self.sound.register_sound('short_out_1', game_sound_path + 'short_out_1.wav')
		self.sound.register_sound('short_out_2', game_sound_path + 'short_out_2.wav')
		self.sound.register_sound('super_jackpot_advance', game_sound_path + 'super_jackpot_advance.wav')
		# Ball Lock Vocals #
		self.sound.register_sound('ball_lock_1', game_sound_path + 'vocal_lock_ball_1.wav')
		self.sound.register_sound('ball_lock_2', game_sound_path + 'vocal_lock_ball_2.wav')
		# Jackpot Vocals #
		self.sound.register_sound('jackpot_instruction', game_sound_path + 'vocal_jackpot_instruction.wav')
		self.sound.register_sound('jackpot', game_sound_path + 'vocal_jackpot_1.wav')
		self.sound.register_sound('jackpot', game_sound_path + 'vocal_jackpot_2.wav')
		#self.sound.register_sound('jackpot', game_sound_path + 'vocal_lionman.wav')
		self.sound.register_sound('jackpot_increase', game_sound_path + 'vocal_jackpot_increase.wav')
		self.sound.register_sound('jackpot_lit', game_sound_path + 'vocal_jackpot_lit.wav')
		self.sound.register_sound('super_jackpot', game_sound_path + 'vocal_super_jackpot.wav')
		self.sound.register_sound('super_jackpot_lit', game_sound_path + 'vocal_super_jackpot_lit_2.wav')
		self.sound.register_sound('million_vocal', game_sound_path + 'vocal_million.wav')
		self.sound.register_sound('million_vocal_crazy', game_sound_path + 'vocal_million_crazy.wav')
		# Complete Shot Vocals #
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_encourage_greatshot.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_encourage_niceshot.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_lionman.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_bitchin.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_nice.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_awesome.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_awesome_shot.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_keep_it_up.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_encourage_killer.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_encourage_rad.wav')
		self.sound.register_sound('complete_shot', game_sound_path + 'vocal_encourage_rockin.wav')
		# Last Chance Million Vocals #
		self.sound.register_sound('lcm_lit', game_sound_path + 'vocal_last_chance_million_lit.wav')
		self.sound.register_sound('lcm_lit', game_sound_path + 'vocal_last_chance_million_lit_shoot_ramp.wav')
		self.sound.register_sound('lcm_missed', game_sound_path + 'vocal_better_luck_next_time.wav')
		# Right Ramp Vocals #
		self.sound.register_sound('shoot_rr', game_sound_path + 'vocal_shoot_right_ramp.wav')
		# Shelter Sounds #
		self.sound.register_sound('mode_select', game_sound_path + 'mode_select_beep2.wav')
		self.sound.register_sound('mode_selected', game_sound_path + 'mode_select_beep_selected.wav')
		# Shelter Sounds #
		self.sound.register_sound('captive_carnival', game_sound_path + 'captive_carnival_beep.wav')
		# Skillshot Sounds #
		self.sound.register_sound('shoot_captive_ball', game_sound_path + 'vocal_shoot_captive_ball.wav')
		# Combo Sounds #
		self.sound.register_sound('combo_swoosh', game_sound_path + 'combo_swoosh.wav')
		self.sound.register_sound('combo1', game_sound_path + 'combo1.wav')
		self.sound.register_sound('combo2', game_sound_path + 'combo2.wav')
		self.sound.register_sound('combo3', game_sound_path + 'combo3.wav')
		self.sound.register_sound('combo4', game_sound_path + 'combo4.wav')
		self.sound.register_sound('combo5', game_sound_path + 'combo5.wav')
		self.sound.register_sound('combo6', game_sound_path + 'combo6.wav')
		self.sound.register_sound('combo7', game_sound_path + 'combo7.wav')
		self.sound.register_sound('combo8', game_sound_path + 'combo8.wav')
		# Countdown Vocals #
		self.sound.register_sound('countdown_0_vox', game_sound_path + 'vocal_countdown_0.wav')
		self.sound.register_sound('countdown_1_vox', game_sound_path + 'vocal_countdown_1.wav')
		self.sound.register_sound('countdown_2_vox', game_sound_path + 'vocal_countdown_2.wav')
		self.sound.register_sound('countdown_3_vox', game_sound_path + 'vocal_countdown_3.wav')
		self.sound.register_sound('countdown_4_vox', game_sound_path + 'vocal_countdown_4.wav')
		self.sound.register_sound('countdown_5_vox', game_sound_path + 'vocal_countdown_5.wav')
		# High Score Vocals #
		self.sound.register_sound('great_score_vox', game_sound_path + 'vocal_great_score.wav')

		self.sound.set_volume(10)

	def RegisterLampshows(self):
		self.lampctrl.register_show('attract1', game_lampshows + 'attract_grow.lampshow')
		self.lampctrl.register_show('attract2', game_lampshows + 'attract_grow.lampshow')
		self.lampctrl.register_show('attract3', game_lampshows + 'attract_horizontal_sweep.lampshow')
		self.lampctrl.register_show('attract4', game_lampshows + 'attract_horizontal_sweep.lampshow')
		self.lampctrl.register_show('attract5', game_lampshows + 'attract_vertical_sweep.lampshow')
		self.lampctrl.register_show('attract6', game_lampshows + 'attract_vertical_sweep.lampshow')
		self.lampctrl.register_show('attract7', game_lampshows + 'attract_radar_ccw.lampshow')
		self.lampctrl.register_show('attract8', game_lampshows + 'attract_radar_ccw.lampshow')
		self.lampctrl.register_show('attract9', game_lampshows + 'attract_radar_cw.lampshow')
		self.lampctrl.register_show('attract10', game_lampshows + 'attract_radar_cw.lampshow')
		self.lampctrl.register_show('attract11', game_lampshows + 'attract_sweep_horizontalsparkle.lampshow')
		self.lampctrl.register_show('attract12', game_lampshows + 'attract_sweep_horizontalsparkle.lampshow')
		self.lampctrl.register_show('attract13', game_lampshows + 'attract_feature_a.lampshow')
		self.lampctrl.register_show('attract14', game_lampshows + 'attract_feature_a.lampshow')
		self.lampctrl.register_show('center_ramp_1', game_lampshows + 'centerramp_complete_a.lampshow')
		self.lampctrlflash.register_show('bonus_feat_left', game_lampshows + 'bonus_feature_left.lampshow')
		self.lampctrlflash.register_show('bonus_feat_right', game_lampshows + 'bonus_feature_right.lampshow')
		self.lampctrlflash.register_show('bonus_total', game_lampshows + 'bonus_total_a.lampshow')
		self.lampctrlflash.register_show('multiball_intro_1', game_lampshows + 'multiball_intro.lampshow')
		self.lampctrlflash.register_show('highscore_flash_loop', game_lampshows + 'highscore_loop_a.lampshow')
		self.lampctrl.register_show('right_ramp_1', game_lampshows + 'rightramp_complete_a.lampshow')
		self.lampctrl.register_show('right_ramp_eject', game_lampshows + 'right_ramp_eject.lampshow')
		self.lampctrl.register_show('jackpot', game_lampshows + 'jackpot_awarded_a.lampshow')
		self.lampctrl.register_show('skillshot', game_lampshows + 'skillshot_standard_awarded.lampshow')
		self.lampctrl.register_show('super_skillshot', game_lampshows + 'skillshot_super_awarded.lampshow')
		self.lampctrl.register_show('zone_collected', game_lampshows + 'zones_zonecollected_a.lampshow')

	def create_player(self, name):
		return Player(name)
		
################################################
# GAME DEFINITION
################################################
game = EarthshakerAftershock(machine_type=game_machine_type)
game.reset()
game.run_loop()