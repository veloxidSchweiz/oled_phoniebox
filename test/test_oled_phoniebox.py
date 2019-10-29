import mock
import pytest

from luma.core.render import canvas
from luma.core import device as luma_device
from oled_phoniebox import PhonieBoxOledDisplay
from unittest.mock import MagicMock, patch
from unittest.mock import patch

from scripts.o4p_functions import SetCharacters, GetMPC


@pytest.fixture
def mocked_display():
    display = mock.MagicMock()
    display.size = (128, 64)
    display.height = 64
    display.width = 128
    display.mode='RGBA'
    return display

def MockedGetSpecialInfos():
    return ('MyWlan', '192.168.123.123')

# @pytest.fixture(params=[128,64])
@pytest.fixture(params=[64])
def width(request):
    return request.param

@pytest.fixture
@mock.patch('scripts.o4p_functions', side_effect=MockedGetSpecialInfos)
def mocked_oled_display(mocked_info, width, mocked_display):
    mocked_info.GetSpecialInfos.side_effect=MockedGetSpecialInfos
    return PhonieBoxOledDisplay(luma_device.dummy(width=128, height=128, rotate=0, mode='1'))

# @mock.patch('scripts.o4p_functions', side_effect=MockedGetSpecialInfos)
# def fixture_test(request, mocked_display,mocked_info):
#     mocked_info.GetSpecialInfos.side_effect=MockedGetSpecialInfos
#     return PhonieBoxOledDisplay(luma_device.dummy(width=128, height=request.param, rotate=0, mode='1'))

class TestPhonieBoxOledDisplay():
    def test_init(self, mocked_display):
        mocked_oled_display = PhonieBoxOledDisplay(mocked_display)

    @pytest.mark.parametrize('image_name', [('music'), ('cardhand'), ('poweroff')])
    def test_ShowImage(self, mocked_oled_display, image_name, ):
        mocked_oled_display.ShowImage(image_name)

    def test_showSpecialInfo(self, mocked_oled_display):
        mocked_oled_display.special = 1
        mocked_oled_display.showSpecialInfo()
        mocked_oled_display

    @pytest.mark.skip
    def test_main(self, mocked_oled_display):
        mocked_oled_display.main(num_iterations=5)

    def test_showPlaySymbol(self,mocked_oled_display):
        mocked_oled_display.showPlaySymbol(0)

    def test_showPauseSymbol(self,mocked_oled_display):
        mocked_oled_display.showPauseSymbol(0)
        mocked_oled_display.device.image.show()

    def test_read_mpc_status(self,mocked_oled_display):
        print(mocked_oled_display.read_mpc_status())

    @pytest.mark.parametrize('file',
                             [('01_peter_fox_and_cold_steel_-_live_aus_berlin.mp3\n'),
                              ('http://www.das_ist.ein/stream.mp3')])
    def test_display_lite_mode(self, mocked_oled_display, file):
        currMPC, mpcstatus, mpc_state, vol, volume, elapsed = mocked_oled_display.read_mpc_status()
        file = SetCharacters(GetMPC("mpc -f %file% current"))  # Get the current title
        track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","")
        mocked_oled_display.WifiConn =('white', 'white', 'black', 'black', 'black')
        mocked_oled_display.display_lite_mode(elapsed, file, mpc_state, mpcstatus, track, 0)
        # mocked_oled_display.device.image.show()

    @pytest.mark.parametrize('file',
                             [('01_peter_fox_and_cold_steel_-_live_aus_berlin.mp3\n'),
                              ('http://www.das_ist.ein/stream.mp3')])
    def test_display_mixed_mode(self,mocked_oled_display, file):

        currMPC, mpcstatus, mpc_state, vol, volume, elapsed = mocked_oled_display.read_mpc_status()
        file = SetCharacters(GetMPC("mpc -f %file% current"))  # Get the current title
        track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","")
        mocked_oled_display.WifiConn =('white', 'white', 'black', 'black', 'black')
        #                        elapsed, file, mpc_state, mpcstatus, track, vol, xpos, xpos_w)
        mocked_oled_display.display_mixed_mode(elapsed, file, mpc_state, mpcstatus, track, vol, 0, 0)
        # mocked_oled_display.device.image.show()

    @pytest.mark.parametrize('file',
                             [('01_peter_fox_and_cold_steel_-_live_aus_berlin.mp3\n'),])
                              # ('http://www.das_ist.ein/stream.mp3')])
    def test_display_full_mode(self,mocked_oled_display, file):
        for i in range(19):
            currMPC, mpcstatus, mpc_state, vol, volume, elapsed = mocked_oled_display.read_mpc_status()
            file = SetCharacters(GetMPC("mpc -f %file% current"))  # Get the current title
            track = mpcstatus.split("\n")[1].replace("  ", " ").split(" ")[1].replace("#","")
            mocked_oled_display.WifiConn =('white', 'white', 'black', 'black', 'white')
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
            #                        elapsed, file, mpc_state, mpcstatus, track, vol, xpos, xpos_w)

            mocked_oled_display.display_full_mode(currMPC, elapsed, file, mpc_state, mpcstatus, track, txtLine1, txtLine2, txtLine3, vol)
            mocked_oled_display.device.image.show()

    @pytest.mark.parametrize('quality, expected',
                             [
                                 (-10, ('black', 'black', 'black', 'black', 'white')),
                                 (0, ('black', 'black', 'black', 'black', 'black')),
                                 (1, ('white', 'black', 'black', 'black', 'black')),
                                 (10, ('white', 'black', 'black', 'black', 'black')),
                                 (20, ('white', 'black', 'black', 'black', 'black')),
                                 (30, ('white', 'black', 'black', 'black', 'black')),
                                 (40, ('white', 'black', 'black', 'black', 'black')),
                                 (50, ('white', 'white', 'black', 'black', 'black')),
                                 (60, ('white', 'white', 'black', 'black', 'black')),
                                 (70, ('white', 'white', 'white', 'black', 'black')),
                                 (80, ('white', 'white', 'white', 'black', 'black')),
                                 (90, ('white', 'white', 'white', 'white', 'black')),
                                 (100, ('white', 'white', 'white', 'white', 'black')),
                                 (110, ('white', 'white', 'white', 'white', 'black')),
                                 ('a',('black', 'black', 'black', 'black', 'white'))])
    def test_show_wifi_connection(self,quality, expected, mocked_oled_display):
            mocked_oled_display.WifiConn = expected
            with canvas(mocked_oled_display.device) as draw:
                mocked_oled_display.show_wifi_connection(draw)
            mocked_oled_display.device.image.show()

    @pytest.mark.parametrize("oldVol,newVol",
                             [(0,1),(1,0),(2,1),(0,100)])
    def test_check_and_display_volume(self, oldVol,newVol, mocked_oled_display):
        mocked_oled_display.oldVol = oldVol
        mocked_oled_display.check_and_display_volume(newVol)
        mocked_oled_display.device.image.show()


    @pytest.mark.parametrize("status",
                             [('[playing]'),'[paused]'])
    def test_check_and_display_play_status(self, status, mocked_oled_display):
        mocked_oled_display.check_and_display_play_status(status)
        mocked_oled_display.device.image.show()