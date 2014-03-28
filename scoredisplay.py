# -------------------------------------------------------------------------------------
# _______         _____  _     _ _______
# |_____| |      |_____] |_____| |_____|
# |     | |_____ |       |     | |     |
#                                       
# _______ _______  _____   ______ _______
# |______ |       |     | |_____/ |______
# ______| |_____  |_____| |    \_ |______
#                                        
# ______  _____ _______  _____         _______ __   __
# |     \   |   |______ |_____] |      |_____|   \_/  
# |_____/ __|__ ______| |       |_____ |     |    |   
#
# -------------------------------------------------------------------------------------
# Score Display Mode for Alphanumeric Display Games
#
# Controls displays during game play and provides various transition effects for 
# displaying text during modes.
# 
# Repeating script list included for attract usage
#
# Copyright (C) 2013 myPinballs, Orange Cloud Software Ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# -------------------------------------------------------------------------------------
#  _______  ______ _______ __   _ _______ _____ _______ _____  _____  __   _ _______
#     |    |_____/ |_____| | \  | |______   |      |      |   |     | | \  | |______
#     |    |    \_ |     | |  \_| ______| __|__    |    __|__ |_____| |  \_| ______|
# 
# -------------------------------------------------------------------------------------
# Transition 0: Fixed top and bottom, centered
# Transition 1: Slide in top and bottom, from right to left, left justified
# Transition 2: Fixed top, slide in bottom from right to left, centered
# Transition 3: Reveal out from center top and bottom, centered
# Transition 4: Fixed top, flashing bottom, centered
# -------------------------------------------------------------------------------------


import procgame
import locale
import random
import logging
from procgame import *


class AlphaScoreDisplay(game.ScoreDisplay):
	
	def __init__(self, game, priority, left_players_justify="right"):
		super(AlphaScoreDisplay, self).__init__(game, priority)

                self.log = logging.getLogger('whirlwind.alpha_display')
                
                #set the position of the rhs of score for each player
                self.player_score_posn=[8,15,8,15]


                #set the starting point for a rhs transition
                self.transition_posn = [17,17]

                self.transition_reveal_posn = [0,0]

                #flags
                self.blink_flag = False
                self.text_set = False

                #reset the display
                self.reset()

        def reset(self):
                self.log.debug('reset called')
                #cancel any delays
                for i in range(2):
                    self.cancel_delayed('text_blink_repeat'+str(i))
                    self.cancel_delayed('transition_loop'+str(i))
                
                #define the display data lists
                self.top_text_data=[]
                self.bottom_text_data=[]
                for i in range(16):
                    self.top_text_data.append(' ')
                    self.bottom_text_data.append(' ')

                self.top_text_data_store=[]
                self.bottom_text_data_store=[]
                for i in range(16):
                    self.top_text_data_store.append(' ')
                    self.bottom_text_data_store.append(' ')

                #setup the display data store lists
                #self.top_text_data_store = self.top_text_data
                #self.bottom_text_data_store = self.bottom_text_data
                    
                #update the data
                self.update_alpha_display()


