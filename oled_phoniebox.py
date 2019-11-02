#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# For more details go to https://github.com/splitti/oled_phoniebox/

import logging
import signal
import sys

from scripts import draw_functions
from scripts.mpc_status_reader import MPCStatusReader

sys.path.append("/home/pi/oled_phoniebox/scripts/")
from scripts.o4p_functions import Init, get_device, GetCurrContrast, SetCharacters, GetWifiConn, \
    GetSpecialInfos, SetNewMode
from time import sleep
import datetime
import os
from luma.core.render import canvas
from PIL import ImageFont

font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'fonts', 'Bitstream Vera Sans Mono Roman.ttf'))
font = ImageFont.truetype(font_path, 12)
font_small = ImageFont.truetype(font_path, 10)
font_midtower = ImageFont.truetype(font_path, 42)
font_hightower = ImageFont.truetype(font_path, 54)
font_path_wifi = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              'fonts', 'WIFI.ttf'))
image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images'))
font_wifi = ImageFont.truetype(font_path_wifi, 64)
font_wifi_mix = ImageFont.truetype(font_path_wifi, 48)

confFile = "/home/pi/oled_phoniebox/oled_phoniebox.conf"
tempFile = "/tmp/o4p_overview.temp"
version = "1.8.3 - 20190626"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)


def get_duration(duration_in_seconds):
        minutes = int(duration_in_seconds) // 60
        seconds = int(duration_in_seconds % 60)
        return minutes, seconds


