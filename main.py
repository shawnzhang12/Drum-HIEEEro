"""
drumClass.py: Contains a class that will detect a circular red object 
              and track if it enters certain areas of space marked by
              coloured boxes. Will print which drum is hit in 
              terminal.
"""

import numpy as np
import cv2
import time
import math
import pygame
import random
import time
import wave
import glob, os
from threading import Thread
from queue import Queue

pygame.mixer.pre_init(buffer=2048)
pygame.init()
pygame.font.init()

green = (50, 220, 50)
lgreen = (90, 255, 90)

blue = (50, 50, 220)
lblue = (90, 90, 255)

yellow = (220, 200, 10)
lyellow = (255, 240, 60)

red = (230, 20, 20)
lred = (255, 70, 70)

black = (0,0,0)
gray = (125, 125, 125)
white = (255, 255, 255)


width = 600
length = 600

window = pygame.display.set_mode([width, length])
myfont = pygame.font.SysFont('Comic Sans MS', 30)

global y
y = 0

difficulty = 2

held_green = False
held_blue = False
held_yellow = False
held_red = False
total = 0
strike = 0
checkStrike = True
curscore = 0

run = True
clock = pygame.time.Clock()
clock.tick(1)

total = 0

channel1 = pygame.mixer.Channel(0) 
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2) 
channel4 = pygame.mixer.Channel(3)
channel5 = pygame.mixer.Channel(4) 

class note:
    def __init__(self, location, rtu, bpm, resolution):
       self.location = location
       self.rtu = rtu
       self.bpm = bpm
       self.resolution = resolution
       self.position = 0
       self.time = 0
       self.converttime()

    def move(self):
       global total
       global held_green
       global held_red
       global held_blue
       global held_yellow
       global total
       global strike
       global checkStrike
       global curscore

       self.position = self.position + 5 
       if self.location == 'hat':
           gr_mpad = pygame.Rect(25, self.position, 100, 50)
           if held_green == True:
                if self.position > 450:
                    total += 10
           pygame.draw.ellipse(window, (green), gr_mpad)

       if self.location == 'snare':
           bl_mpad = pygame.Rect(175, self.position, 100, 50)
           if held_blue == True:
                if self.position > 450:
                    total += 10
           pygame.draw.ellipse(window, (blue), bl_mpad)

       if self.location == "tom":
           ye_mpad = pygame.Rect(325, self.position, 100, 50)
           if held_yellow == True:
                if self.position > 450:
                    total += 10
           pygame.draw.ellipse(window, (yellow), ye_mpad)
      
       if self.location == "crash":
           re_mpad = pygame.Rect(475, self.position, 100, 50)
           if held_red == True:
                if self.position > 450:
                    total += 10
           pygame.draw.ellipse(window, (red), re_mpad)

    def converttime(self):
        self.time = (self.rtu * 60000000.0) / (self.bpm * self.resolution)

    def getposition(self):
        return self.position

    def gettime(self):
        return self.time

    def __del__(self):
        pass

def Overlay():
        gr_pad = pygame.Rect(25, 450, 100, 50)
        bl_pad = pygame.Rect(175, 450, 100, 50)
        ye_pad = pygame.Rect(325, 450, 100, 50)
        re_pad = pygame.Rect(475, 450, 100, 50)
        
        window.fill(black)
        
        pygame.draw.line(window, (white), (25, 475), (25, 0), 1)
        pygame.draw.line(window, (gray), (75, 475), (75, 0), 1)
        pygame.draw.line(window, (white), (125, 475), (125, 0), 1)
        
        pygame.draw.line(window, (white), (175, 475), (175, 0), 1)
        pygame.draw.line(window, (gray), (225, 475), (225, 0), 1)
        pygame.draw.line(window, (white), (275, 475), (275, 0), 1)
        
        pygame.draw.line(window, (white), (325, 475), (325, 0), 1)
        pygame.draw.line(window, (gray), (375, 475), (375, 0), 1)
        pygame.draw.line(window, (white), (425, 475), (425, 0), 1)
        
        pygame.draw.line(window, (white), (475, 475), (475, 0), 1)
        pygame.draw.line(window, (gray), (525, 475), (525, 0), 1)
        pygame.draw.line(window, (white), (575, 475), (575, 0), 1)
        
        pygame.draw.ellipse(window, (green), gr_pad)
        pygame.draw.ellipse(window, (blue), bl_pad)
        pygame.draw.ellipse(window, (yellow), ye_pad)
        pygame.draw.ellipse(window, (red), re_pad)

