import random, machine
from fonts import six_by_three_font, seven_by_four_font
from time import sleep_ms
import gc
try:
    import pyb
except ImportError:
    import machine as pyb

#Graduation cap class to control LED matrix functionality
class GradCap:
	def __init__(self):
		self.data_pin = 18			#pin one-wire interface is connected to 
		self.led_length = 14*14		#number of LEDs in matrix

		self.leds = WS2812(data_pin=self.data_pin, led_count=self.led_length, intensity=.45)	#WS2812B LED strip object

		#array of colors used by the sprites/text
		self.colors = { 0:(0,0,0),\
		#1:Green, 2:Red, 3:Blue
		1:(0,255,0), 2:(255,0,0), 3:(0,0,255), \
		#4:White (255,255,255), 5:Cherry (130,24,42), 6:Gray (165,165,165)
  		4:(255,255,255), 5:(255,48,84), 6:(10,6,6), \
  		#flame colors 7:red, 8:orange 192, 9:yellow
  		7:(255,35,35), 8:(255,120,0), 9:(255,255,0), \
  		#
  		10:(0,0,0), 11:(0,0,0), 12:(0,0,0), \
		}

	#display_6x3_text("ABCD", frame_speed=100)
	#display_6x3_text("ABCDAAAAAA")
	#display_6x3_text("HELLO WORLD")
	#display_6x3_text("Hello World! This thing is really working the way it is supposed to...", frame_speed=40)

	#function to display messages with 6x3 pixel fonts
	#takes a frame speed (time for a pixel to scroll left), colors 1 and 2 (1 bottom, 2 top), and whether text scrolls offscreen at end of message
	def display_6x3_text(self, message, frame_speed=250, color1=None, color2=None, scroll_off=True):
		
		#set default color values
		if not color1:
			color1 = self.colors[4]
		if not color2:
			color2 = self.colors[5]

		#create an empty matrix to store display binary numbers
		matrix = []
		#create 14 variables (create the rows of the matrix)
		for y in range(0,14):
			matrix.append(0)

		#iter through the message, getting the character
		for ch in message:
			#define the char at 0 initially, look for char in 6x3 font, overwrite var if char found
			ch_arr = [0b0]
			if ch in six_by_three_font:
				ch_arr = six_by_three_font[ch]
			#for column in pixel font (3 per char)
			for ch_seg in ch_arr:
				#iter through loop 14 times to shift each row to the left by 1 bit
				for m_ind in range(0,14):

					#if the index is less than 6 (top row)
					if m_ind < 6:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#place bottom row bit 14 into top row bit 1
						matrix[m_ind] |= (matrix[m_ind+8]&0b10000000000000)>>13

					#if the index is greater than 7 (bot row)
					if m_ind > 7:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#place new ch_seg bit into row
						matrix[m_ind] |= 1&(ch_seg>>(m_ind-8))

				#generate new matrix to build 1D array for WS2182B module
				new_matrix = []
				#move through matrix rows
				for m_ind, m_row in enumerate(matrix):
					#move through row columns
					for bit in range(0,14):
						#if row is even, invert row and isolate column bit
						if m_ind%2 == 0: 
							m_bit = (m_row>>(13-bit))&1
						#otherwise isolate column bit
						else:
							m_bit = (m_row>>(bit))&1

						#if row is less than 6 and bit is 1
						if m_ind < 6 and m_bit == 1:
							#add color 1 to array
							new_matrix.append(color1)
						#if row is greater than 7 and bit is 1
						elif m_ind > 7 and m_bit == 1:
							#add color 2 to array
							new_matrix.append(color2)
						#otherwise add no color to array
						else:
							new_matrix.append((0,0,0))

				#display new LED matrix and wait for frame_speed duration
				self.leds.show(new_matrix)
				sleep_ms(frame_speed)

		#if text is to scroll offscreen at the end of the message
		if scroll_off:
			#create iter for 28 indexes
			for pixels in range(0,28):
				#create iter to move through each matrix row
				for m_ind in range(0,14):

					#if the index is less than 6 (top row)
					if m_ind < 6:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#place bottom row bit 14 into top row bit 1
						matrix[m_ind] |= (matrix[m_ind+8]&0b10000000000000)>>13
					#if the index is greater than 7 (bot row)
					if m_ind > 7:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#add a 0 to row, will eventually clear bot and top row
						matrix[m_ind] |= 0

				#generate new matrix to build 1D array for WS2182B module
				new_matrix = []
				#move through matrix rows
				for m_ind, m_row in enumerate(matrix):
					#move through row columns
					for bit in range(0,14):
						#if row is even, invert row and isolate column bit
						if m_ind%2 == 0: 
							m_bit = (m_row>>(13-bit))&1
						#otherwise isolate column bit
						else:
							m_bit = (m_row>>(bit))&1

						#if row is less than 6 and bit is 1
						if m_ind < 6 and m_bit == 1:
							#add color 1 to array
							new_matrix.append(color1)
						#if row is greater than 7 and bit is 1
						elif m_ind > 7 and m_bit == 1:
							#add color 2 to array
							new_matrix.append(color2)
						#otherwise add no color to array
						else:
							new_matrix.append((0,0,0))

				#display new LED matrix and wait for frame_speed duration
				self.leds.show(new_matrix)
				sleep_ms(frame_speed)
				
	#display_7x4_text("ABCD", frame_speed=100)
	#display_7x4_text("ABCD")
	#display_7x4_text("ABCDAAAAAA")
	#display_7x4_text("HELLO WORLD")
	#display_7x4_text("Hello World", frame_speed=60)
	#display_7x4_text("Hello World! This thing is really working the way it is supposed to...", frame_speed=40)

	#function to display messages with 7x4 pixel fonts
	#takes a frame speed (time for a pixel to scroll left), colors 1 and 2 (1 bottom, 2 top), and whether text scrolls offscreen at end of message
	def display_7x4_text(self, message, frame_speed=250, color1=None, color2=None, scroll_off=True):
		
		#set default color values
		if not color1:
			color1 = self.colors[4]
		if not color2:
			color2 = self.colors[5]

		#make all characters in message uppercase
		message = message.upper()
		#create an empty matrix to store display binary numbers
		matrix = []
		#create 14 variables (create the rows of the matrix)
		for y in range(0,14):
			matrix.append(0)

		#iter through the message, getting the character
		for ch in message:
			#define the char at 0 initially, look for char in 6x3 font, overwrite var if char found
			ch_arr = [0b0]
			if ch in seven_by_four_font:
				ch_arr = seven_by_four_font[ch]
			#for column in pixel font (4 per char)
			for ch_seg in ch_arr:
				#iter through loop 14 times to shift each row to the left by 1 bit
				for m_ind in range(0,14):

					#if the index is less than 7 (top row)
					if m_ind < 7:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#place bottom row bit 14 into top row bit 1
						matrix[m_ind] |= (matrix[m_ind+7]&0b10000000000000)>>13
					#if the index is greater than 6 (bot row)
					if m_ind > 6:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#place new ch_seg bit into row
						matrix[m_ind] |= 1&(ch_seg>>(m_ind-7))

				#generate new matrix to build 1D array for WS2182B module
				new_matrix = []
				#move through matrix rows
				for m_ind, m_row in enumerate(matrix):
					#move through row columns
					for bit in range(0,14):
						#if row is even, invert row and isolate column bit
						if m_ind%2 == 0: 
							m_bit = (m_row>>(13-bit))&1
						#otherwise isolate column bit
						else:
							m_bit = (m_row>>(bit))&1

						#if row is less than 7 and bit is 1
						if m_ind < 7 and m_bit == 1:
							#add color 1 to array
							new_matrix.append(color1)
						#if row is greater than 6 and bit is 1
						elif m_ind > 6 and m_bit == 1:
							#add color 2 to array
							new_matrix.append(color2)
						#otherwise add no color to array
						else:
							new_matrix.append((0,0,0))

				#display new LED matrix and wait for frame_speed duration
				self.leds.show(new_matrix)
				sleep_ms(frame_speed)

		#if text is to scroll offscreen at the end of the message
		if scroll_off:
			#create iter for 28 indexes
			for pixels in range(0,28):
				#create iter to move through each matrix row
				for m_ind in range(0,14):

					#if the index is less than 7 (top row)
					if m_ind < 7:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#place bottom row bit 14 into top row bit 1
						matrix[m_ind] |= (matrix[m_ind+7]&0b10000000000000)>>13
					#if the index is greater than 6 (bot row)
					if m_ind > 6:
						#shift the row 1 bit left
						matrix[m_ind] = matrix[m_ind]<<1
						#add a 0 to row, will eventually clear bot and top row
						matrix[m_ind] |= 0

				#generate new matrix to build 1D array for WS2182B module
				new_matrix = []
				#move through matrix rows
				for m_ind, m_row in enumerate(matrix):
					#move through row columns
					for bit in range(0,14):
						#if row is even, invert row and isolate column bit
						if m_ind%2 == 0: 
							m_bit = (m_row>>(13-bit))&1
						#otherwise isolate column bit
						else:
							m_bit = (m_row>>(bit))&1

						#if row is less than 7 and bit is 1
						if m_ind < 7 and m_bit == 1:
							#add color 1 to array
							new_matrix.append(color1)
						#if row is greater than 6 and bit is 1
						elif m_ind > 6 and m_bit == 1:
							#add color 2 to array
							new_matrix.append(color2)
						#otherwise add no color to array
						else:
							new_matrix.append((0,0,0))

				#display new LED matrix and wait for frame_speed duration
				self.leds.show(new_matrix)
				sleep_ms(frame_speed)

	#function to display a sprite from "paint by numbers" input matrix
	#takes a data matrix, expects a 14x14 matrix with index value of color in colors array
	def display_sprite(self, data):
		#constructed 1D array
		const_data = []
		#move through each row in matrix
		for i, row in enumerate(data):
			#if index is 1
			if i%2 is 1:
				#reverse the row and iter through row
				for col_val in reversed(row):
					#append color tuple to const_data
					const_data.append(self.colors[col_val])
			else:
				#iter through row
				for col_val in row:
					#append color tuple to const_data
					const_data.append(self.colors[col_val])
		#display new LED matrix
		self.leds.show(const_data)

	#function to update LED intensity
	#takes a 0-100 integer
	def new_intensity(self, intens):
		#scale the value and update the display
		self.leds.intensity = intens/100
		self.leds.show([])

	#function to clear the display
	def clear(self):
		self.leds.show([])	

