import logging

import pytest


http_stream = 'http://icecast.radio24.ch/radio24-rc-96-aac\n[playing] #2/2   0:00/0:00 (0%)\nvolume: 20%   repeat: off   random: off   single: off   consume: off'
playing = "Norah Jones - Don't Know Why\n[playing] #4/4   0:04/3:06 (2%)\nvolume: 20%   repeat: off   random: off   single: off   consume: off"
pause = "Norah Jones - Don't Know Why\n[paused]  #4/4   0:44/3:06 (23%)\nvolume: 20%   repeat: off   random: off   single: off   consume: off"
stop = "volume: 20%   repeat: off   random: off   single: off   consume: off"

@pytest.fixture(params=[
    http_stream,
    playing,
    pause,
    stop
],ids=['http_stream','playing','pause','stop'])
def mpc_status_ouput(request):
    return request.param