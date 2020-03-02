"""
Python OOK Demodulate
Deserialize Sink

Takes a bit stream and uses a deleayd version of it as a strobe signal
"""

import numpy as np
import sys

from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, reset_limit = 2000):
        """reset_limit - expect next pulse within x number of samples"""
        gr.sync_block.__init__(
            self,
            name='Python OOK Demod',
            in_sig=[np.byte, np.byte], 
            out_sig=None
        )
        
	self.buffer = np.byte(0)
	self.count = 0
	self.timeout = 0
	self.reset_limit = reset_limit

    def work(self, input_items, output_items):
        
	if np.any(input_items[1][:] > 0):
        	for i in range (1, len(input_items[0])):
			self.timeout = self.timeout + 1
			if self.timeout == self.reset_limit and self.count > 0:
				sys.stdout.write("%x \n" % (self.buffer << (8 - self.count))) 
				self.buffer = 0
				self.count = 0
			if input_items[1][i] & 0x01 & ~input_items[1][i-1]:
				self.timeout = 0
				self.buffer = (self.buffer << 1) | (~input_items[0][i] & 0x01)
				self.count = self.count + 1

				if self.count == 8:
					sys.stdout.write("%x " % (self.buffer)) 		
					self.buffer = 0
					self.count = 0		
		
	else:
		if self.timeout > 0:
			self.timeout = 0
			if self.count > 0:
				sys.stdout.write("%x \n" % (self.buffer << (8 - self.count)))
				self.buffer = 0
				self.count = 0
			else:
				print ""
        return len(input_items[0])
	
