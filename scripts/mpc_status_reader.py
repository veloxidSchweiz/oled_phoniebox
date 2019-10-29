from mpd import MPDClient
import queue

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
        self.messages = queue.Queue()

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
        return status

    @with_connection
    def readmessages(self):
        list(map(self.messages.put, self.client.readmessages()))

        return

    def has_messages(self):
        self.messages.extend(self.readmessages())
        return len(self.messages) > 0

    def get_message(self):
        msg = self.message.get()