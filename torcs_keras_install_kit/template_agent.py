import numpy as np
import matplotlib.pyplot as plt
import random

class Agent(object):
    def __init__(self, dim_action):
        self.dim_action = dim_action

    def act(self, ob, reward, done, vision_on):
        #print("ACT!")

        # Get an Observation from the environment.
        # Each observation vectors are numpy array.
        # focus, opponents, track sensors are scaled into [0, 1]. When the agent
        # is out of the road, sensor variables return -1/200.
        # rpm, wheelSpinVel are raw values and then needed to be preprocessed.
        # vision is given as a tensor with size of (64*64, 3) = (4096, 3) <-- rgb
        # and values are in [0, 255]
        obDict = ob
        focus = obDict["focus"]
        speedX = obDict["speedX"]
        speedY = obDict["speedY"]
        speedZ = obDict["speedZ"]
        opponents = obDict["opponents"]
        rpm = obDict["rpm"]
        track = obDict["track"]
        wheelSpinVel = obDict["wheelSpinVel"]
        if vision_on:
            vision = obDict["img"]
            #The code below is for checking the vision input. 
            #This is very heavy for real-time Control So you may need to remove.
            img = np.ndarray((64,64,3))
            plt.imshow(img, origin='lower')
            plt.draw()
            plt.pause(0.001)

        #################################################
        ###      START OF AGENT (modify this code)    ###
        #################################################
        steer = float(0)   #random.uniform(-1, 1)
        accel = random.uniform(0, 1)
        #most of the time don't break
        if not random.choice(range(10)):
             brk = random.uniform(0, 1)
        else:
             brk = float(0)
        #################################################
        ###      END OF AGENT (modify up to here)     ###
        #################################################

        return np.tanh([ steer, accel, brk] ) # random action
