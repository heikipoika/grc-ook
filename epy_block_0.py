"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds!!
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import sys

from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Deserialize PrintByte Sink',   # will show up in GRC
            in_sig=[np.byte, np.byte], 
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        #self.example_param = example_param
	self.buffer = np.byte(0)
	self.count = 0
	self.timeout = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
	if np.any(input_items[1][:] > 0):
        	for i in range (1, len(input_items[0])):
			self.timeout = self.timeout + 1
			if self.timeout == 2000 and self.count > 0:
				print self.buffer
				self.buffer = 0
				self.count = 0
			if input_items[1][i] & 0x01 & ~input_items[1][i-1]:
				self.timeout = 0
				#output_items[0][i] = (output_items[0][i-1] << 1) | input_items[0][i]
				self.buffer = (self.buffer << 1) | (~input_items[0][i] & 0x01)
				#print "strobe", input_items[1][i]
				self.count = self.count + 1
				#print self.count
				if self.count == 8:
					#output_items[0][:] = self.buffer
					sys.stdout.write("%x " % (self.buffer)) 		
					self.buffer = 0
					self.count = 0		
		#print "out", output_items[0][i]
		#print "out", self.buffer		
		#print "in", input_items[1][i]	
	#else:
	#print "nop"
	#print input_items[0][:]	
	#print self.count, output_items[0][:]
	else:
		if self.timeout > 0:
			self.timeout = 0
			if self.count > 0:
				print self.buffer
				self.buffer = 0
				self.count = 0
			else:
				print ""
        return len(input_items[0])
