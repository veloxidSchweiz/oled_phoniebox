import mock
import pytest

from luma.core.render import canvas
from luma.core import device as luma_device
from oled_phoniebox import PhonieBoxOledDisplay
from unittest.mock import MagicMock, patch
from unittest.mock import patch

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

@pytest.fixture(params=[128,64])
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




