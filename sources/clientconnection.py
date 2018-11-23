from multiprocessing.connection import *
from sharedconstants import *

POLL_INTERVAL = 0.01


class ClientConnection:
    def __init__(self):
        self.socket = Client(ADDRESS)
        self.is_waiting = False

    def respond(self, message=None):
        if self.socket.closed:
            return
        self.socket.send(message)
        self.is_waiting = False

    def poll(self):
        message = None
        if self.socket.poll(POLL_INTERVAL):
            message = self.socket.recv()
            self.is_waiting = True
        return message

    def stop(self):
        self.respond()
        self.socket.close()