#Class to handle the WS2812B one-wire communications
class WS2812:
    buf_bytes = (0x88, 0x8e, 0xe8, 0xee)

    def __init__(self, data_pin, led_count=1, intensity=1):
        """
        Params:
        * spi_bus = SPI bus ID (1 or 2)
        * led_count = count of LEDs
        * intensity = light intensity (float up to 1)
        """
        self.led_count = led_count
        self.intensity = intensity

        # prepare SPI data buffer (4 bytes for each color)
        self.buf_length = self.led_count * 3 * 4
        self.buf = bytearray(self.buf_length)

        # SPI init
        self.spi = pyb.SPI(1, baudrate=3200000, polarity=0, phase=1,mosi=machine.Pin(data_pin))

        # turn LEDs off
        self.show([])

    def show(self, data):
        """
        Show RGB data on LEDs. Expected data = [(R, G, B), ...] where R, G and B
        are intensities of self.colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        """
        Send buffer over SPI.
        """
        self.spi.write(self.buf)
        gc.collect()

    def update_buf(self, data, start=0):
        """
        Fill a part of the buffer with RGB data.

        Order of self.colors in buffer is changed from RGB to GRB because WS2812 LED
        has GRB order of self.colors. Each color is represented by 4 bytes in buffer
        (1 byte for each 2 bits).

        Returns the index of the first unfilled LED

        Note: If you find this function ugly, it's because speed optimisations
        beated purity of code.
        """

        buf = self.buf
        buf_bytes = self.buf_bytes
        intensity = self.intensity

        mask = 0x03
        index = start * 12
        #print(data)
        for red, green, blue in data:
            red = int(red * intensity)
            green = int(green * intensity)
            blue = int(blue * intensity)

            buf[index] = buf_bytes[green >> 6 & mask]
            buf[index+1] = buf_bytes[green >> 4 & mask]
            buf[index+2] = buf_bytes[green >> 2 & mask]
            buf[index+3] = buf_bytes[green & mask]

            buf[index+4] = buf_bytes[red >> 6 & mask]
            buf[index+5] = buf_bytes[red >> 4 & mask]
            buf[index+6] = buf_bytes[red >> 2 & mask]
            buf[index+7] = buf_bytes[red & mask]

            buf[index+8] = buf_bytes[blue >> 6 & mask]
            buf[index+9] = buf_bytes[blue >> 4 & mask]
            buf[index+10] = buf_bytes[blue >> 2 & mask]
            buf[index+11] = buf_bytes[blue & mask]

            index += 12

        return index // 12

    def fill_buf(self, data):
        """
        Fill buffer with RGB data.

        All LEDs after the data are turned off.
        """
        end = self.update_buf(data)

        # turn off the rest of the LEDs
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 12, self.buf_length):
            buf[index] = off
            index += 1		