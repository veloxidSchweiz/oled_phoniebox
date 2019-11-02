from mpd import MPDClient
import queue
from collections import deque
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
logger.setLevel('DEBUG')

def with_connection(func):
    def wrapper(*args):
        self=args[0]
        try:
            self.client.ping()
        except Exception:
            self.reconnect()
        return func(*args)
    return wrapper

def with_reconnect(func):
    def wrapper(*args):
        self=args[0]
        for i in range(3):
            try:
                self.client.ping()
                return func(*args)
            except Exception:
                self.reconnect()
    return wrapper

class MPCStatusReader():
    def __init__(self):
        logger.info('INIT')
        self.client = MPDClient()
        self.client.timeout = 10  # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None  # timeout for fetching the result of the idle command is handled seperately, default: None
        self.host ='localhost'
        self.port = 6600
        self.connect()
        self.messages = deque()

    def reconnect(self):
        logger.info('reconnect')
        self.client.disconnect()
        self.connect()

    def connect(self):
        logger.info('connect')
        self.client.connect(self.host, self.port)
        #self.client.subscribe('phoniebox')

    @with_connection
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @with_reconnect
    def perform_command(self, command, *args):
        return getattr(self.client,command)(*args)


    @with_connection
    def get_status(self):
        return self.client.status()

    @with_connection
    def get_currentsong(self):
        return self.client.currentsong()

    def get_info(self):
        status = self.read_info_from_mpd()
        if 'duration' not in status:
            status['duration'] = status['time'].split(":")[-1]
            t = int(status['duration'])
            status['duration_as_time'] = '{:02}:{:02}'.format(t//60,t%60)
            t = round(float((status['elapsed'])))
            status['elapsed_as_time'] = '{:02}:{:02}'.format(t//60,t%60)

        status['playlisttrack'] = f"{status.get('song','-')}/{status['playlistlength']}"
        if status.get('file','').startswith("http"):
            status['rel_elapsed_time'] = 1.0
            status['song_description'] = f'{status.get("name")}'
        else:
            status['rel_elapsed_time'] = round(float(status.get('elapsed',0))/float(status.get('duration',1)),2)
            status['song_description'] = f"{status.get('artist')} - {status.get('title')}"

        return status

    def read_info_from_mpd(self):
        status = self.get_currentsong()
        status.update(self.get_status())
        return status

    @with_connection
    def readmessages(self):
        new_messages = self.client.readmessages()
        self.messages.extend(new_messages)
        return len(new_messages)

    def has_messages(self):
        self.readmessages()
        return len(self.messages) > 0

    def get_message(self):
        if len(self.messages):
            return self.messages.popleft()
        return None
