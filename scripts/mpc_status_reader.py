from mpd import MPDClient
import queue
from collections import deque

def with_connection(func):
    def wrapper(*args):
        self=args[0]
        try:
            self.client.ping()
        except ConnectionError:
            self.connect()
        return func(*args)
    return wrapper

class MPCStatusReader():
    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 10  # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None  # timeout for fetching the result of the idle command is handled seperately, default: None
        self.host ='localhost'
        self.port = 6600
        self.connect()
        self.messages = deque()

    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.subscribe('phoniebox')

    @with_connection
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @with_connection
    def get_status(self):
        return self.client.status()

    @with_connection
    def get_currentsong(self):
        return self.client.currentsong()

    def get_info(self):
        status = self.get_currentsong()
        status.update(self.get_status())
        status['playlisttrack'] = f"{status.get('song','-')}/{status['playlistlength']}"
        if status.get('file','').startswith("http"):
            status['rel_elapsed_time'] = 1.0
            status['song_description'] = f'{status.get("title")}'
        else:
            status['rel_elapsed_time'] = round(float(status.get('elapsed',0))/float(status.get('duration',1)),2)
            status['song_description'] = f"{status.get('artist')} - {status.get('title')}"

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