import mock
import pytest
from luma.core import device as luma_device
from luma.core.render import canvas

from oled_phoniebox import PhonieBoxOledDisplay

show_images = False


@pytest.fixture
def mocked_display():
    display = mock.MagicMock()
    display.size = (128, 64)
    display.height = 64
    display.width = 128
    display.mode = 'RGBA'
    return display


def MockedGetSpecialInfos():
    return ('MyWlan', '192.168.123.123')


@pytest.fixture
@mock.patch('scripts.o4p_functions.GetMPC')
def MockedGetMpcStatus(mockedGetMPC, mpc_status_ouput):
    mockedGetMPC.return_value = mpc_status_ouput


@pytest.fixture(params=[128, 64])
# @pytest.fixture(params=[64])
def width(request):
    return request.param


@pytest.fixture
@mock.patch('scripts.o4p_functions', side_effect=MockedGetSpecialInfos)
def oled_display(mocked_info, width, mocked_display):
    mocked_info.GetSpecialInfos.side_effect = MockedGetSpecialInfos
    return PhonieBoxOledDisplay(luma_device.dummy(width=128, height=128, rotate=0, mode='1'))


@pytest.fixture
def mocked_oled_display(oled_display, mpc_status_mock):
    with mock.patch('oled_phoniebox.MPCStatusReader.read_info_from_mpd') as \
            mocked_mpd_status_reader:
        mocked_mpd_status_reader.return_value = mpc_status_mock
        return oled_display


# @mock.patch('scripts.o4p_functions', side_effect=MockedGetSpecialInfos)
# def fixture_test(request, mocked_display,mocked_info):
#     mocked_info.GetSpecialInfos.side_effect=MockedGetSpecialInfos
#     return PhonieBoxOledDisplay(luma_device.dummy(width=128, height=request.param, rotate=0, mode='1'))

class TestPhonieBoxOledDisplay():
    def test_init(self, mocked_display):
        mocked_oled_display = PhonieBoxOledDisplay(mocked_display)

    @pytest.mark.parametrize('image_name', [('music'), ('cardhand'), ('poweroff')])
    def test_ShowImage(self, oled_display, image_name, ):
        oled_display.ShowImage(image_name)

    def test_showSpecialInfo(self, oled_display):
        oled_display.special = 1
        oled_display.showSpecialInfo()
        mocked_oled_display

    # @pytest.mark.skip
    def test_main(self, oled_display):
        oled_display.main(num_iterations=5)

    def test_showPlaySymbol(self, oled_display):
        oled_display.showPlaySymbol(0)

    def test_showPauseSymbol(self, oled_display):
        oled_display.showPauseSymbol(0)
        if show_images:
            oled_display.device.image.show()

    @pytest.mark.parametrize('file',
                             [('01_peter_fox_and_cold_steel_-_live_aus_berlin.mp3\n'),
                              ('http://www.das_ist.ein/stream.mp3')])
    def test_display_lite_mode(self, mocked_oled_display, file):
        currMPC, mpcstatus, mpc_state, vol, volume, elapsed, mpd_info = mocked_oled_display.read_mpc_status()
        file = mpd_info['file']  # Get the current title
        track = mpd_info['playlisttrack']
        mocked_oled_display.WifiConn = ('white', 'white', 'black', 'black', 'black')
        mocked_oled_display.display_lite_mode(elapsed, file, mpc_state, mpcstatus, track, 0)
        if show_images:
            mocked_oled_display.device.image.show()

    @pytest.mark.parametrize('file',
                             [('01_peter_fox_and_cold_steel_-_live_aus_berlin.mp3\n'),
                              ('http://www.das_ist.ein/stream.mp3')])
    def test_display_mixed_mode(self, mocked_oled_display, file):

        currMPC, mpcstatus, mpc_state, vol, volume, elapsed, mpd_info = mocked_oled_display.read_mpc_status()
        file = mpd_info['file']  # Get the current title
        track = mpd_info['playlisttrack']

        mocked_oled_display.WifiConn = ('white', 'white', 'black', 'black', 'black')
        #                        elapsed, file, mpc_state, mpcstatus, track, vol, xpos, xpos_w)
        mocked_oled_display.display_mixed_mode(elapsed, file, mpc_state, mpcstatus, track, vol, 0, 0)
        if show_images:
            mocked_oled_display.device.image.show()

    @pytest.mark.parametrize('file',
                             [('01_peter_fox_and_cold_steel_-_live_aus_berlin.mp3\n'), ])
    # ('http://www.das_ist.ein/stream.mp3')])
    def test_display_full_mode(self, mocked_oled_display, file):
        for i in range(19):
            currMPC, mpcstatus, mpc_state, vol, volume, elapsed, mpd_info = mocked_oled_display.read_mpc_status()
            mocked_oled_display.WifiConn = ('white', 'white', 'black', 'black', 'white')
            txtLine1 = mpd_info.get('album', '')
            txtLine3 = mpd_info['title']
            txtLine2 = mpd_info.get('artist', mpd_info.get('name', ''))
            if txtLine2 == "\n":
                filename = mpd_info['file']
                localfile = filename.split("/")
                txtLine1 = localfile[1]
                txtLine2 = localfile[0]
            #                        elapsed, file, mpc_state, mpcstatus, track, vol, xpos, xpos_w)

            mocked_oled_display.display_full_mode(txtLine1, txtLine2, txtLine3, vol, mpd_info)
            if show_images:
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
                                 ('a', ('black', 'black', 'black', 'black', 'white'))])
    def test_show_wifi_connection(self, quality, expected, oled_display):
        oled_display.WifiConn = expected
        with canvas(oled_display.device) as draw:
            oled_display.show_wifi_connection(draw)
        if show_images:
            oled_display.device.image.show()

    @pytest.mark.parametrize("oldVol,newVol",
                             [(0, 1), (1, 0), (2, 1), (0, 100)])
    def test_check_and_display_volume(self, oldVol, newVol, oled_display):
        oled_display.oldVol = oldVol
        oled_display.check_and_display_volume(newVol)
        if show_images:
            oled_display.device.image.show()

    @pytest.mark.parametrize("status",
                             [('play'), 'pause'])
    def test_check_and_display_play_status(self, status, oled_display):
        oled_display.check_and_display_play_status(status)
        if show_images:
            oled_display.device.image.show()

    def test_show_change_display(self, mocked_oled_display, mpc_status_mock):
        currMPC, mpcstatus, mpc_state, vol, volume, elapsed, mpd_info = mocked_oled_display.read_mpc_status()
        track, txtLine1, txtLine2, txtLine3 = mocked_oled_display.show_change_display(mpd_info)
        vol = 'V100'
        for i in range(10):
            mocked_oled_display.display_full_mode(txtLine1, txtLine2, txtLine3, vol, mpd_info)

    def test_drawSpecialInfo(self, oled_display):
        specialInfo = ['TestWlan', '123.456.789.000']
        for i in range(10):
            oled_display.timetoshow = i
            oled_display.drawSpecialInfo(specialInfos=specialInfo)
            # oled_display.device.image.show()
