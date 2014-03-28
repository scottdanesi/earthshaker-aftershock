import pinproc

class AlphanumericDisplay(object):
	# Start at ASCII table offset 32: ' ' 
	asciiSegments = [0x0000,  # ' '
                         0x016a,  # '!' Random Debris Character 1
                         0x3014,  # '"' Random Debris Character 2
                         0x5d80,  # '#' Random Debris Character 3
                         0x00a4,  # '$' Random Debris Character 4
                         0x3270,  # '%' Random Debris Character 5
                         0x4640,  # '&' Random Debris Character 6
                         0x0200,  # '''
                         0x1400,  # '('
                         0x4100,  # ')'
                         0x7f40,  # '*'
                         0x2a40,  # '+'
                         0x8080,  # ','
                         0x0840,  # '-'
                         0x8000,  # '.'
                         0x4400,  # '/'
  
                         0x003f,  # '0'
                         0x0006,  # '1'
                         0x085b,  # '2'
                         0x084f,  # '3'
                         0x0866,  # '4'
                         0x086d,  # '5'
                         0x087d,  # '6'
                         0x0007,  # '7'
                         0x087f,  # '8'
                         0x086f,  # '9'
  
                         0x0821,  # ':' Random Debris Character 7
                         0x1004,  # ';' Random Debris Character 8
                         0x1c00,  # '<' Left Arrow
                         0x1386,  # '=' Random Debris Character 9
                         0x4140,  # '>' Right Arrow
                         0x0045,  # '?' Random Debris Character 10
                         0x4820,  # '@' Random Debris Character 11

                         0x0877,  # 'A'
                         0x2a4f,  # 'B'
                         0x0039,  # 'C'
                         0x220f,  # 'D'
                         0x0879,  # 'E'
                         0x0871,  # 'F'
                         0x083d,  # 'G'
                         0x0876,  # 'H'
                         0x2209,  # 'I'
                         0x001e,  # 'J'
                         0x1470,  # 'K'
                         0x0038,  # 'L'
                         0x0536,  # 'M'
                         0x1136,  # 'N'
                         0x003f,  # 'O'
                         0x0873,  # 'P'
                         0x103f,  # 'Q'
                         0x1873,  # 'R'
                         0x086d,  # 'S'
                         0x2201,  # 'T'
                         0x003e,  # 'U'
                         0x4430,  # 'V'
                         0x5036,  # 'W'
                         0x5500,  # 'X'
                         0x2500,  # 'Y'
                         0x4409,  # 'Z'

                         0x6004,  # '[' Random Debris Character 12
                         0x6411,  # '\' Random Debris Character 13
                         0x780a,  # ']' Random Debris Character 14
                         0x093a,  # '^' Random Debris Character 15
                         0x0008,  # '_'
                         0x2220,  # '`' Random Debris Character 16

                         0x0c56,  # 'a' Broken Letter a
                         0x684e,  # 'b' Broken Letter b
                         0x081c,  # 'c' Broken Letter c
                         0x380e,  # 'd' Broken Letter d
                         0x1178,  # 'e' Broken Letter e
                         0x4831,  # 'f' Broken Letter f
                         0x083d,  # 'g' Broken Letter g NOT CREATED YET
                         0x0854,  # 'h' Broken Letter h
                         0x2209,  # 'i' Broken Letter i NOT CREATED YET
                         0x001e,  # 'j' Broken Letter j NOT CREATED YET
                         0x1070,  # 'k' Broken Letter k
                         0x0038,  # 'l' Broken Letter l NOT CREATED YET
                         0x0536,  # 'm' Broken Letter m NOT CREATED YET
                         0x1136,  # 'n' Broken Letter n NOT CREATED YET
                         0x085c,  # 'o' Broken Letter o
                         0x0873,  # 'p' Broken Letter p NOT CREATED YET
                         0x103f,  # 'q' Broken Letter q NOT CREATED YET
                         0x1c72,  # 'r' Broken Letter r
                         0x116c,  # 's' Broken Letter s
                         0x2120,  # 't' Broken Letter t
                         0x003e,  # 'u' Broken Letter u NOT CREATED YET
                         0x4430,  # 'v' Broken Letter v NOT CREATED YET
                         0x5036,  # 'w' Broken Letter w NOT CREATED YET
                         0x5500,  # 'x' Broken Letter x NOT CREATED YET
                         0x2500,  # 'y' Broken Letter y NOT CREATED YET
                         0x4409   # 'z' Broken Letter z NOT CREATED YET
                        ]

	strobes = [8,9,10,11,12]
	full_intensity_delay = 350 # microseconds
	inter_char_delay = 40 # microseconds

	def __init__(self, aux_controller):
		"""Initializes the animation."""
		super(AlphanumericDisplay, self).__init__()

		self.aux_controller = aux_controller
		self.aux_index = aux_controller.get_index()

	def display(self, input_strings, intensities=[[1]*16]*2):

		strings = []

		# Make sure strings are at least 16 chars.
		# Then convert each string to a list of chars.
		for j in range(0,2):
			input_strings[j] = input_strings[j]
			if len(input_strings[j]) < 16: input_strings[j] += ' '*(16-len(input_strings[j]))
			strings += [list(input_strings[j])]

		# Make sure insensities are 1 or less
		for i in range(0,16):
			for j in range(0,2):
				if intensities[j][i] > 1: intensities[j][i] = 1

		commands = []
		segs = []
		char_on_time = []
		char_off_time = []

		# Initialize a 2x16 array for segments value
		segs = [[0] * 16 for i in xrange(2)]

		# Loop through each character
		for i in range(0,16):

			# Activate the character position (this goes to both displayas)
			commands += [pinproc.aux_command_output_custom(i,0,self.strobes[0],False,0)]

			for j in range(0,2):
				segs[j][i] = self.asciiSegments[ord(strings[j][i])-32]

				# Check for commas or periods.  
				# If found, squeeze comma into previous character.
				# No point checking the last character (plus, this avoids an
				# indexing error by not checking i+1 on the 16th char.
				if (i<15): 
					comma_dot = strings[j][i+1]
	                        	if comma_dot == "," or comma_dot == ".":
						segs[j][i] |= self.asciiSegments[ord(comma_dot)-32]
						strings[j].remove(comma_dot)
						# Append a space to ensure there are enough chars.
						strings[j].append(' ')
                                #character is 16 bits long, characters are loaded in 2 lots of 8 bits, for each display (4 enable lines total)
				commands += [pinproc.aux_command_output_custom(segs[j][i] & 0xff,0,self.strobes[j*2+1],False, 0)] #first 8 bits of characater data
				commands += [pinproc.aux_command_output_custom((segs[j][i]>> 8) & 0xff,0,self.strobes[j*2+2],False, 0)] #second 8 bits of characater data

                                char_on_time += [intensities[j][i] * self.full_intensity_delay]
				char_off_time += [self.inter_char_delay + (self.full_intensity_delay - char_on_time[j])]

			if char_on_time[0] < char_on_time[1]:
				first = 0
				second = 1
			else:
				first = 1
				second = 0

			# Determine amount of time to leave the other char on after the
			# first is off.
			between_delay = char_on_time[second] - char_on_time[first]

			# Not sure if the hardware will like a delay of 0
			# Use 2 to be extra safe.  2 microseconds won't affect display.
			if between_delay == 0: between_delay = 2

			# Delay until it's time to turn off the character with the lowest intensity
			commands += [pinproc.aux_command_delay(char_on_time[first])]
			commands += [pinproc.aux_command_output_custom(0,0,self.strobes[first*2+1],False,0)]
			commands += [pinproc.aux_command_output_custom(0,0,self.strobes[first*2+2],False,0)]

			# Delay until it's time to turn off the other character.
			commands += [pinproc.aux_command_delay(between_delay)]
			commands += [pinproc.aux_command_output_custom(0,0,self.strobes[second*2+1],False,0)]
			commands += [pinproc.aux_command_output_custom(0,0,self.strobes[second*2+2],False,0)]

			# Delay for the inter-digit delay.
			commands += [pinproc.aux_command_delay(char_off_time[second])]

		# Send the new list of commands to the Aux port controller.
		self.aux_controller.update(self.aux_index, commands)

		#for command in commands:
			#print "Aux Command: %s" % command
