"""
Python OOK modulate
Serialize source

Takes a predefined string, and outputs it as a serial OOK coded bitsream.....
"""

import numpy as np
import pmt

from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, bitsInLast = 1, repeat = 5, gap = 40, hi_1 = 1, lo_1 = 4, hi_0 = 3, lo_0 = 2):
        """
        bitsInLast - Number of bits to send from tha last byte
        repeat - number of times to repeat the message
        gap = the gap to use between messages
        hi_1 = the number of 1 samples in a logic hi
        lo_1 = the number of 0 samples in a logic hi
        hi_0 = the number of 1 samples in a logic low
        lo_0 = the number of 0 samples in a logic low
        """
        
        gr.sync_block.__init__(
            self,
            name='Python OOK modulate', 
            in_sig=None, 
            out_sig=[np.byte]
        )
        
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
 
        self.bitsInLast = bitsInLast
	self.items = [np.byte]
        self.sent = 0
        self.send = 0
	self.repeat = repeat
        self.gap = gap
        self.hi_1 = hi_1
        self.lo_1 = lo_1
        self.hi_0 = hi_0
        self.lo_0 = lo_0 

    def work(self, input_items, output_items):
            
        retcnt = 0
        if ~self.sent & self.send & 0x01:
        
                if len(output_items[0]) > (len(self.items)*8*5+self.gap)*self.repeat:
                        
                        for x in range(0, self.repeat):
                                
                                for i in range(0, len(self.items)):
                                        elem = self.items[i]
                                        last = 8
                                        if i == len(self.items)-1:
                                                last = self.bitsInLast
                                        
                                        for n in range(0,last):

                                                if elem & 0x80:
                                                        output_items[0][retcnt:retcnt+self.hi_1] = 1
                                                        output_items[0][retcnt+self.hi_1:retcnt+self.hi_1 +self.lo_1] = 0
                                                        retcnt = retcnt + self.hi_1 + self.lo_1
                                                         
                                                else:
                                                        output_items[0][retcnt:retcnt+self.hi_0] = 1
                                                        output_items[0][retcnt+self.hi_0:retcnt+self.hi_0+self.lo_0] = 0 
                                                        retcnt = retcnt + self.hi_0 + self.lo_0
                                                        
                                                elem =  elem << 1
                                                
                                output_items[0][retcnt:retcnt+self.gap] = 0
                                retcnt = retcnt + self.gap         
                                
                        self.sent = 1
                        self.send = 0

        elif ~self.send & 0x01:
                self.sent = 0
                retcnt = 0 
        else:
                retcnt = 0 
        
        return retcnt

    def handle_msg(self, msg):
            self.items = bytearray.fromhex(pmt.symbol_to_string(msg))
            self.send = 1
