
from Page_Table import Page_Table
import numpy as np
import sys
import random
import time


#statistics to track
page_faults=0
dirty_page_writes=0
disc_ref=0
valids=0 #debugging
######################


#variable initialize  
address_to_remove =0
reference =0
TS =[time.time_ns()]*32
TE= [0]*32
########################



#GRAB TXT FILE INPUT
##############################   
f1=open("instructions.txt","r")
Mat=[]
Lines=f1.readlines()
for param in Lines:
    line =  str.split(param)
    Mat =  Mat + [line]    
Mat= np.array(Mat)

##############################




#MAIN MEMORY
#######################################################
#INIT block and Main memory    
Block=[0]*512  #512 bytes 
Block= np.array(Block)
num = 0
Memory=[]
while num  < 32:
    Memory= Memory + [Block]
    num = num + 1
Memory = np.array(Memory)
########################################################



#DISC ???
################

################



#PROGRAM SECTION
########################################################################################


#orders and removes duplicates of processes and puts them into array with instance of Page_table
process_manager_array=[]
proccess_num_array= Mat[:,0]
proccess_num_array = sorted(list(set(proccess_num_array)))
for Each_process in proccess_num_array:
    process_manager_array= process_manager_array + [Page_Table()]
      

    
    
for next_line in Mat:
    process_num=next_line[0]  #process #
    VPN= next_line[1]         # decimal num input
    R_W=next_line[2]          # R or W 
    PT_num = int(VPN) >> 9     # get VPN number
    
    
    if R_W =='W':
        dirty=1
       
    else:
        dirty=0
  
    
    
    Line_in_PT=process_manager_array[int(process_num)-1].map_ret(PT_num) #access line in page table
    
    if(Line_in_PT[1]== None):  #check for page fault
        page_faults=page_faults +1 
        disc_ref= disc_ref +1  #at least 1 since page fault
        
        #checking mem for free space
        for loc, space in enumerate(Memory):
            if space[0] == 0:    #checking  for each block if first byte == 00000001
                space[0]=1       #set bit to first byte to 1 since its now being used
                process_manager_array[int(process_num)-1].update(PT_num, dirty, loc,0) #update page table
                #place data in mem ?
                TE[loc]= time.time_ns() - TS[loc]
                No_free_space= False
                break
            else:    
                No_free_space=True        
              
        if  No_free_space:
            
           
            if dirty:           
                disc_ref= disc_ref +1  #another ref due to writeback to disc
                #dirty_page_writes = dirty_page_writes +1
                
            if sys.argv[1] == "Rand":  
                address_to_remove =random.randint(0, 31)
                #Temp=Memory[address_to_remove]
                #place in Disc
                process_manager_array[int(process_num)-1].update(PT_num, dirty, address_to_remove,0) #update page table
           
            
           
            elif sys.argv[1]== "FIFO": #memory is placed in order beging from 0 so oldest memory will be index +1
                  
                if (address_to_remove > 31):
                    address_to_remove=0
                else:    
                    Oldest_Mem = Memory[address_to_remove] 
                    page_faults=page_faults +1 
                    disc_ref= disc_ref +1 
                    #Temp = Oldest_Mem
                    #place in disc
                    process_manager_array[int(process_num)-1].update(PT_num, dirty, address_to_remove,0)    
                    address_to_remove = address_to_remove +1
                    
            elif sys.argv[1]== "LRU":
                  
                  LRU = TE.index(max(TE))
                  TE[LRU]=0 #reset time 
                 # Temp = Memory[LRU] 
                  process_manager_array[int(process_num)-1].update(PT_num, dirty, LRU,0)  
              
                
            else :
                print("invalid input")
                
                      
    
    else:
            TS =[time.time()]*32  #reset time
            valids= valids +1 #debugging 
            process_manager_array[int(process_num)-1].dirty_write(PT_num, dirty)  #update dirty page writes
            if dirty:
                dirty_page_writes = dirty_page_writes +1
       
            TE[Line_in_PT[1]]= time.time_ns() - TS[Line_in_PT[1]] #update time for used location
            
        
        

print(valids) 

print("Total number of page faults is :", page_faults)
print("Total number of dirty page writes is :", dirty_page_writes)
print("Total number of disc references is :", disc_ref)

f1.close()



    