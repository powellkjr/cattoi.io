

'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com

updated 2.31
'''

import RPi.GPIO as GPIO
from gpiozero import Pin
import board
import neopixel
import time
import sys
import getopt
import socket
import subprocess
import os
import importlib
import imp
import pprint
import numpy
from flask import Flask, render_template, request, jsonify
from multiprocessing import Process, Value, Manager
from random import randrange
#from config import *
from os.path import dirname, join, isdir, abspath, basename
from glob import glob
#import defaultValues
from profiles import *
import profiles
#working
lastTime=time.time_ns()
pwd = dirname(__file__)
sys.path.append(pwd+'/profiles')
from defaultValues import *
#from profiles.basic import *
#__import__('basic') #adds basic.action
def loadImports(path):
    files = os.listdir(pwd+"/"+path+"/")
    imps = []

    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
               name = name[0]
               imps.append(name)

    file = open(pwd+"/"+path+"/"+'__init__.py','w')

    toWrite = '__all__ = '+str(imps)

    file.write(toWrite)
    file.close()
loadImports('profiles')
from profiles import *

#basic=__import__('basic')
#__import__('profiles') #adds basic.action
#import profiles #adds basic.action
#from profiles import * #adds basic.action
#from profiles.basic import * #adds action_peek

#importlib.import_module('profiles.basic')
#profile_basic = importlib.import_module("profiles.basic",package=None)
#importlib.load_module(pwd+'/profiles/basic.py')
#imp.load_source('profile_basic',pwd+'/profiles/basic.py')









print("Path: " + str(sys.path),file=sys.stderr)

# for x in glob(join(pwd, '*.py')):
    # if('__' not in x):
        # print("Loading from x name:" + x,file=sys.stderr)
        # __import__(basename(x)[:-3], globals(), locals())
        # importlib.import_module(basename(x)[:-3])
        
# for x in glob(join(pwd+'/profiles/', '*.py')):
    # if not x.startswith('__'):
        # print("Loading from x name:" + x,file=sys.stderr)
        # __import__(basename(x)[:-3], globals(), locals())
        # importlib.import_module(basename(x)[:-3])




def get_ip():
  
   tryIP = subprocess.run([ "hostname", "-I"], capture_output=True, text=True).stdout
  
   if debugLevel >1: print("tryIPraw:" + str(tryIP), file=sys.stderr)
   try:
      IP = tryIP
   except Exception:
      IP = '127.0.0.1'   
   IP=IP.strip() 
   if debugLevel >0: print("IP:>" + IP + "<", file=sys.stderr)
   return IP


def get_SSID():
   SSID=subprocess.run([ "iwgetid", "-r"], capture_output=True, text=True).stdout
   if debugLevel >0: print("SSID: " + SSID,file=sys.stderr)
   return SSID
   
def get_ssidList():
   scanResults = subprocess.run([ "sudo","iw", "wlan0", "scan"], capture_output=True, text=True).stdout
   scanResults= scanResults.replace("\t","")
   scanList = scanResults.split("SSID:")
   ssidList = []
   for SSID in scanList:
      testID=SSID.split("\n")
      if("wlan0" not in testID[0] and len(testID[0])>1):
         ssidList.append(testID[0])
   if debugLevel >0: print(ssidList,file=sys.stderr)
   return ssidList


app = Flask(__name__)

GPIO.setmode(GPIO.BCM)


runProfile='preStart'

pixels = neopixel.NeoPixel(default_pixelPin, default_pixels, brightness=0.2, auto_write=False)
#pixels.begin()
pixels.fill((0, 0, 0))
pixels[0]=(128,0,0)
pixels.show()
myIP=get_ip()
mySSID=get_SSID()
myssidList=get_ssidList()
print("IP: " + myIP,file=sys.stderr)






 
@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   #for pin in pins:
   #   pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   #global templateData
   # templateData = {
      # 'cattoiState' : cattoiState,
      # 'pins' : pins
      # }
   # Pass the template data into the template main.html and return it to the user

   print("Main initializing"+templateData['cattoiState']['config']['SSID'], file=sys.stderr)
   runProfile='Main'   
   return render_template('main.html', **templateData)


   
@app.route("/configSSID" , methods=['GET', 'POST'])
def configSSID():
    newSSID = str(request.form.get('newSSID'))
    newPASS = str(request.form.get('newPASS'))
   
    print("Adding the SSID: " + newSSID + " with " + newPASS, file=sys.stderr)
    
    os.system('wpa_passphrase ' + newSSID + ' ' + newPASS + ' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf')
    os.system('sudo sed -i \'/#psk/d\' /etc/wpa_supplicant/wpa_supplicant.conf')
    print(os.system('sudo cat /etc/wpa_supplicant/wpa_supplicant.conf'), file=sys.stderr)
    time.sleep(1)
    os.system('sudo reboot')

    
    
    return render_template('main.html', **templateData)
    
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/config_peek", methods=['GET', 'POST'])
def config_peek():
   cattoiState['profile']['name'] = "hold"
   period=int(request.form['config_peek_period'])
   duty=int(request.form['config_peek_duty'])
   basic.action_peek(cattoiState,period,duty)
   return render_template('main.html', **templateData)
   
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/config_shift", methods=['GET', 'POST'])
def config_shift():
   cattoiState['profile']['name'] = "hold"
   period=int(request.form['config_shift_period'])
   wide=int(request.form['config_shift_wide'])
   step=int(request.form['config_shift_step'])
   basic.action_shift(cattoiState,period,wide,step)
   return render_template('main.html', **templateData)
   
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/config_off", methods=['GET', 'POST'])
def config_off():
   cattoiState['profile']['name'] = "hold"
   basic.action_off(cattoiState)
   return render_template('main.html', **templateData)
   
  
def ARGB_controller(inDict, inData):
   global i
   global lastTime
   #global cattoiState
   #global templateData
   #ARGB_controller loop
   while True:
      #with templateData.get_lock():
      testVal = inData['cattoiState']['config']['SSID']
      testDict = inDict['test']
      
      if cattoiState['profile']['name']=='init':   
         tryIP = str(get_ip())
         trySSID= str(get_SSID())
         cattoiState['config']['SSID']=trySSID
         cattoiState['config']['IP']=tryIP
         basic.ARGB_init(cattoiState,pixels)
      elif cattoiState['profile']['name']=='off':   
         basic.ARGB_off(cattoiState,pixels)
      elif cattoiState['profile']['name']=='peek':
         basic.ARGB_peek(cattoiState,pixels)
      elif cattoiState['profile']['name']=='shift':
         basic.ARGB_shift(cattoiState,pixels)
      if(debugLevel>1):print('dt: ' + str((time.time_ns()-lastTime) // 1_000_000) + ' vs ' + str(cattoiState['profile']['period']),file=sys.stderr)
      lastTime=time.time_ns()


      
def setLED0():
   pixels[0]=cattoiState['config']['LED0']
   pixels.show()
   
	   

if __name__ == "__main__":
   argv=sys.argv[1:]
   try:
      #opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
      opts, args = getopt.getopt(argv,"vv",["ifile=","ofile="])
   except getopt.GetoptError:
      print( '__app.py -v debug -vv moreDebug', file=sys.stderr)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( '__app.py -v debug -vv moreDebug', file=sys.stderr)
         sys.exit()
      elif opt in ("-vv"):
         debugLevel=2
      elif opt in ("-v",):
         debugLevel = 1
   print("debugLevel" +str(debugLevel), file=sys.stderr)
   with Manager() as manager:
      global templateData
      global d
      global cattoiState
      global config
      global profile
      # global lastTime
      # lastTime=time.time_ns()
      
      
      d= manager.dict()
      cattoiState= manager.dict()
      templateData = manager.dict()
      profile=manager.dict()
      config=manager.dict()
      
      #d={'test':'this Dict'}
      d['test']='this Dict'
      
      profile['name']='init'
      profile['period']=200
      profile['focus']=0
      profile['c0']=0
      profile['c0_max']=5
      profile['wide']=3
      profile['duty']=50
      
      config['IP'] = myIP
      config['SSID'] = mySSID
      config['ssidList'] = myssidList
      config['passwd'] = 'testPasswd'
      config['size'] = default_pixels
      config['LED0'] = (64,0,0)
      config['debugLevel']=debugLevel
      
      
      
      
      cattoiState['config']= config
      cattoiState['profile']= profile
      templateData['cattoiState']=cattoiState
      basic.action_init(cattoiState)
      
      for i in range(100,50,-5): 
         print("i=" + str(i) +"interp" + str(numpy.interp(i,[50,100],[32,64])), file=sys.stderr)
      #templateData = {
      #   'cattoiState' : cattoiState,
      #   'pins' : pins
      #   }
      
 
      
      print("post config: " +templateData['cattoiState']['config']['SSID']+": " +d['test'], file=sys.stderr)

      p = Process(target=ARGB_controller, args=(d,templateData,))
      p.start()
      app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
      p.join()