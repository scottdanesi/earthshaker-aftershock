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
##     ____  __    _____  ____________     ______________  ___________
##    / __ \/ /   /   \ \/ / ____/ __ \   / ___/_  __/   |/_  __/ ___/
##   / /_/ / /   / /| |\  / __/ / /_/ /   \__ \ / / / /| | / /  \__ \ 
##  / ____/ /___/ ___ |/ / /___/ _, _/   ___/ // / / ___ |/ /  ___/ / 
## /_/   /_____/_/  |_/_/_____/_/ |_|   /____//_/ /_/  |_/_/  /____/  
## 
#################################################################################

import procgame.game

class Player(procgame.game.Player):

	def __init__(self, name):
			super(Player, self).__init__(name)

			#create player stats
			self.player_stats = {}

			### General Stats ###
			self.player_stats['ball_in_play']=False

			### Bonus and Status ###
			self.player_stats['status']=''
			self.player_stats['bonus_x']=1

			### Ball Saver ###
			self.player_stats['ballsave_active']=False
			self.player_stats['ballsave_timer_active']=False

			### Skillshot ###
			self.player_stats['skillshot_active']=False
			self.player_stats['skillshot_x']=1
			#self.player_stats['skillshot_active']=False

			### Center Ramp Stats ###
			self.player_stats['miles']=0
			self.player_stats['center_shots']=0

			self.player_stats['fault_visits']=0
			self.player_stats['inlanes_made']=0
			self.player_stats['lock_lit']=False
			self.player_stats['multiball_ready']=False
			self.player_stats['multiball_started']=False
			self.player_stats['multiball_running']=False
			self.player_stats['balls_locked']=0
			self.player_stats['million_lit']=False
			self.player_stats['ball_start_time']=0
			self.player_stats['drop_banks_completed']=0
			self.player_stats['super_skillshots']=0
			self.player_stats['secret_skillshots']=0
			self.player_stats['modes_running']=False
			self.player_stats['spinner_level']=0