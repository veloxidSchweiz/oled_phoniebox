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
], ids=['http_stream', 'playing', 'pause', 'stop'])
def mpc_status_ouput(request):
    return request.param


mpc_status_http_playing = {
    'file': 'https://wdr-1live-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3?ar-key'
            '=BcG5DcAgEATAYiwRIvY-9gKKwSdTggNX75l34Wu1KB3IDo7O9iy4SpAAFH6pVYzct5Ql_XBIGI_uWZE2PX4',
    'name': '1Live, Westdeutscher Rundfunk Koeln', 'pos': '5', 'id': '6', 'volume': '100',
    'repeat': '0', 'random': '0', 'single': '0', 'consume': '0', 'playlist': '10',
    'playlistlength': '6', 'mixrampdb': '0.000000', 'state': 'play', 'song': '5', 'songid': '6',
    'time': '371:0', 'elapsed': '371.160', 'bitrate': '128', 'audio': '48000:24:2',
    'playlisttrack': '5/6', 'rel_elapsed_time': 1.0
}

mpc_status_mp3_playing = {
    'file': '07 - Fredrik Vahle - Wolkenlied.mp3', 'last-modified': '2019-10-31T17:47:53Z',
    'artist': 'Fredrik Vahle', 'albumartist': 'Fredrik Vahle', 'artistsort': 'Vahle, Fredrik',
    'albumartistsort': 'Vahle, Fredrik', 'title': 'Wolkenlied', 'album': 'Der Friedensmacher',
    'track': '7', 'genre': 'Kinder', 'disc': '1',
    'musicbrainz_albumid': '6ec8a88f-36d3-4e75-93d1-7129cf635257',
    'musicbrainz_artistid': '6670101d-070a-4fc9-92c4-e60bf0cc3cae',
    'musicbrainz_albumartistid': '6670101d-070a-4fc9-92c4-e60bf0cc3cae',
    'musicbrainz_releasetrackid': '15aa422f-c2da-371d-ba82-a6735690bc6d',
    'musicbrainz_trackid': 'bb6a0191-4178-4fbb-ae14-ec6b091e2698', 'time': '31:279',
    'duration': '279.118', 'pos': '4', 'id': '5', 'volume': '100', 'repeat': '0', 'random': '0',
    'single': '0', 'consume': '0', 'playlist': '10', 'playlistlength': '6',
    'mixrampdb': '0.000000', 'state': 'play', 'song': '4', 'songid': '5', 'elapsed': '31.416',
    'bitrate': '192', 'audio': '44100:24:2', 'nextsong': '5', 'nextsongid': '6',
    'playlisttrack': '4/6', 'rel_elapsed_time': 0.11
}

mpc_status_mp3_paused = {
    'file': '07 - Fredrik Vahle - Wolkenlied.mp3', 'last-modified': '2019-10-31T17:47:53Z',
    'artist': 'Fredrik Vahle', 'albumartist': 'Fredrik Vahle', 'artistsort': 'Vahle, Fredrik',
    'albumartistsort': 'Vahle, Fredrik', 'title': 'Wolkenlied', 'album': 'Der Friedensmacher',
    'track': '7', 'genre': 'Kinder', 'disc': '1',
    'musicbrainz_albumid': '6ec8a88f-36d3-4e75-93d1-7129cf635257',
    'musicbrainz_artistid': '6670101d-070a-4fc9-92c4-e60bf0cc3cae',
    'musicbrainz_albumartistid': '6670101d-070a-4fc9-92c4-e60bf0cc3cae',
    'musicbrainz_releasetrackid': '15aa422f-c2da-371d-ba82-a6735690bc6d',
    'musicbrainz_trackid': 'bb6a0191-4178-4fbb-ae14-ec6b091e2698', 'time': '107:279',
    'duration': '279.118', 'pos': '4', 'id': '5', 'volume': '100', 'repeat': '0', 'random': '0',
    'single': '0', 'consume': '0', 'playlist': '10', 'playlistlength': '6',
    'mixrampdb': '0.000000', 'state': 'pause', 'song': '4', 'songid': '5', 'elapsed': '107.067',
    'bitrate': '192', 'audio': '44100:24:2', 'nextsong': '5', 'nextsongid': '6',
    'playlisttrack': '4/6', 'rel_elapsed_time': 0.38
}

mpc_status_mp3_stopped = {
    'file': '07 - Fredrik Vahle - Wolkenlied.mp3',
    'last-modified': '2019-10-31T17:47:53Z',
    'artist': 'Fredrik Vahle',
    'albumartist': 'Fredrik Vahle',
    'artistsort': 'Vahle, Fredrik',
    'albumartistsort': 'Vahle, Fredrik',
    'title': 'Wolkenlied',
    'album': 'Der Friedensmacher',
    'track': '7',
    'genre': 'Kinder',
    'disc': '1',
    'musicbrainz_albumid': '6ec8a88f-36d3-4e75-93d1-7129cf635257',
    'musicbrainz_artistid': '6670101d-070a-4fc9-92c4-e60bf0cc3cae',
    'musicbrainz_albumartistid': '6670101d-070a-4fc9-92c4-e60bf0cc3cae',
    'musicbrainz_releasetrackid': '15aa422f-c2da-371d-ba82-a6735690bc6d',
    'musicbrainz_trackid': 'bb6a0191-4178-4fbb-ae14-ec6b091e2698',
    'time': '279', 'duration': '279.118', 'pos': '4',
    'id': '5',
    'volume': '100',
    'repeat': '0', 'random': '0', 'single': '0', 'consume': '0', 'playlist': '10',
    'playlistlength': '6', 'mixrampdb': '0.000000',
    'state': 'stop',
    'song': '4', 'songid': '5', 'nextsong': '5',
    'nextsongid': '6',
    'playlisttrack': '4/6', 'rel_elapsed_time': 0.0
}



@pytest.fixture(params=[
    mpc_status_http_playing,
    mpc_status_mp3_playing,
    mpc_status_mp3_paused,
    mpc_status_mp3_stopped
], ids=['http_stream', 'playing', 'pause', 'stop'])
def mpc_status(request):
    return request.param

