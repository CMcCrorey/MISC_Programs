# -*- coding: utf-8 -*-

import numpy as np

#recently refernces ?

class Page_Table:
    def __init__(self):
        mem_address=[[None,None,None]]*128
        self.mem_address=np.array(mem_address)
      
        
       #returns line based on vpn# 
    def map_ret(self,address):
        return self.mem_address[address]
    
    def update(self,address,dirty,mem_location,ref):
         self.mem_address[address] =[dirty,mem_location,ref]
         
    def dirty_write(self,address,dirty):
         self.mem_address[address,0] =dirty
    
        
        
 
        
       