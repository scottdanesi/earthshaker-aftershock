import procgame
import locale
import random
import logging
from procgame import *


#class AttractLayer(dmd.GroupedLayer):
#	def __init__(self, width, height, mode):
#		super(AttractLayer, self).__init__(width, height, mode)
#		self.mode = mode
#	def next_frame(self):
#		"""docstring for next_frame"""
#		# Setup for the frame.
#		self.mode.update_script()
#		return super(AttractLayer, self).next_frame()

class AlphaScoreDisplay(game.ScoreDisplay):
	
	def __init__(self, game, priority, left_players_justify="right"):
		super(AlphaScoreDisplay, self).__init__(game, priority)

                self.log = logging.getLogger('whirlwind.alpha_display')
                
                #set the position of the rhs of score for each player
                self.player_score_posn=[6,15,6,15]

                #flag for display text
                self.text_set = False

                #set the starting point for a rhs transition
                self.transition_posn = 17

                self.transition_reveal_posn =0

                self.text_blink_repeat = None



                #reset the display
                self.reset()

        def reset(self):
                #cancel any delays
                self.cancel_delayed(self.text_blink_repeat)
                
                #define the display data lists
                self.top_text_data=[]
                self.bottom_text_data=[]
                for i in range(16):
                    self.top_text_data.append(' ')
                    self.bottom_text_data.append(' ')
                    
                #update the data
                self.update_alpha_display()

        def mode_tick(self):
            if self.text_set==False:
                self.update_layer()
            
            
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
                    self.bottom_text_data[posn:posn+len(text)] = text
                  
                    #update the data
                    self.update_alpha_display()

	def update_layer_1p(self, font=None):
                super(AlphaScoreDisplay, self).update_layer_1p(font)
                if self.game.current_player() == None:
			score = 0 # Small hack to make *something* show up on startup.
		elif self.game.ball>0:
			score = self.format_digit_score(self.game.current_player().score)
                        posn = self.player_score_posn[0]+1
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

            elif row==1:
                if opaque:
                    for i in range(16):
                        self.bottom_text_data[i] = ' '
                self.bottom_text_data[posn-size:posn]=text

            
            self.update_alpha_display()

            if seconds>0:
                self.delay(name='restore_display',delay=seconds,handler=self.restore)

            if blink_rate>0:
                #store the current text data
                self.top_text_data_store = self.top_text_data
                self.bottom_text_data_store = self.bottom_text_data
                #call the blinker method
                self.set_text_blink(blink_rate)
            else:
                self.cancel_delayed(self.text_blink_repeat)

		def set_text_blink(self,num):
			def clear(self):
				for i in range(16):
					self.top_text_data[i] = ' '
					self.bottom_text_data[i] = ' '

				#update the data
				self.update_alpha_display()

			def restore(self):
				for i in range(16):
					self.top_text_data = self.top_text_data_store
					self.bottom_text_data = self.bottom_text_data_store
				#update the data
				self.update_alpha_display()

			#Added by Scott Danesi to properly set the default blink flag
			self.blink_flag = True
			if self.blink_flag:
				clear()
				self.blink_flag=False
			else:
				restore()
				self.blink_flag=True
			#Added by Scott Danesi to properly set the default blink flag
			#blink_flag = (not blink_flag)
			self.text_blink_repeat = self.delay(delay=num,handler=self.set_text_blink, param=num)

		

        def set_script(self,data): #set up a sequence of text calls to loop
            self.log.info('display script called')
            i=0
            for item in data:

                def wrapper(item,i): # Use wrapper() to capture the values of item.
                    self.log.info('script item is:%s',item)
                    if item['transition']==0:
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_text(item['top'],0,justify='center'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_text(item['bottom'],1,justify='center'))
                    elif item['transition']==1:
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_transition_in(item['top'],0,justify='left'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_transition_in(item['bottom'],1,justify='left'))
                    elif item['transition']==2:
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_text(item['top'],0,justify='center'))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_transition_in(item['bottom'],1,justify='center'))
                    elif item['transition']==3:
                        self.__top_delay = self.delay(name='display_script_ttext', delay=i,handler=lambda: self.set_transition_reveal(item['top'],0))
                        self.__bottom_delay = self.delay(name='display_script_btext', delay=i,handler=lambda: self.set_transition_reveal(item['bottom'],1))
                    
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
            stop_posn = 0

            text_data=[]
            for i in range(0,32):
                text_data.append(' ')
            text_data[self.transition_posn:self.transition_posn+size] = text

            if row==0:
                self.top_text_data=text_data[0:16]
            elif row==1:
                self.bottom_text_data=text_data[0:16]

            self.update_alpha_display()
            self.transition_posn -=1

            if self.transition_posn>stop_posn:
                self.delay(name='transition_loop',delay=0.01,handler=lambda:self.set_transition_in(text,row,justify,seconds))
            else:
                self.cancel_delayed('transition_loop')
                self.transition_posn = 17
                if seconds>0:
                    self.delay(name='restore_display',delay=seconds,handler=self.restore)

        def set_transition_reveal(self,text,row,seconds=0):
            size = len(text)
            reveal_text = text[size/2-self.transition_reveal_posn:size/2+self.transition_reveal_posn]
            reveal_size = len(reveal_text)
            posn = 8+reveal_size/2

            text_data=[]
            for i in range(0,16):
                text_data.append(' ')

            text_data[posn-reveal_size:posn] = reveal_text

            if row==0:
                self.top_text_data=text_data
            elif row==1:
                self.bottom_text_data=text_data

            self.update_alpha_display()

            self.transition_reveal_posn +=1

            if self.transition_reveal_posn>size/2:
                self.delay(name='transition_loop',delay=0.01,handler=lambda:self.set_transition_reveal(text,row,seconds))
            else:
                self.cancel_delayed('transition_loop')
                self.transition_reveal_posn = 0
                if seconds>0:
                    self.delay(name='restore_display',delay=seconds,handler=self.restore)


	def update_alpha_display(self):
            #using gerry's builtin procgame method for now
            #write the data to the display
            self.game.alpha_display.display([''.join(self.top_text_data),''.join(self.bottom_text_data)])