current = time.time()
current2 = time.time()
notes = []
startcheck = False
resolution = 0
bpm = 0
cnotetime = 0
lnotetime = 0
startdelay = 0
drums = ["hat","snare","tom","crash"]
endcheck = False
channelplay = False

print("")
print("Here are the current songs we offer:")

############# Change to match your directory ######
###################################################
###################################################
###################################################
###################################################
os.chdir("/home/shawn/Desktop/DrumHIEEEro")
###################################################
###################################################
###################################################
###################################################
###################################################

for file in glob.glob("*.chart"):
    print(file.rstrip(".chart"))

print("")
song = input("Insert song: ")
chartfile = song + ".chart"
wavfile = song + ".wav"
f = open(chartfile)
g = open(chartfile)
music = pygame.mixer.Sound(wavfile)

notearray = []
bpmarray = []
realnotearray = []
notecounter = 0
bpmcounter = 0
endcheck = False
bpmtotal = 0

print("Different Tracks:")
while True:
   line = g.readline().strip()
   if line == "[ExpertSingle]" or line == "[EasySingle]" or line == "[EasyDoubleBass]" or line == "[EasyDrums]" or line == "[MediumSingle]" or line == "[MediumDoubleBass]" or line == "[MediumDrums]" or line == "[HardSingle]" or line == "[HardDoubleBass]" or line == "[HardDrums]" or line == "[ExpertDoubleBass]" or line == "[ExpertDrums]":

      print(line)
   if line == "":
      break
   
g.close()
print("")
track = input("Select a track to play from the list above: ")
trackwb = "[" + track + "]"
while True:
   line = f.readline().strip()
   if "Resolution" in line:
      string = line.split()
      resolution = float(string[2])
      break

while True:
   line = f.readline().strip()
   if line == "[SyncTrack]":
      line = f.readline().strip()
      while True:
         line = f.readline().strip()
         if line == "}":
            break
         string = line.split()
         if string[2] == "B":
            bpmarray += [[string[0],string[3]]]
            bpmtotal += int(string[3])
      if line == "}":
         break


while True:
   line = f.readline().strip()

   if line == trackwb:

      line = f.readline().strip()
      while True:
         line = f.readline().strip()
         if line == "}":
            break
         string = line.split()
         if string[2] == "N":
            if string[3] == "4":
               pass              
               #notearray += [[string[0],"2"]]
            else:
               notearray += [[string[0],string[3]]]
      if line == "}":
         break


for anotes in notearray:
   while True:
      if bpmcounter == len(bpmarray):
         bpmcounter = len(bpmarray) - 1
         endcheck = True

      currentbpmtime = int(bpmarray[bpmcounter][0])

      if int(anotes[0]) >= currentbpmtime and endcheck == False:
         bpmcounter += 1
      else:
         if endcheck == False:
            bpmcounter -= 1
         #anote = note(drums[int(anotes[1])],float(anotes[0]),float(bpmarray[bpmcounter][1]),float(resolution))
         anote = note(drums[int(anotes[1])],float(anotes[0]),bpmtotal/len(bpmarray),float(resolution))
         realnotearray += [anote]
         break

current = time.time()

cap_width = 640
cap_height = 360


