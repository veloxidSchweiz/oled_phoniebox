import mock
import pytest

from scripts.o4p_functions import GetSpecialInfos, GetWifiConn, get_device
from luma.core.device import dummy  as luma_dummy_device

def test_GetSpecialInfos():
    print(GetSpecialInfos())

@pytest.mark.parametrize('quality, expected',
                         [
                          (-10,('black', 'black', 'black', 'black', 'black')),
                          (0,('black', 'black', 'black', 'black', 'black')),
                          ( 1,('white', 'black', 'black', 'black', 'black')),
                          (10,('white', 'black', 'black', 'black', 'black')),
                          (20,('white', 'black', 'black', 'black', 'black')),
                          (30,('white', 'black', 'black', 'black', 'black')),
                          (40,('white', 'black', 'black', 'black', 'black')),
                          (50,('white', 'white', 'black', 'black', 'black')),
                          (60,('white', 'white', 'black', 'black', 'black')),
                          (70,('white', 'white', 'white', 'black', 'black')),
                          (80,('white', 'white', 'white', 'black', 'black')),
                          (90,('white', 'white', 'white', 'white', 'black')),
                          (100,('white', 'white', 'white', 'white', 'black')),
                          (110,('white', 'white', 'white', 'white', 'black'))])
@mock.patch('scripts.o4p_functions.get_wifi_quality')
def test_GetWifiConn(mocked_wifi_quality, quality, expected):
    mocked_wifi_quality.return_value = quality
    assert GetWifiConn() ==  expected

def test_get_device():
    width=128
    device = get_device(deviceName='dummy',width = width)
    assert isinstance(device,luma_dummy_device)
    assert device.width == width
