#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# For more details go to https://github.com/splitti/oled_phoniebox/

import signal
import sys
import atexit
sys.path.append("/home/pi/oled_phoniebox/scripts/")
from scripts.o4p_functions import Init,get_device,GetCurrContrast,SetCharacters,GetMPC,Getself.WifiConn,Getself.specialInfos, SetNewMode
from time import sleep
from datetime import datetime
import os
from luma.core.render import canvas
from PIL import ImageFont, Image
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'Bitstream Vera Sans Mono Roman.ttf'))
font = ImageFont.truetype(font_path, 12)
font_small = ImageFont.truetype(font_path, 10)
font_midtower = ImageFont.truetype(font_path, 42)
font_hightower = ImageFont.truetype(font_path, 54)
font_path_wifi = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'WIFI.ttf'))
font_wifi = ImageFont.truetype(font_path_wifi, 64)
font_wifi_mix = ImageFont.truetype(font_path_wifi, 48)

confFile = "/home/pi/oled_phoniebox/oled_phoniebox.conf"
tempFile = "/tmp/o4p_overview.temp"
version = "1.8.3 - 20190626"




class PhonieBoxOledDisplay():
    def __init__(self, device):
        self.device = device
        self.tmpcard = 3
        self.linePos = 1
        self.subLine1 = 0
        self.subLine2 = 0
        self.subLine3 = 0
        self.widthLetter = 7
        self.spaceJump = 7
        self.oldMPC = ""
        self.oldPlaying = "-"
        self.displayTime = 0.5
        self.oldVol = "FirstStart"
        self.WifiConn = Getself.WifiConn()
        self.special = 0
        self.lenLine1 = -1
        self.lenLine2 = -1
        self.lenLine3 = -1
        self.line1 = 4
        self.line2 = 19
        self.line3 = 34
        self.line4org = 49
        self.line4 = self.device.height-1-10
        self.timetoshow = 1
        atexit.register(self.cleanup)

    def cleanup(self):
        self.ShowImage("poweroff")
        sleep(1)

    def ShowImage(self, imgname):
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', imgname + '.png'))
        logo = Image.open(img_path).convert("RGBA")
        fff = Image.new(logo.mode, logo.size, (255,) * 4)
        background = Image.new("RGBA", self.device.size, "black")
        posn = ((self.device.width - logo.width) // 2, 0)
        img = Image.composite(logo, fff, logo)
        background.paste(img, posn)
        self.device.display(background.convert(device.mode))

    def main(self, num_iterations=sys.maxsize):
        oldContrast = GetCurrContrast(confFile)
        self.device.contrast(oldContrast)
        self.ShowImage("music")

        while num_iterations > 0:
            num_iterations = 1
            curr_time = datetime.now()
            seconds = curr_time.strftime('%S')
            sleep(0.8)
            seconds = int(seconds)%5
            if seconds == 0:
                self.WifiConn = Getself.WifiConn()
            try:
            #if self.WifiConn != "BUGFIXING_LINE":
                if (os.path.exists(tempFile)) or (self.special == 1):
                    self.specialInfos = Getself.specialInfos()
                    if self.special == 0:
                        self.special = 1
                        self.timetoshow = 10
                        os.remove(tempFile)
                    with canvas(self.device) as draw:
                        draw.text((0, self.line1),  "WLAN: "+self.specialInfos[0],font=font_small, fill="white")
                        draw.text((0, self.line2),  "IP:   "+self.specialInfos[1],font=font_small, fill="white")
                        draw.text((0, self.line3),  "Version:",font=font_small, fill="white")
                        draw.text((0, self.line4org),version,font=font_small, fill="white")
                        draw.rectangle((self.device.width-4,0,self.device.width,self.device.height/10*self.timetoshow), outline="white", fill="white")

                        #draw.line((self.device.width, , self.device.width, self.device.height), fill="white")
                        #draw.text((110, line4org),self.timetoshow,font=font_small, fill="white")
                    sleep(1)
                    self.timetoshow = self.timetoshow - 1
                    if self.timetoshow == 0:
                        self.special = 0
                    if os.path.exists(tempFile):
                        self.timetoshow = 10
                        os.remove(tempFile)
                        newMode = SetNewMode(confFile)
                        initVars.set('GENERAL', 'mode', newMode)
                        with canvas(self.device) as draw:
                            draw.text((0, self.line1),initVars['GENERAL']['mode'],font=font_hightower, fill="white")
                        sleep(self.displayTime)
                else:
                    currContrast = GetCurrContrast(confFile)
                    if currContrast != oldContrast:
                        self.device.contrast(currContrast)
                        oldContrast = currContrast
                    mpcstatus = SetCharacters(GetMPC("mpc status"))
                    playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
                    currMPC = mpcstatus.split("\n")[0]
                    if (playing == "[playing]") or (playing == "[paused]"):
                        volume = mpcstatus.split("\n")[2].split("   ")[0].split(":")[1]
                    else:
                        volume = mpcstatus.split("   ")[0].split(":")[1]
                    vol = "V"+str(volume.replace("%",""))
                    if self.oldPlaying != playing:
                        if playing == "[playing]":
                            with canvas(self.device) as draw:
                                draw.polygon([(49, 10), (79, 32), (49, 54)], outline="white", fill="white")
                            sleep(self.displayTime)
                        if playing == "[paused]":
                            with canvas(self.device) as draw:
                                draw.rectangle((51,10,59,54), outline="white", fill="white")
                                draw.rectangle((69,10,77,54), outline="white", fill="white")
                            sleep(self.displayTime)
                        self.oldPlaying = playing
                    volume = int(volume.replace(" ","").replace("%",""))
                    if (self.oldVol != volume) and (self.oldVol != "FirstStart"):
                        with canvas(self.device) as draw:
                            draw.rectangle((30,22,45,42), outline="white", fill="white")
                            draw.polygon([(45, 22),(60, 10), (60,54), (45, 42)], outline="white", fill="white")
                            if volume != 0:
                                draw.rectangle((75,28,105,36), outline="white", fill="white")
                                if self.oldVol < volume:
                                    draw.rectangle((86,17,94,47), outline="white", fill="white")
                            else:
                                draw.text((75, 2),"X",font=font_hightower, fill="white")
                        sleep(self.displayTime)
                    self.oldVol = volume
                    if (playing == "[playing]") or (playing == "[paused]"):
                        if playing == "[playing]":
                            #timer = SetCharacters(GetMPC("mpc -f %time% current"))
                            elapsed = mpcstatus.split("\n")[1].replace("  "," ").split(" ")[3]
                        if currMPC != self.oldMPC:
                            track =   mpcstatus.split("\n")[1].replace("  "," ").split(" ")[1].replace("#","") #SetCharacters(GetMPC("mpc -f %track% current"))
                            if len(track.split("/")[1]) > 2:
                                track = track.split("/")[0]
                            if track == "\n":
                                track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","") #.split("/")[0]
                            file = SetCharacters(GetMPC("mpc -f %file% current")) # Get the current title
                            if initVars['GENERAL']['mode'] == "full" :
                                if file.startswith("http"): # if it is a http stream!
                                    txtLine1 = SetCharacters(GetMPC("mpc -f %name% current"))
                                    txtLine2 = SetCharacters(GetMPC("mpc -f %title% current"))
                                    txtLine3 = ""
                                    track = "--/--"
                                else: # if it is not a stream
                                    self.lenLine1 = -1
                                    self.lenLine2 = -1
                                    self.lenLine3 = -1
                                    self.subLine1 = 0
                                    self.subLine2 = 0
                                    self.subLine3 = 0
                                    self.linePos = 1
                                    txtLine1 = SetCharacters(GetMPC("mpc -f %album% current"))
                                    txtLine3 = SetCharacters(GetMPC("mpc -f %title% current"))
                                    txtLine2 = SetCharacters(GetMPC("mpc -f %artist% current"))
                                if txtLine2 == "\n":
                                    filename = SetCharacters(GetMPC("mpc -f %file% current"))
                                    filename = filename.split(":")[2]
                                    filename = SetCharacters(filename)
                                    localfile = filename.split("/")
                                    txtLine1 = localfile[1]
                                    txtLine2 = localfile[0]
                        if initVars['GENERAL']['mode'] == "lite" :
                            if playing != "[paused]":
                                TimeLine = elapsed.split("/")
                                if not file.startswith("http"):
                                    if TimeLine[1] != "0:00":
                                        elapsed = TimeLine[1]
                            if not file.startswith("http"):
                                TimeLineP = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
                                TimeLineP = self.device.width * TimeLineP / 100
                            else:
                                TimeLineP = self.device.width
                                track = "X"
                                xpos_w = self.device.width/2-38
                            track = track.split("/")[0]
                            if len(track) == 1:
                                xpos = self.device.width/2-15
                            if len(track) == 2:
                                xpos = self.device.width/2-30
                            if len(track) == 3:
                                xpos = self.device.width/2-45
                            if len(track) == 4:
                                xpos = self.device.width/2-60
                            with canvas(self.device) as draw:
                                if not file.startswith("http"):
                                    draw.text((xpos, 4),track,font=font_hightower, fill="white")
                                else:
                                    draw.text((xpos_w, 4),track,font=font_wifi, fill="white")
                                draw.rectangle((0,0,TimeLineP,1), outline="white", fill="white")
                                draw.rectangle((109, self.line4+8,111,self.line4+10), outline=self.WifiConn[0], fill=self.WifiConn[0])
                                draw.rectangle((114, self.line4+6,116,self.line4+10), outline=self.WifiConn[1], fill=self.WifiConn[1])
                                draw.rectangle((119, self.line4+4,121,self.line4+10), outline=self.WifiConn[2], fill=self.WifiConn[2])
                                draw.rectangle((124, self.line4+2,126,self.line4+10), outline=self.WifiConn[3], fill=self.WifiConn[3])
                        if initVars['GENERAL']['mode'] == "mix" :
                            if playing != "[paused]":
                                TimeLine = elapsed.split("/")
                                if TimeLine[0] == "(0%)":
                                    elapsed = "-:--"
                                elif TimeLine[1] != "0:00":
                                    elapsed = TimeLine[1]
                                else:
                                    elapsed = "-:--"
                                if len(elapsed) == 4:
                                    elapsed = "L "+elapsed
                                if len(elapsed) == 5:
                                    elapsed = "L"+elapsed
                            else:
                                elapsed = "PAUSE"
                            if not file.startswith("http"):
                                TimeLineP = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
                                TimeLineP = self.device.width * TimeLineP / 100
                            else:
                                TimeLineP = self.device.width
                                xpos_w = self.device.width/2-28
                                track = "X"
                            tracki = track.replace("\n","")
                            if len(tracki) == 1:
                                tracki = "    "+tracki
                            if len(tracki) == 2:
                                tracki = "   "+tracki
                            if len(tracki) == 3:
                                tracki = "  "+tracki
                            if len(tracki) == 4:
                                tracki = " "+tracki
                            if len(tracki) == 5:
                                tracki = tracki
                            track = track.split("/")[0]
                            if len(track) == 1:
                                xpos = self.device.width/2-13
                            if len(track) == 2:
                                xpos = self.device.width/2-26
                            if len(track) == 3:
                                xpos = self.device.width/2-39
                            if len(track) == 4:
                                xpos = self.device.width/2-52
                            with canvas(self.device) as draw:
                                if not file.startswith("http"):
                                    draw.line((39, self.line4-2, 39, self.device.height), fill="white")
                                    draw.text((0, self.line4),elapsed,font=font_small, fill="white")
                                    draw.text((42, self.line4),tracki,font=font_small, fill="white")
                                    draw.line((0, self.line4-2, self.device.width, self.line4-2), fill="white")
                                    draw.text((xpos, 4),track,font=font_midtower, fill="white")
                                else:
                                    draw.line((75, self.line4-2, self.device.width, self.line4-2), fill="white")
                                    draw.text((xpos_w, 4),track,font=font_wifi_mix, fill="white")
                                draw.rectangle((0,0,TimeLineP,1), outline="white", fill="white")
                                draw.rectangle((109, self.line4+8,111,self.line4+10), outline=self.WifiConn[0], fill=self.WifiConn[0])
                                draw.rectangle((114, self.line4+6,116,self.line4+10), outline=self.WifiConn[1], fill=self.WifiConn[1])
                                draw.rectangle((119, self.line4+4,121,self.line4+10), outline=self.WifiConn[2], fill=self.WifiConn[2])
                                draw.rectangle((124, self.line4+2,126,self.line4+10), outline=self.WifiConn[3], fill=self.WifiConn[3])
                                draw.line((75, self.line4-2, 75, self.device.height), fill="white")
                                draw.line((105, self.line4-2, 105, self.device.height), fill="white")
                                draw.text((78, self.line4),vol,font=font_small, fill="white")
                                draw.text((108, self.line4),"---",font=font_small, fill=self.WifiConn[4])
                                #draw.line((self.device.width/2, 0, self.device.width/2, self.device.height), fill="white")
                        if initVars['GENERAL']['mode'] == "full" :
                            if self.lenLine1 == -1:
                                self.lenLine1 = (len(txtLine1)*self.widthLetter)-self.device.width
                                if self.lenLine1 > 0 and self.lenLine1 < self.spaceJump:
                                    self.lenLine1 = self.spaceJump
                                if self.lenLine1 < 1:
                                    self.lenLine1 = 0
                                self.lenLine2 = (len(txtLine2)*self.widthLetter)-self.device.width
                                if self.lenLine2 > 0 and self.lenLine2 < self.spaceJump:
                                    self.lenLine2 = self.spaceJump
                                if self.lenLine2 < 1:
                                    self.lenLine2 = 0
                                self.lenLine3 = (len(txtLine3)*self.widthLetter)-self.device.width
                                if self.lenLine3 > 0 and self.lenLine3 < self.spaceJump:
                                    self.lenLine3 = self.spaceJump
                                if self.lenLine3 < 1:
                                    self.lenLine3 = 0
                                cnt = 0
                            if self.linePos == 1:
                                if (cnt <= self.lenLine1+self.spaceJump*3) and (self.lenLine1 != 0):
                                    self.subLine1 = cnt
                                    self.subLine2 = 0
                                    self.subLine3 = 0
                                else:
                                    self.linePos = 2
                                    cnt = 0-self.spaceJump
                            elif self.linePos == 2:
                                if (cnt <= self.lenLine2+self.spaceJump*3) and (self.lenLine2 != 0):
                                    self.subLine1 = 0
                                    self.subLine2 = cnt
                                    self.subLine3 = 0
                                else:
                                    self.linePos = 3
                                    cnt = 0-self.spaceJump
                            elif  self.linePos == 3:
                                if (cnt <= self.lenLine3+self.spaceJump*3) and (self.lenLine3 != 0):
                                    self.subLine1 = 0
                                    self.subLine2 = 0
                                    self.subLine3 = cnt
                                else:
                                    self.linePos = 1
                                    cnt = 0-self.spaceJump
                        if initVars['GENERAL']['mode'] == "full" :
                            if playing != "[paused]":
                                TimeLine = elapsed.split("/")
                                if TimeLine[0] == "(0%)":
                                    elapsed = "-:--"
                                elif TimeLine[1] != "0:00":
                                    elapsed = TimeLine[1]
                                else:
                                    elapsed = "-:--"
                                if len(elapsed) == 4:
                                    elapsed = "L "+elapsed
                                if len(elapsed) == 5:
                                    elapsed = "L"+elapsed
                            else:
                                elapsed = "PAUSE"
                            if not file.startswith("http"):
                                TimeLineP = int(mpcstatus.split("\n")[1].replace("   "," ").replace("  "," ").split(" ")[3].replace("(","").replace("%)",""))
                                TimeLineP = self.device.width * TimeLineP / 100
                            else:
                                TimeLineP = self.device.width
                            track = track.replace("\n","")
                            if len(track) == 1:
                                track = "    "+track
                            if len(track) == 2:
                                track = "   "+track
                            if len(track) == 3:
                                track = "  "+track
                            if len(track) == 4:
                                track = " "+track
                            if len(track) == 5:
                                track = track
                            with canvas(self.device) as draw:
                                if not file.startswith("http"):
                                    draw.line((39, self.line4-2, 39, self.device.height), fill="white")
                                    draw.text((0, self.line4),elapsed,font=font_small, fill="white")
                                    draw.text((42, self.line4),track,font=font_small, fill="white")
                                    draw.line((0, self.line4-2, self.device.width, self.line4-2), fill="white")
                                else:
                                    draw.line((75, self.line4-2, self.device.width, self.line4-2), fill="white")
                                draw.rectangle((0,0,TimeLineP,1), outline="white", fill="white")
                                draw.rectangle((109, self.line4+8,111,self.line4+10), outline=self.WifiConn[0], fill=self.WifiConn[0])
                                draw.rectangle((114, self.line4+6,116,self.line4+10), outline=self.WifiConn[1], fill=self.WifiConn[1])
                                draw.rectangle((119, self.line4+4,121,self.line4+10), outline=self.WifiConn[2], fill=self.WifiConn[2])
                                draw.rectangle((124, self.line4+2,126,self.line4+10), outline=self.WifiConn[3], fill=self.WifiConn[3])
                                draw.line((75, self.line4-2, 75, self.device.height), fill="white")
                                draw.line((105, self.line4-2, 105, self.device.height), fill="white")
                                draw.text((0-self.subLine1, self.line1),txtLine1,font=font, fill="white")
                                draw.text((0-self.subLine2, self.line2),txtLine2,font=font, fill="white")
                                draw.text((0-self.subLine3, self.line3),txtLine3,font=font, fill="white")
                                draw.text((78, self.line4),vol,font=font_small, fill="white")
                                draw.text((108, self.line4),"---",font=font_small, fill=self.WifiConn[4])
                                self.oldMPC = currMPC
                            cnt = cnt + self.spaceJump
                    else:
                        self.oldMPC = currMPC
                        if self.tmpcard < 3:
                            sleep(0.5)
                            self.tmpcard += 1
                        else:
                            self.ShowImage("cardhand")
                            self.tmpcard = 0
            except:
                sleep(0.5)
                self.ShowImage("music")

#if __name__ == "__main__":
initVars = Init(confFile)

try:
    device = get_device(initVars['GENERAL']['controller'])
    display = PhonieBoxOledDisplay(device=device)

    def sigterm_handler(signal, frame):
        # save the state here or do whatever you want
        device.cleanup()
        os._exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    display.main()
except KeyboardInterrupt:
    pass


