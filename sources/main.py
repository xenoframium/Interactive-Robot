from multiprocessing.connection import *
from subprocess import Popen
from sharedconstants import *
import sys
import code
import time

Popen([sys.executable, "game.py"])
listener = Listener(ADDRESS)
socket = listener.accept()


def generate_targets(num_targets, proportions=(1, 1)):
    if proportions[0] < 0 or proportions[1] < 0:
        print("Error, both proportions must be greater than or equal to 0")
        return
    if proportions[0] < 1 and proportions[1] < 1:
        print("Error, at least one of the proportions must be greater or equal to 1")
        return
    socket.send((GENERATE_TARGETS, num_targets, (int(proportions[0]), int(proportions[1]))))
    while not socket.poll(0.01):
        time.sleep(0.01)
    socket.recv()


def get_shootable_targets():
    socket.send((GET_SHOOTABLE_TARGETS,))
    while not socket.poll(0.01):
        time.sleep(0.01)
    return socket.recv()


def get_treadable_targets():
    socket.send((GET_TREADABLE_TARGETS,))
    while not socket.poll(0.01):
        time.sleep(0.01)
    return socket.recv()


def terminate():
    socket.send((None,))
    socket.close()
    listener.close()
    exit()


class ProxyRobot:
    def __get_response(self):
        while not socket.poll(0.01):
            time.sleep(0.01)
        return socket.recv()

    def __communicate(self, message):
        socket.send(message)
        return self.__get_response()

    def __rotate(self, angle):
        self.__communicate((ROTATE, angle))

    def turn(self, angle):
        self.__rotate(-angle)

    def move(self, distance):
        self.__communicate((MOVE, distance))

    def get_location(self):
        return self.__communicate((GET_LOCATION,))

    def get_bearing(self):
        return self.__communicate((GET_BEARING,))

    def shoot(self):
        self.__communicate((SHOOT,))

    def turn_to(self, x, y):
        self.__communicate((TURN_TO, x, y))

    def move_to(self, x, y):
        self.__communicate((MOVE_TO, x, y))


robot = ProxyRobot()


def main():
    code.interact(local=globals())

if __name__ == '__main__':
    main()