class drum():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
        _, self.img = self.cap.read()
        self.im_orig = self.img.copy()
        self.lower_colour = np.array([50,0,0])
        self.upper_colour = np.array([70,255,255])
        self.mask1 = 0
        self.hsv = 0
        self.contours = 0
        self.contour_centre = [0,0,0,0]
        self.tom2Coords = (10, 220, 150, 280)
        self.tom1Coords = (170, 290, 310, 350)
        self.snareCoords = (330, 290, 470, 350)
        self.hihatCoords = (490, 220, 630, 280)
        self.wasInSnare = False
        self.wasInTom1 = False
        self.wasInTom2 = False
        self.wasInHihat = False

    # Gets a frame from VideoCapture
    def get_frame(self):
        _ , self.img = self.cap.read()  # ret = 1 if the video is captured; frame is the image
        self.img  = np.flip(self.img, axis=1)
        self.im_orig = self.img.copy() # Make a copy of original image
        self.hsv = cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV) 

    # Creates a mask of chosen colour
    def mask(self):
        self.mask1 = cv2.inRange(self.hsv, self.lower_colour, self.upper_colour)
        #mask2 = cv2.inRange(self.hsv,self.lower_red[1],self.upper_red[1])
        #self.mask1 = self.mask1+mask2
        self.mask1 = cv2.morphologyEx(self.mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        self.mask1 = cv2.morphologyEx(self.mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    # Finds and draws contours. Will only use circular ones
    def draw_contours(self):
        self.contours, _ = cv2.findContours(self.mask1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self.contour_centre = [0,0,0,0]
        i = 0
        for contour in self.contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    break
                circularity = 4*math.pi*(area/(perimeter*perimeter))
                #print circularity
                if 0.0 < circularity < 1.2:
                    cv2.drawContours(self.im_orig, contour, -1, (0,255,0), 3) #Adds circle contour
                    br = cv2.boundingRect(contour)
                    self.contour_centre[i] = br[0]+br[2]/2 
                    self.contour_centre[i+1] = br[1]+br[3]/2
                    cv2.rectangle(self.im_orig, (br[0], br[1]),
                        (br[0] + br[2], br[1] + br[3]), (255, 0, 0), 0) #Adds rectangular contour
                    i += 2
                    if i > 3:
                        break
    
    # Draws rectangles for drum space
    def draw_drum_rect(self):
        cv2.rectangle(self.im_orig, (self.tom1Coords[0], self.tom1Coords[1]),
                        (self.tom1Coords[2], self.tom1Coords[3]), (255, 0, 0), 0)

        cv2.rectangle(self.im_orig, (self.tom2Coords[0], self.tom2Coords[1]),
                        (self.tom2Coords[2], self.tom2Coords[3]), (0, 255, 0), 0)

        cv2.rectangle(self.im_orig, (self.snareCoords[0], self.snareCoords[1]),
                        (self.snareCoords[2], self.snareCoords[3]), (0, 255, 255), 0)

        cv2.rectangle(self.im_orig, (self.hihatCoords[0], self.hihatCoords[1]),
                        (self.hihatCoords[2], self.hihatCoords[3]), (0, 0, 255), 0)

    # Displays the resulting image
    def show_img(self):
        resized_image = cv2.resize(self.im_orig, (1280 , 720)) 
        cv2.imshow('Video Capture',resized_image)

    # Determines if snare hit
    def snareHit(self):
        if self.inDrumZone(self.contour_centre, "snare"):
            if self.wasInSnare == False:
                self.wasInSnare = True
                return True
            else:
                return False
        else:
            self.wasInSnare = False
            return False

    # Determines if first tom hit
    def tom1Hit(self):
        if self.inDrumZone(self.contour_centre, "tom1"):
            if self.wasInTom1 == False:
                self.wasInTom1 = True
                return True
            else:
                return False
        else:
            self.wasInTom1 = False
            return False

    # Determines if second tom hit
    def tom2Hit(self):
        if self.inDrumZone(self.contour_centre, "tom2"):
            if self.wasInTom2 == False:
                self.wasInTom2 = True
                return True
            else:
                return False
        else:
            self.wasInTom2 = False
            return False

    # Determines if hihat hit
    def hihatHit(self):
        if self.inDrumZone(self.contour_centre, "hihat"):
            if self.wasInHihat == False:
                self.wasInHihat = True
                return True
            else:
                return False
        else:
            self.wasInHihat = False
            return False


    # Checks if drumstick in drum space
    def inDrumZone(self, center, drum):
        if drum == "tom2":
            if ((center[0] > self.tom2Coords[0] and center[1] > self.tom2Coords[1] and
                center[0] < self.tom2Coords[2] and center[1] < self.tom2Coords[3]) or 
                (center[2] > self.tom2Coords[0] and center[3] > self.tom2Coords[1] and
                center[2] < self.tom2Coords[2] and center[3] < self.tom2Coords[3])
                ):
                return True
            else:
                return False
        elif drum == "tom1":
            if ((center[0] > self.tom1Coords[0] and center[1] > self.tom1Coords[1] and
                center[0] < self.tom1Coords[2] and center[1] < self.tom1Coords[3]) or 
                (center[2] > self.tom1Coords[0] and center[3] > self.tom1Coords[1] and
                center[2] < self.tom1Coords[2] and center[3] < self.tom1Coords[3])
                ):
                return True
            else:
                return False
        elif drum == "snare":
            if ((center[0] > self.snareCoords[0] and center[1] > self.snareCoords[1] and
                center[0] < self.snareCoords[2] and center[1] < self.snareCoords[3]) or
                (center[2] > self.snareCoords[0] and center[3] > self.snareCoords[1] and
                center[2] < self.snareCoords[2] and center[3] < self.snareCoords[3])
                ):
                return True
            else:
                return False
        elif drum == "hihat":
            if ((center[0] > self.hihatCoords[0] and center[1] > self.hihatCoords[1] and
                center [0] < self.hihatCoords[2] and center[1] < self.hihatCoords[3]) or
                (center[2] > self.hihatCoords[0] and center[3] > self.hihatCoords[1] and
                center [2] < self.hihatCoords[2] and center[3] < self.hihatCoords[3])
                ):
                return True
            else:
                return False

    # Plays drum sounds
    def playSounds(self):
        self.snareHit()   
        self.tom1Hit()
        self.tom2Hit()
        self.hihatHit()

    def get_next_frame(self):
        self.get_frame()
        self.mask()
        self.draw_contours()
        self.draw_drum_rect()
        self.show_img()
        self.playSounds()

    def get_drum_values(self):
        return [self.wasInTom2, self.wasInTom1, self.wasInSnare, self.wasInHihat]



def Lights():
        
        pA = pygame.mixer.Sound("hat.wav")
        pC = pygame.mixer.Sound("snare.wav")
        pD = pygame.mixer.Sound("tom.wav")
        pF = pygame.mixer.Sound("crash.wav")

        gr_pad = pygame.Rect(25, 450, 100, 50)
        bl_pad = pygame.Rect(175, 450, 100, 50)
        ye_pad = pygame.Rect(325, 450, 100, 50)
        re_pad = pygame.Rect(475, 450, 100, 50)

        drumhit = q.get()    

        #print(drumhit)
        if drumhit[0]:
           held_green = True
           channel1.play(pA)
        else:
           held_green = False

        if drumhit[1]:
           held_blue = True
           channel2.play(pC)
        else:
           held_blue = False

        if drumhit[2]:
           held_yellow = True
           channel3.play(pD)
        else:
           held_yellow = False

        if drumhit[3]:
           held_red = True
           channel4.play(pF)
        else:
           held_red = False
 
        if held_green == True:
            pygame.draw.ellipse(window, (lgreen), gr_pad)
        if held_blue == True:
            pygame.draw.ellipse(window, (lblue), bl_pad)
        if held_yellow == True:
            pygame.draw.ellipse(window, (lyellow), ye_pad)
        if held_red == True:
            pygame.draw.ellipse(window, (lred), re_pad)

q = Queue(maxsize=1000)

def main():
    samplerate = 5
    d = drum()
    count = 0
    start = time.time()
    stallq = []
    stallcheck = [False] * 4
    for i in range(0,samplerate,1):
       d.get_next_frame()
       out = d.get_drum_values()
       stallq += [out]
    #print(stallq)

    while (time.time()-start <= 100000000000000000000):
       trueoutput = [False] * 4
       stallcheck = [False] * 4
       d.get_next_frame()
       count += 1
       if not q.full():
          out=d.get_drum_values()
          #print("StallQ Packet")
          for i in range(0,samplerate,1):
             
             #print(stallq[i])
             for j in range (0,4,1):
                if stallq[i][j] == True:
                   stallcheck[j] = True

          for i in range(0,4,1):
             if not stallcheck[i] and out[i]:
                trueoutput[i] = True
             else:
                trueoutput[i] = False 

          q.put(trueoutput)
          stallq = stallq[1:]
          stallq += [out]
       if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
           break  

#Initializing threading for cv process
t = Thread(target=main, args=())
t.daemon=True
t.start()

while True:
    Overlay()
    Lights() 

    for n in notes:
        n.move()
        if n.getposition() > 500:
            notes.remove(n)

    #print(realnotearray[notecounter].gettime() / 1000.0)
    if time.time() - current > (realnotearray[notecounter].gettime() / 1000.0):
       notes += [realnotearray[notecounter]]
       notecounter += 1
       if notecounter == len(realnotearray):
          notecounter -= 1
    
    if channelplay == False:
       if time.time() - current > 2.8:
          channel5.play(music)
          channelplay = True

    textsurface = myfont.render("Score: %s" % total, 1, (100, 100, 100))
    window.blit(textsurface,(0, 0))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
f.close()
