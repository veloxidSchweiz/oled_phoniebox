#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
#
import platform
from luma.core import device as luma_device
from mpd import MPDClient
def Init(File):
    import configparser
    config = configparser.ConfigParser()
    config.read(File)
    config.sections()
    return config

def get_device(deviceName,height=64,width=128):
    from luma.core import cmdline, error
    """
    Create device from command-line arguments and return it.
    """
    if deviceName == 'dummy':
        device = luma_device.dummy(width=width, height=height, rotate=0, mode='RGB')
    else:
        actual_args = ['-d', deviceName,'--height', str(height),'--width', str(width)]
        parser = cmdline.create_parser(description='luma.examples arguments')
        args = parser.parse_args(actual_args)
        if args.config:
            # load config from file
            config = cmdline.load_config(args.config)
            args = parser.parse_args(config + actual_args)
        # create device
        try:
            device = cmdline.create_device(args)
        except error.Error as e:
            parser.error(e)
    return device

def GetCurrContrast(config):
    return int(config['GENERAL']['contrast'])

def SetNewMode(File):
    import configparser
    config = configparser.ConfigParser()
    config.read(File)
    config.sections()
    if config['GENERAL']['mode'] == "full":
        config.set('GENERAL', 'mode', 'lite')
    elif config['GENERAL']['mode'] == "lite":
        config.set('GENERAL', 'mode', 'mix')
    elif config['GENERAL']['mode'] == "mix":
        config.set('GENERAL', 'mode', 'full')
    with open(File, 'w') as configfile:
        config.write(configfile)
    return config['GENERAL']['mode']

def SetCharacters(text):
    chars = {'ö':chr(246),'ä':chr(228),'ü':chr(252),'ß':chr(223),'Ä':chr(196),'Ü':chr(220),'Ö':chr(214),'%20':' ',' 1/4':chr(252),'%C3%9C':chr(220),'%C3%BC':chr(252),'%C3%84':chr(196),'%C3%A4':chr(228),'%C3%96':chr(214),'%C3%B6':chr(246),'%C3%9F':chr(223)}
    for char in chars:
        text = text.replace(char,chars[char])
    return text

def GetMPC(command):
    from subprocess import check_output
    process = check_output(command.split())
    process = process.decode()
    return process

def GetWifiConn():
    first = "black"
    second = "black"
    third = "black"
    fourth = "black"
    alternate = "black"
    try:
        WifiRate = get_wifi_quality()
        if WifiRate > 0:
            first = "white"
        if WifiRate > 40:
            second = "white"
        if WifiRate > 60:
            third = "white"
        if WifiRate > 80:
            fourth = "white"
    except:
        alternate = "white"
    return (first,second,third,fourth,alternate)


def get_wifi_quality():
    WifiRate = readWifiRateFile()
    WifiRate = WifiRate[2].replace("   ", " ").replace("  ", " ")
    WifiRate = WifiRate.split(" ")
    WifiRate = WifiRate[4].replace(".", "")
    if WifiRate[0:1] == "-":
        WifiRate = 100 + float(WifiRate)
    else:
        WifiRate = float(WifiRate)
    return WifiRate


def readWifiRateFile():
    '''
    Format:
    ['Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE',
 ' face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22',
 'wlp1s0: 0000   53.  -57.  -256        0      0      0      3   1001        0']
    :param WifiFile:
    :return:
    '''
    WifiFile = "/proc/net/wireless"
    WifiRateFile = open(WifiFile)
    WifiRate = WifiRateFile.readlines()
    WifiRateFile.close()
    return WifiRate



def GetSpecialInfos():
    if platform.system() == 'Darwin':
        import wifiinfo, socket
        wifi = wifiinfo.getWifi('osx')
        wlan = wifi.get('SSID')
        ip = socket.gethostbyname(socket.gethostname())
    else:
        from subprocess import check_output
        process = check_output("iwgetid".split())
        process = process.decode()
        wlan = process.split(":")[1].replace('"','').replace('\n','')
        import netifaces as ni
        ni.ifaddresses('wlan0')
        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return (wlan, ip)

