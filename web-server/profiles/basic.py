import sys
from random import randrange
import numpy
import time
def action_peek(cattoiState,period,duty):
   cattoiState['config']['LED0']=(0,64,64)
   cattoiState['profile']['period'] = int(period)
   cattoiState['profile']['duty']=duty
   cattoiState['profile']['c0_max'] = 50
   cattoiState['profile']['c0']=0
   cattoiState['profile']['name'] = "peek"
   
def ARGB_peek(cattoiState,pixels):
   cattoiState['config']['LED0']=(0,64,64)
   while(abs(cattoiState['profile']['c0'])>0):
      if(cattoiState['profile']['name']!="peek"):return
      cattoiState['profile']['c0']=cattoiState['profile']['c0']-1
      peek_c0= cattoiState['profile']['c0']/cattoiState['profile']['c0_max']
      pixels.fill((0,0,0))
      pixels[cattoiState['profile']['focus']]=(0,0,int(numpy.interp(peek_c0,[0,cattoiState['profile']['duty']/100,cattoiState['profile']['duty']/100,1],[128,32,0,0])))
      pixels[0]=cattoiState['config']['LED0']
      pixels.show()
      time.sleep(cattoiState['profile']['period']/1000)   
   if(cattoiState['config']['debugLevel']>1): print("c0 Reset", file=sys.stderr)
   cattoiState['profile']['c0']=cattoiState['profile']['c0_max']
   cattoiState['profile']['focus']=randrange(cattoiState['config']['size']-1)+1

def action_shift(cattoiState,period,wide,step):
   cattoiState['config']['LED0']=(0,0,64)
   cattoiState['profile']['period'] = int(period)
   cattoiState['profile']['wide'] = int(wide)
   cattoiState['profile']['step'] = int(step)
   cattoiState['profile']['c0']=1
   cattoiState['profile']['focus']=cattoiState['config']['size']
   cattoiState['profile']['name'] = "shift" 
         
def ARGB_shift(cattoiState,pixels):
   cattoiState['config']['LED0']=(0,0,64)
   step=cattoiState['profile']['step']
   while(abs(cattoiState['profile']['focus']-cattoiState['profile']['c0'])>step):
      if(cattoiState['profile']['name']!="shift"):return
      pixels.fill((0,0,0))
      if(cattoiState['profile']['focus']>cattoiState['profile']['c0']):
         cattoiState['profile']['focus']=cattoiState['profile']['focus']-step
      else:
         cattoiState['profile']['focus']=cattoiState['profile']['focus']+step
      cattoiState['profile']['focus'] = min(max(cattoiState['profile']['focus'],1),cattoiState['config']['size']-1)
      
      f0=cattoiState['profile']['focus']
      brightness=128
      frange=[0,1,-1,2,-2,3,-3,4,-4,5,-5]
      # for i in range(1,cattoiState['profile']['wide']):
         # frange.insert(len(frange),i)
         # frange.insert(len(frange),-1*i)
      # if(cattoiState['config']['debugLevel']>0): print("frange" + str(frange), file=sys.stderr)


      fn=0
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=-1
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=1
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=-2
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=2
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=-3
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=3
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=-4
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      
      fn=4
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      fn=-5
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
      fn=-5
      if(min(max(int(f0)+int(fn),1),cattoiState['config']['size']-1)==(int(f0)+int(fn)) and (abs(fn) < cattoiState['profile']['wide']) ):pixels[int(f0)+int(fn)]=(0,0,int(brightness/(abs(fn)+1)))
            
      
      pixels[0]=cattoiState['config']['LED0']
      pixels.show()
      time.sleep(cattoiState['profile']['period']/1000)   
   cattoiState['profile']['c0']=  randrange(cattoiState['config']['size']-1)+1
   if(cattoiState['config']['debugLevel']>1): print("c0 Reset"+str(cattoiState['profile']['c0']), file=sys.stderr)   
      
   
   
def action_off(cattoiState):
   cattoiState['config']['LED0']=(128,0,0)
   cattoiState['profile']['period'] = 50
   cattoiState['profile']['c0']=0
   cattoiState['profile']['c0_max'] = 10
   cattoiState['profile']['name'] = "off"
   
def ARGB_off(cattoiState,pixels):
   cattoiState['config']['LED0']=(128,0,0)
   while(cattoiState['profile']['c0']>0):
      cattoiState['profile']['c0']=cattoiState['profile']['c0']-1
      pixels.fill((0, 0, 0))
      off_c0 = cattoiState['profile']['c0']/cattoiState['profile']['c0_max']
      cattoiState['config']['LED0']=(int(numpy.interp(off_c0,[0,.5,1],[16,64,16])),0,0)
      pixels[0]=cattoiState['config']['LED0']
      pixels.show()
      time.sleep(cattoiState['profile']['period']/1000)      
   if(cattoiState['config']['debugLevel']>1): print("c0 Reset", file=sys.stderr)
   cattoiState['profile']['c0']=cattoiState['profile']['c0_max']
   
      
def action_init(cattoiState):
   cattoiState['config']['LED0']=(128,128,128)
   cattoiState['profile']['period'] = 200
   cattoiState['profile']['c0']=0
   cattoiState['profile']['c0_max'] = 5
   cattoiState['profile']['name'] = "init"
   
def ARGB_init(cattoiState,pixels):
   cattoiState['config']['LED0']=(128,128,128)
   while(cattoiState['profile']['c0']>0):
      pixels.fill((0, 0, 0))
      cattoiState['profile']['c0']=cattoiState['profile']['c0']-1
      init_c0 = cattoiState['profile']['c0']/cattoiState['profile']['c0_max']
      #print("tryIP loop"+ tryIP, file=sys.stderr)
      if(cattoiState['config']['IP']=="127.0.0.1"): #not configured: red
         tryIP=(0,0,64) if (init_c0>.5) else (0,0,32)
      elif(cattoiState['config']['IP'] == '10.0.0.5'): #config IP: purple
         tryIP=(64,0,64) if (init_c0>.5) else (32,0,32)
      else:#good IP: green
         tryIP=(0,64,0) if (init_c0>.5) else (0,32,0)
      
      cattoiState['config']['LED0']=tryIP
      pixels[0]=cattoiState['config']['LED0']
      pixels.show()
      time.sleep(cattoiState['profile']['period']/1000)   
   cattoiState['profile']['c0']=cattoiState['profile']['c0_max']

