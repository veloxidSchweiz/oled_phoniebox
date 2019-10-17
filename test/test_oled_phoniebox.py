import mock
import pytest

from oled_phoniebox import PhonieBoxOledDisplay


@pytest.fixture
def mocked_display():
    display =  mock.MagicMock()
    display.size = (128, 64)
    display.height = 64
    display.width = 128
    display.mode='RGBA'
    return display


@pytest.fixture
def mocked_oled_display(mocked_display):
    return PhonieBoxOledDisplay(mocked_display)


class TestPhonieBoxOledDisplay():
    def test_init(self, mocked_display):
        mocked_oled_display = PhonieBoxOledDisplay(mocked_display)

    # @pytest.mark.parametrize('image_name', ['music', 'cardhand', 'poweroff'])
    @pytest.mark.parametrize("x", [(0), (1)])
    def test_ShowImage(self, mocked_oled_display, x):
        mocked_oled_display.ShowImage('music')
        mocked_oled_display.ShowImage('cardhand')
        mocked_oled_display.ShowImage('poweroff')
        mocked_oled_display.ShowImage('musiccard')



    @pytest.mark.skipif(True)
    def test_main(self, mocked_oled_display):
        mocked_oled_display.main()