#        def mode_tick(self):
#            if self.text_set==False:
#                self.update_layer()
            
            
        def test(self):
            self.set_text('whirlwind'.upper(),0)

        def restore(self):
                self.reset()
                self.text_set = False
                self.update_layer()

        def format_digit_score(self, score):
	
		if score == 0:
			return '00'
		else:
			return locale.format("%d", score, True)

        def update_layer(self):
                super(AlphaScoreDisplay, self).update_layer()

		if self.game.ball >0:
                    text = "BALL %d" % (self.game.ball)
                    if self.game.current_player_index<3: #move text if player 4
                        posn = 9
                    else:
                        posn = 0
                   
                    if not self.text_set:
                        self.bottom_text_data[posn:posn+len(text)] = text
                        #update the data
                        self.update_alpha_display()

	def update_layer_1p(self):
                super(AlphaScoreDisplay, self).update_layer_1p()
                if self.game.current_player() == None:
			score = 0 # Small hack to make *something* show up on startup.
		elif self.game.ball>0:
			score = self.format_digit_score(self.game.current_player().score)
                        posn = self.player_score_posn[0]+1

                        if not self.text_set:
                            #add the score as right justified in player 1s posn
                            self.top_text_data[posn-len(score):posn] = score
                            #update the data
                            self.update_alpha_display()
                        
        def update_layer_4p(self):
                super(AlphaScoreDisplay, self).update_layer_4p()
		for i in range(len(self.game.players[:4])): # Limit to first 4 players for now.
			score = self.game.players[i].score
                        formatted_score = self.format_digit_score(score)
                        #adjust posn for scores bigger than 10 Mil on players 1 and 3
                        if score>=10000000 and (i==0 or i==2):
                            posn = self.player_score_posn[i]+1
                        else:
                            posn = self.player_score_posn[i]

                        if not self.text_set:
                            #add the scores as right justified for the num of players playing, players 1 and 2 on top, 3 and 4 on bottom
                            if i<2:
                                self.top_text_data[posn-len(formatted_score):posn] = formatted_score
                            else:
                                self.bottom_text_data[posn-len(formatted_score):posn] = formatted_score

                            #update the data
                            self.update_alpha_display()


        def set_text(self,text,row,justify='center',opaque=True,blink_rate=0,seconds=0):
            self.text_set = True

            size = len(text)
            posn = 0
            if justify=='left':
                posn = len(text)
            elif justify=='right':
                posn =16
            elif justify=='center':
                posn = 8+size/2

            if row==0:
                if opaque:
                    for i in range(16):
                        self.top_text_data[i] = ' '
                self.top_text_data[posn-size:posn]=text
                self.top_text_data_store[posn-size:posn] = text

            elif row==1:
                if opaque:
                    for i in range(16):
                        self.bottom_text_data[i] = ' '
                self.bottom_text_data[posn-size:posn]=text
                self.bottom_text_data_store[posn-size:posn]=text

            
            #check for blinking enabled
            if blink_rate>0:
                #store the current text data
                #self.top_text_data = self.top_text_data_store
                #self.bottom_text_data_store = self.bottom_text_data

                #call the blinker method
                self.blink_flag = True
                self.set_text_blink([blink_rate,row])
            else:
                self.cancel_delayed('text_blink_repeat'+str(row))
                self.update_alpha_display()

            #timer to restore the scores
            if seconds>0:
                self.delay(name='restore_display',delay=seconds,handler=self.restore)


        def set_text_blink(self,data):
            delay=data[0]
            row=data[1]

            self.log.debug('Top text data store contains:%s',self.top_text_data_store)
                   
            def clear(self):
                for i in range(16):
                    if row==0:
                        self.top_text_data[i] = ' '
                    elif row==1:
                        self.bottom_text_data[i] = ' '

                #update the data
                self.update_alpha_display()

            def restore(self):
                if row==0:
                    for i in range(len(self.top_text_data_store)):
                        self.top_text_data[i] = self.top_text_data_store[i]
                elif row==1:
                    for i in range(len(self.bottom_text_data_store)):
                        self.bottom_text_data[i] = self.bottom_text_data_store[i]

                #update the data
                self.update_alpha_display()

            if self.blink_flag:
                clear(self)
                self.blink_flag=False
                self.log.debug('blinking, cleared')
            else:
                restore(self)
                self.blink_flag=True
                self.log.debug('blinking, restored')

            self.delay(name='text_blink_repeat'+str(row),delay=delay,handler=self.set_text_blink, param=data)


        def set_script(self,data): #set up a sequence of text calls to loop
            self.log.debug('display script called')
            i=0
            for item in data:

                def wrapper(item,i): # Use wrapper() to capture the values of item.
                    self.log.info('script item is:%s',item)
                    if item['transition']==0: # fixed top and bottom, centered
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_text(item['top'],0,justify='center'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_text(item['bottom'],1,justify='center'))
                    elif item['transition']==1: #slide in top and bottom, from right to left
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_transition_in(item['top'],0,justify='left'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_transition_in(item['bottom'],1,justify='left'))
                    elif item['transition']==2: #fixed top, slide in bottom, centered
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_text(item['top'],0,justify='center'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_transition_in(item['bottom'],1,justify='center'))
                    elif item['transition']==3: # reveal out from center top and bottom
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_transition_reveal(item['top'],0))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_transition_reveal(item['bottom'],1))
                    elif item['transition']==4: # fixed top, flashing bottom, centered
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_text(item['top'],0,justify='center'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_text(item['bottom'],1,justify='center',blink_rate=0.2))                        
                        
                wrapper(item,i)
                i+=item['timer']
            repeat_delay =self.delay(name='display_script_repeat',delay=i,handler=self.set_script,param=data)


        def cancel_script(self):
            self.cancel_delayed('display_script_ttext')
            self.cancel_delayed('display_script_btext')
            self.cancel_delayed('display_script_repeat')
            self.restore()
            

        def set_transition_in(self,text,row,justify='left',seconds=0):
            size = len(text)

            if justify=='left':
                stop_posn = 0
            elif justify=='center':
                stop_posn = 8-(size/2)
            elif justify=='right':
                stop_posn = 15-size

            text_data=[]
            for i in range(0,32):
                text_data.append(' ')
            text_data[self.transition_posn[row]:self.transition_posn[row]+size] = text

            if row==0:
                self.top_text_data=text_data[0:16]
            elif row==1:
                self.bottom_text_data=text_data[0:16]

            self.update_alpha_display()
            self.transition_posn[row] -=1

            if self.transition_posn[row]>=stop_posn:
                self.delay(name='transition_loop'+str(row),delay=0.03,handler=lambda:self.set_transition_in(text,row,justify,seconds))
            else:
                self.cancel_delayed('transition_loop'+str(row))
                self.transition_posn[row] = 17
                if seconds>0:
                    self.delay(name='restore_display',delay=seconds,handler=self.restore)


        def set_transition_reveal(self,text,row,seconds=0):
            size = len(text)
            
            #create curtain
            curtain_text = '!"#$%&'
            curtain=''
            if self.transition_reveal_posn[row]<=(size/2):
                for i in range(3):
                    curtain += random.choice(curtain_text)

            reveal_text = curtain+text[(size/2)+1-self.transition_reveal_posn[row]:(size/2)+1+self.transition_reveal_posn[row]]+curtain
            self.log.debug('%s %s',text,reveal_text)

            #work out end posn
            reveal_size = len(reveal_text)
            posn = 8+(reveal_size/2)

            #create full text data
            text_data=[]
            for i in range(0,16):
                text_data.append(' ')

            text_data[posn-reveal_size:posn] = reveal_text

            #set text to correct row
            if row==0:
                self.top_text_data=text_data
            elif row==1:
                self.bottom_text_data=text_data

            #write data to the display
            self.update_alpha_display()
            #inc counter
            self.transition_reveal_posn[row] +=1
            
            #repeat or cancel and reset?
            if self.transition_reveal_posn[row]<=(size/2)+1:
                self.delay(name='transition_loop'+str(row),delay=0.05,handler=lambda:self.set_transition_reveal(text,row,seconds))
            else:
                self.cancel_delayed('transition_loop'+str(row))
                self.transition_reveal_posn[row] = 0
                if seconds>0:
                    self.delay(name='restore_display',delay=seconds,handler=self.restore)

            


	def update_alpha_display(self):
            #using gerry's builtin procgame method for now
            #write the data to the display
            self.game.alpha_display.display([''.join(self.top_text_data),''.join(self.bottom_text_data)])
            #debug
            self.log.debug('top text:%s',self.top_text_data)
            self.log.debug('bottom text:%s',self.bottom_text_data)
