"""
Serialize source

Takes a predefined string, and outputs it as a serial OOK coded bitsream.....
"""

import numpy as np
import sys
import pmt

from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, bitsInLast = 1, repeat = 5, gap = 40):
        """
        bitsInLast - Number of bits to send from tha last byte
        repeat - number of times to repeat the message
        gap = the gap to use between messages
        """
        
        gr.sync_block.__init__(
            self,
            name='Serialize Source', 
            in_sig=None, 
            out_sig=[np.byte]
        )
        
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
 
        self.bitsInLast = bitsInLast
	self.items = [np.byte(0xff), np.byte(0xff), np.byte(0xea), np.byte(0x80)] #ea on eb off
        self.sent = 0
        self.send = 0
	self.repeat = repeat
        self.gap = gap

    def work(self, input_items, output_items):
            
        retcnt = 0
        if ~self.sent & self.send & 0x01:
        
                if len(output_items[0]) > (len(self.items)*8*5+self.gap)*self.repeat:
                        
                        for x in range(0, self.repeat):
                                
                                #output_items[0][retcnt] = 1
                                #output_items[0][retcnt+1:retcnt+11] = 0
                                #retcnt = retcnt + 11
                                for i in range(0, len(self.items)):
                                        elem = self.items[i]
                                        last = 8
                                        if i == len(self.items)-1:
                                                last = self.bitsInLast
                                        #print i
                                        ##sys.stdout.write("%x " % (elem))
                                        for n in range(0,last):
                                                #sys.stdout.write("%i " % (n))
                                                #self.buffer.append(self.items[i] & 0x01) # [i*7+n]
                                                if elem & 0x80:
                                                        output_items[0][retcnt] = 1
                                                        output_items[0][retcnt+1:retcnt+5] = 0
                                                        retcnt = retcnt + 5
                                                        #output_items[0][retcnt] = 1
                                                        #output_items[0][retcnt+1:retcnt+6] = 0
                                                        #retcnt = retcnt + 6 
                                                else:
                                                        output_items[0][retcnt:retcnt+3] = 1
                                                        output_items[0][retcnt+5] = 0 
                                                        retcnt = retcnt + 5 
                                                        #output_items[0][retcnt] = 1
                                                        #output_items[0][retcnt+1:retcnt+3] = 0 
                                                        #retcnt = retcnt + 3 
                                                #output_items[0][i*7+n] = elem & 0x01
                                                elem =  elem << 1
                                                #retcnt = retcnt + 1
                                                #self.count = self.count + 1
                                #output_items[0][retcnt] = 1
                                #retcnt = retcnt + 1
                                output_items[0][retcnt:retcnt+self.gap] = 0
                                retcnt = retcnt + self.gap         
                                
                        self.sent = 1
                        self.send = 0 #forresten det kanske funka bara att det inte sags pa time sink
                        #print self.sent
        elif ~self.send & 0x01:
                self.sent = 0
                #self.send = 0
                #output_items[0][:] = 0
                #retcnt = len(output_items[0])
                retcnt = 0 
        else:
                #output_items[0][:] = 0
                #retcnt = len(output_items[0])
                retcnt = 0 
        #retcnt = self.count
        #self.count = 0
        #print self.buffer
        #output_items[0][0:len(self.buffer)] = 1
        #output_items[0][:] = 1
        #self.buffer[:] = []
        
        return retcnt

    def handle_msg(self, msg):
         self.items = bytearray.fromhex(pmt.symbol_to_string(msg))
         self.send = 1