class PhonieBoxOledDisplay:
    def __init__(self, device):
        self.device = device
        self.mpc_client = MPCStatusReader()
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
        self.WifiConn = GetWifiConn()
        self.special = 0
        self.cnt=0
        self.lenLine1 = -1
        self.lenLine2 = -1
        self.lenLine3 = -1
        self.line1 = 4
        self.line2 = 19
        self.line3 = 34
        self.line4org = 49
        self.line4 = self.device.height - 1 - 10
        self.timetoshow = 1
        self.confFile = Init(os.path.join(os.path.dirname(__file__), 'oled_phoniebox.conf'))
        self.update_time = 0.8

    def __del__(self):
        logger.info('delete')
        # os._exit(0)
        # self.cleanup()

    def cleanup(self):
        self.ShowImage("poweroff")
        sleep(1)
        logger.info('cleanup done')

    def ShowImage(self, imgname):
        logger.debug(f'ShowImage {imgname}')
        if imgname.startswith('cover'):
            img_path = os.path.abspath(os.path.join(image_dir, imgname + '.jpg'))
            draw_functions.drawCover(self.device, img_path)
        else:
            img_path = os.path.abspath(os.path.join(image_dir, imgname + '.png'))
            draw_functions.drawImage(self.device, img_path)

    def check_wifi_connection(self):
        logger.debug(f'Check WifiConnection')
        curr_time = datetime.datetime.now()
        seconds = curr_time.strftime('%S')
        seconds = int(seconds) % 5
        if seconds == 0:
            self.WifiConn = GetWifiConn()

    def show_change_display(self, mpd_info):
        logger.debug(f'ShowChangeDisplay')
        file = mpd_info['file']
        track = f'{mpd_info.get("playlisttrack"):>5}'
        if file.startswith("http"):  # if it is a http stream!
            txtLine1 = mpd_info['name']
            txtLine2 = mpd_info['title']
            txtLine3 = ""
            track = "--/--"
        else:  # if it is not a stream
            self.lenLine1 = -1
            self.lenLine2 = -1
            self.lenLine3 = -1
            self.subLine1 = 0
            self.subLine2 = 0
            self.subLine3 = 0
            self.linePos = 1
            txtLine1 = mpd_info['album']
            txtLine3 = mpd_info['title']
            txtLine2 = mpd_info['artist']
        if txtLine2 == "\n":
            filename = mpd_info['file']
            filename = filename.split(":")[2]
            filename = SetCharacters(filename)
            localfile = filename.split("/")
            txtLine1 = localfile[1]
            txtLine2 = localfile[0]
        return track, txtLine1, txtLine2, txtLine3

    def display_full_mode(self, txtLine1, txtLine2, txtLine3, vol, mpd_info):
        logger.debug(f'Display Full Mode')
        if self.lenLine1 == -1:
            self.lenLine1 = (len(txtLine1) * self.widthLetter) - self.device.width
            if self.lenLine1 > 0 and self.lenLine1 < self.spaceJump:
                self.lenLine1 = self.spaceJump
            if self.lenLine1 < 1:
                self.lenLine1 = 0
            self.lenLine2 = (len(txtLine2) * self.widthLetter) - self.device.width
            if self.lenLine2 > 0 and self.lenLine2 < self.spaceJump:
                self.lenLine2 = self.spaceJump
            if self.lenLine2 < 1:
                self.lenLine2 = 0
            self.lenLine3 = (len(txtLine3) * self.widthLetter) - self.device.width
            if self.lenLine3 > 0 and self.lenLine3 < self.spaceJump:
                self.lenLine3 = self.spaceJump
            if self.lenLine3 < 1:
                self.lenLine3 = 0
            self.cnt = 0
        if self.linePos == 1:
            if (self.cnt <= self.lenLine1 + self.spaceJump * 3) and (self.lenLine1 != 0):
                self.subLine1 = self.cnt
                self.subLine2 = 0
                self.subLine3 = 0
            else:
                self.linePos = 2
                self.cnt = 0 - self.spaceJump
        elif self.linePos == 2:

            if (self.cnt <= self.lenLine2 + self.spaceJump * 3) and (self.lenLine2 != 0):
                self.subLine1 = 0
                self.subLine2 = self.cnt
                self.subLine3 = 0
            else:
                self.linePos = 3
                self.cnt = 0 - self.spaceJump
        elif self.linePos == 3:
            if (self.cnt <= self.lenLine3 + self.spaceJump * 3) and (self.lenLine3 != 0):
                self.subLine1 = 0
                self.subLine2 = 0
                self.subLine3 = self.cnt
            else:
                self.linePos = 1
                self.cnt = 0 - self.spaceJump
        mpc_state = mpd_info['state']
        if mpc_state != "pause":
            elapsed = f'L{mpd_info["elapsed_as_time"]:>5}'
        else:
            elapsed = "PAUSE"
        file = mpd_info['file']
        TimeLineP = mpd_info['rel_elapsed_time'] * self.device.width
        track = f'{mpd_info.get("playlisttrack"):>5}'
        with canvas(self.device) as draw:
            if not file.startswith("http"):
                draw.line((39, self.line4 - 2, 39, self.device.height), fill="white")
                draw.text((0, self.line4), elapsed, font=font_small, fill="white")
                draw.text((42, self.line4), track, font=font_small, fill="white")
                draw.line((0, self.line4 - 2, self.device.width, self.line4 - 2), fill="white")
            else:
                draw.line((75, self.line4 - 2, self.device.width, self.line4 - 2), fill="white")
            draw.rectangle((0, 0, TimeLineP, 1), outline="white", fill="white")
            self.show_wifi_connection(draw)
            draw.line((75, self.line4 - 2, 75, self.device.height), fill="white")
            draw.line((105, self.line4 - 2, 105, self.device.height), fill="white")
            draw.text((0 - self.subLine1, self.line1), txtLine1, font=font, fill="white")
            draw.text((0 - self.subLine2, self.line2), txtLine2, font=font, fill="white")
            draw.text((0 - self.subLine3, self.line3), txtLine3, font=font, fill="white")
            draw.text((78, self.line4), vol, font=font_small, fill="white")
            draw.text((108, self.line4), "---", font=font_small, fill=self.WifiConn[4])
            self.oldMPC = mpd_info['song_description']
        self.cnt += self.spaceJump
        return track

    def get_relative_ellapsed_time(self, file, mpcstatus):
        if not file.startswith("http"):
            TimeLineP = int(
                mpcstatus.split("\n")[1].replace("   ", " ").replace("  ", " ").split(" ")[3].replace("(", "").replace(
                    "%)", ""))
            TimeLineP = TimeLineP / 100.
        else:
            TimeLineP = 1.
        return TimeLineP

    def display_mixed_mode(self, elapsed, file, mpc_state, mpcstatus, track, vol, xpos, xpos_w):
        logger.debug(f'Display Mixed Mode')
        if mpc_state != "pause":
            TimeLine = elapsed.split("/")
            if TimeLine[0] == "(0%)":
                elapsed = "-:--"
            elif TimeLine[1] != "0:00":
                elapsed = TimeLine[1]
            else:
                elapsed = "-:--"
            if len(elapsed) == 4:
                elapsed = "L " + elapsed
            if len(elapsed) == 5:
                elapsed = "L" + elapsed
        else:
            elapsed = "PAUSE"
        if not file.startswith("http"):
            TimeLineP = int(
                mpcstatus.split("\n")[1].replace("   ", " ").replace("  ", " ").split(" ")[3].replace("(", "").replace(
                    "%)", ""))
            TimeLineP = self.device.width * TimeLineP / 100
        else:
            TimeLineP = self.device.width
            xpos_w = self.device.width / 2 - 28
            track = "X"
        tracki = track.replace("\n", "")
        if len(tracki) == 1:
            tracki = "    " + tracki
        if len(tracki) == 2:
            tracki = "   " + tracki
        if len(tracki) == 3:
            tracki = "  " + tracki
        if len(tracki) == 4:
            tracki = " " + tracki
        if len(tracki) == 5:
            tracki = tracki
        track = track.split("/")[0]
        if len(track) == 1:
            xpos = self.device.width / 2 - 13
        if len(track) == 2:
            xpos = self.device.width / 2 - 26
        if len(track) == 3:
            xpos = self.device.width / 2 - 39
        if len(track) == 4:
            xpos = self.device.width / 2 - 52
        with canvas(self.device) as draw:
            if not file.startswith("http"):
                draw.line((39, self.line4 - 2, 39, self.device.height), fill="white")
                draw.text((0, self.line4), elapsed, font=font_small, fill="white")
                draw.text((42, self.line4), tracki, font=font_small, fill="white")
                draw.line((0, self.line4 - 2, self.device.width, self.line4 - 2), fill="white")
                draw.text((xpos, 4), track, font=font_midtower, fill="white")
            else:
                draw.line((75, self.line4 - 2, self.device.width, self.line4 - 2), fill="white")
                draw.text((xpos_w, 4), track, font=font_wifi_mix, fill="white")
            draw.rectangle((0, 0, TimeLineP, 1), outline="white", fill="white")
            self.show_wifi_connection(draw)
            draw.line((75, self.line4 - 2, 75, self.device.height), fill="white")
            draw.line((105, self.line4 - 2, 105, self.device.height), fill="white")
            draw.text((78, self.line4), vol, font=font_small, fill="white")
            # draw.line((self.device.width/2, 0, self.device.width/2, self.device.height), fill="white")
        return elapsed, track, xpos, xpos_w

    def display_lite_mode(self, elapsed, file, mpc_state, mpcstatus, track, xpos_w):
        logger.debug(f'Display Lite Mode')
        if mpc_state != "pause":
            TimeLine = elapsed.split("/")
            if not file.startswith("http"):
                if TimeLine[1] != "0:00":
                    elapsed = TimeLine[1]
        if not file.startswith("http"):
            TimeLineP = int(
                mpcstatus.split("\n")[1].replace("   ", " ").replace("  ", " ").split(" ")[3].replace("(", "").replace(
                    "%)", ""))
            TimeLineP = self.device.width * TimeLineP / 100
        else:
            TimeLineP = self.device.width
            track = "X"
            xpos_w = self.device.width / 2 - 38
        track = track.split("/")[0]
        xpos = self.get_xpos(track)
        with canvas(self.device) as draw:
            if not file.startswith("http"):
                draw.text((xpos, 4), track, font=font_hightower, fill="white")
            else:
                draw.text((xpos_w, 4), track, font=font_wifi, fill="white")
            draw.rectangle((0, 0, TimeLineP, 1), outline="white", fill="white")
            self.show_wifi_connection(draw)
        return elapsed, track, xpos, xpos_w

    def get_xpos(self, track):
        if len(track) == 1:
            xpos = self.device.width / 2 - 15
        if len(track) == 2:
            xpos = self.device.width / 2 - 30
        if len(track) == 3:
            xpos = self.device.width / 2 - 45
        if len(track) == 4:
            xpos = self.device.width / 2 - 60
        return xpos

    def show_wifi_connection(self, draw):
        if self.WifiConn[4] == 'white':
            draw.text((108, self.line4), "---", font=font_small, fill=self.WifiConn[4])
            return
        draw.rectangle((109, self.line4 + 8, 111, self.line4 + 10), outline='white', fill=self.WifiConn[0])
        draw.rectangle((114, self.line4 + 6, 116, self.line4 + 10), outline='white', fill=self.WifiConn[1])
        draw.rectangle((119, self.line4 + 4, 121, self.line4 + 10), outline='white', fill=self.WifiConn[2])
        draw.rectangle((124, self.line4 + 2, 126, self.line4 + 10), outline='white', fill=self.WifiConn[3])

    def check_and_display_volume(self, volume):
        logger.debug(f'Check Display Volume')
        if (self.oldVol != volume) and (self.oldVol != "FirstStart"):
            with canvas(self.device) as draw:
                self.draw_loudspeaker(draw)
                if volume != 0:
                    rectangle = (11 + self.device.width // 2,
                                  -4 + self.device.height // 2,
                                  41 + self.device.width // 2,
                                   4 + self.device.height // 2)
                    draw.rectangle(rectangle, outline="white", fill="white")
                    if self.oldVol < volume:
                        rectangle = (22 + self.device.width // 2,
                                     -15 + self.device.height // 2,
                                     30 + self.device.width // 2,
                                     15 + self.device.height // 2)
                        draw.rectangle(rectangle, outline="white", fill="white")
                else:
                    pos = (11 + self.device.width // 2,
                           -30 + self.device.height // 2)
                    draw.text(pos, "X", font=font_hightower, fill="white")
            sleep(self.displayTime)
        self.oldVol = volume

    def draw_loudspeaker(self, draw):
        logger.debug(f'Draw Loudspeaker')
        rectangle = (-34 + self.device.width // 2, -10 + self.device.height // 2,
                     -19 + self.device.width // 2, 10 + self.device.height // 2)
        polygon = [
            (-19 + self.device.width // 2, -10 + self.device.height // 2),
            (-4 + self.device.width // 2, -22 + self.device.height // 2),
            (-4 + self.device.width // 2, 22 + self.device.height // 2),
            (-19 + self.device.width // 2, 10 + self.device.height // 2)
        ]
        draw.rectangle(rectangle, outline="white", fill="white")
        draw.polygon(polygon, outline="white", fill="white")

    def check_and_display_play_status(self, playing):
        logger.debug(f'Display Play Status {playing}')
        if self.oldPlaying != playing:
            showTime = self.displayTime
            if playing == "play":
                self.showPlaySymbol(showTime)
            if playing == "pause":
                self.showPauseSymbol(showTime)
            self.oldPlaying = playing

    def showPauseSymbol(self, showTime):
        logger.info('ShowPauseSymbol')
        draw_functions.drawPauseSymbol(self.device)

        sleep(showTime)

    def showPlaySymbol(self, showTime):
        logger.debug('ShowPlayymbol')
        draw_functions.drawPlaySymbol(self.device)
        sleep(showTime)


    def read_mpc_status(self, use_python_lib=False):
        logger.debug(f'Read MPC status')
        if use_python_lib:
            return self.read_mpc_status_using_python_mpd2()
        mpd_info = self.mpc_client.get_info()
        mpcstatus=''
        mpc_state=mpd_info.get('state')
        currMPC = mpd_info.get('song_description')
        vol = 'V {}'.format(mpd_info['volume'])
        volume = int(mpd_info['volume'])
        duration = '{:01d}:{:02d}'.format(*get_duration(float(mpd_info.get('duration','0'))))
        elapsed = '{:01d}:{:02d}'.format(*get_duration(float(mpd_info.get('elapsed','0'))))
        elapsed = f'{elapsed}/{duration}'
        return currMPC, mpcstatus, mpc_state, vol, volume, elapsed, mpd_info

    def get_volume(self, mpc_state, mpcstatus):
        logger.debug(f'Get Volume')
        if (mpc_state == "play") or (mpc_state == "pause"):
            volume = mpcstatus.split("\n")[2].split("   ")[0].split(":")[1]
        else:
            volume = mpcstatus.split("   ")[0].split(":")[1]
        vol = "V" + str(volume.replace("%", ""))
        volume = int(volume.replace(" ", "").replace("%", ""))
        return vol, volume

    def check_and_update_contrast(self, oldContrast):
        currContrast = GetCurrContrast(self.confFile)
        if currContrast != oldContrast:
            self.device.contrast(currContrast)
            oldContrast = currContrast
        return oldContrast

    def showSpecialInfo(self):
        logger.info('showSpecialInfo')
        specialInfos = GetSpecialInfos()
        if self.special == 0:
            self.special = 1
            self.timetoshow = 10
            os.remove(tempFile)
        self.drawSpecialInfo(specialInfos)
        sleep(1)
        self.timetoshow = self.timetoshow - 1
        if self.timetoshow == 0:
            self.special = 0
        if os.path.exists(tempFile):
            self.timetoshow = 10
            os.remove(tempFile)
            newMode = SetNewMode(self.confFile)
            initVars.set('GENERAL', 'mode', newMode)
            with canvas(self.device) as draw:
                draw.text((0, self.line1), initVars['GENERAL']['mode'], font=font_hightower, fill="white")
            sleep(self.displayTime)

    def drawSpecialInfo(self, specialInfos):
        logger.debug(f'Draw Special Info')
        with canvas(self.device) as draw:
            draw.text((0, self.line1), "WLAN: " + specialInfos[0], font=font_small, fill="white")
            draw.text((0, self.line2), "IP:   " + specialInfos[1], font=font_small, fill="white")
            draw.text((0, self.line3), "Version:", font=font_small, fill="white")
            draw.text((0, self.line4org), version, font=font_small, fill="white")
            draw.rectangle((self.device.width - 4, 0, self.device.width, self.device.height / 10 * self.timetoshow),
                           outline="white", fill="white")

            # draw.line((self.device.width, , self.device.width, self.device.height), fill="white")
            draw.text((110, self.line4org),str(self.timetoshow),font=font_small, fill="white")

    def showSpecialInfoMode(self):
        return (os.path.exists(tempFile)) or (self.special == 1)

    def main(self, num_iterations=sys.maxsize):
        oldContrast = GetCurrContrast(self.confFile)
        self.device.contrast(oldContrast)
        self.ShowImage("music")

        while num_iterations > 0:
            num_iterations -= 1
            sleep(self.update_time)
            self.check_wifi_connection()
            try:
                if self.showSpecialInfoMode():
                    self.showSpecialInfo()
                else:
                    oldContrast = self.check_and_update_contrast(oldContrast)
                    currMPC, mpcstatus, mpc_state, vol, volume, elapsed, mpd_info = self.read_mpc_status()
                    mpc_state = mpd_info['state']
                    self.check_and_display_play_status(mpc_state)
                    self.check_and_display_volume(volume)
                    if (mpc_state == "play") or (mpc_state == "pause"):
                        if mpd_info['song_description'] != self.oldMPC:
                            track = mpd_info['playlisttrack']
                            file = mpd_info['file']
                            if initVars['GENERAL']['mode'] == "full":
                                track, txtLine1, txtLine2, txtLine3 = self.show_change_display(mpd_info)
                        if initVars['GENERAL']['mode'] == "lite":
                            elapsed, track, xpos, xpos_w = self.display_lite_mode(elapsed, file, mpc_state, mpcstatus,
                                                                                  track, xpos_w,mpd_info)
                        elif initVars['GENERAL']['mode'] == "mix":
                            elapsed, track, xpos, xpos_w = self.display_mixed_mode(elapsed, file, mpc_state, mpcstatus,
                                                                                   track, vol, xpos, xpos_w, mpd_info)
                        elif initVars['GENERAL']['mode'] == "full":
                            track = self.display_full_mode(txtLine1, txtLine2, txtLine3, vol, mpd_info)
                    else:
                        self.oldMPC = mpd_info['song_description']
                        if self.tmpcard < 3:
                            sleep(0.5)
                            self.tmpcard += 1
                        else:
                            self.ShowImage("cardhand")
                            self.tmpcard = 0
            except Exception as error:
                logger.exception(error)
                sleep(0.5)
                self.ShowImage("music")

if __name__ == "__main__":
    initVars = Init(confFile)

    device = get_device(initVars['GENERAL']['controller'], height=initVars['GENERAL'].get('height', 64))
    device.persist = True
    display = PhonieBoxOledDisplay(device=device)


    def sigterm_handler(signal, frame):
        # save the state here or do whatever you want
        logger.info('Handling sigterm')
        display.cleanup()
        logger.info('exit')
        os._exit(0)


    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        display.main()
    except KeyboardInterrupt:
        display.cleanup()
        os._exit(0)
        pass
