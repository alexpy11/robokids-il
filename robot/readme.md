Shalom Mitz			5 Feb 2017

Note: The instructions below assume a Linux machine is used. Howere, all those steps can be done on Windows as well.
      If Windows are used, the main change is the name of the serial.
      

One time:
Steps 1 to 8 below need to be performed only once per NodeMCU
1) Connect the NodeMCU to a PC running Linux, using a normal 'Android' USB cable
2) ls /dev/ttyUSB? should show /dev/ttyUSB0
   If only /dev/ttyUSB2 exists, you should change 'burn' to reflect this
   If the 'ls' command above does not show anything, the NodeMCU was not recognized.
   This must be resolved before continuing.

OPTIONAL: you can bring the latest firmware build from
     http://micropython.org/download#esp8266
     If you bring such a file, you need to modify the 2nd line of 'burn'

3) Program the NodeMCU w/microPython: Simply run './burn'
   Note: 'burn' depends on the 'serial' Python module.

4) Sanity check: disconnect the NodeMCU from the USB and plug back.
   When you re-connect the NodeMCU, one of the LEDs should blink twice.
   If the LED does not blink, or blink all the time, try to run 'burn' again
   Note: Detailed instructions of programming the NodeMCU and troubleshooting can be found at:
   http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware


5) Connect to the NodeMCU: 
   The NodeMCU looks like serial port at /dev/ttyUSB0 (rarly: /dev/ttyUSB1)
   You can connect to it using: putty, minicom, screen, or any other 'terminal emulation' sofware

   Once you are connected, hit "Enter" few times, and you should get the ">>>" REPL prompt.
   If you do not get the prompt, try unplugin/pluging from USB. If this fails, try 'burn' again.
   There is no point to continue w/o the REPL prompt.

6) Enable WebREPL: WebREPL is a very useful ability to use REPL over WiFi.
   To enable it, copy/paste the following lines into the ">>>" REPL prompt:
f = open('boot.ini','w')
f.write('import gc, webrepl\nwebrepl.start()\ngc.collect()\n')
f.close()
   
6) Disable password when accessing the NodeMCU using WiFi:
   Copy/paste the following lines into the ">>>" REPL prompt:
import network
ap = network.WLAN(network.AP_IF)
ap.config(authmode=0)

7) Restart the NodeMCU, so the two previous steps will take affect.
   This is done by unpluging/repluging from USB, or by pressing the 'rst' botton.

8) Download the files needed for WebREPL to your disk:
   Download the needed files to your disk from:
   https://github.com/micropython/webrepl/archive/master.zip
   Extract the files from the zip into a directory.
 
Steps that are repeated each time the NodeMCU is used:
9) Connect to the PC/laptop to the WiFi access-point created by the NodeMCU:
   Look at the available WiFi networks for a network called "MicroPython-xxxxxx" (the 'xxxxxx' part is different for each NodeMCU)
   Connect to this network.
   Note: This will probably disconnect you from the Internet. 

9) Connect to the NodeMCU using WebREPL:
   Open the file "open webrepl.html in a browser. This file was saved to the hard-disk at step 8 above.
   You should get a prompt to choose password (first time) or login.
   After login, you should get the ">>>" prompt. You are also able to upload and download files.
   There are more details at: https://github.com/micropython/webrepl

10) Put the 'robot.py' module on the NodeMCU storage
    This is done using WebREPL.

11) Test the robot:
    Using WebREPL, import the 'robot' module. This will define 4 outputs:
    pwmRight, dirRight, pwmLeft, dirLeft
    Each of those can be set to high or low, for example:
    pwmRight.low() or pwmLeft.high() 
