from robot import *
from clientconnection import ClientConnection
from sharedconstants import *
from world import *
from random import *


class GameInstance:
    def __init__(self):
        self.gui = GUI(self.tick)
        self.event_poller = ClientConnection()
        self.world = World()
        self.robot = Robot(self.world, self.gui.canvas, self.event_poller)

    def handle_event(self, event):
        if event is None:
            return
        elif event[0] is None:
            self.stop()
        elif event[0] == MOVE:
            self.robot.move(event[1])
        elif event[0] == ROTATE:
            self.robot.rotate(event[1])
        elif event[0] == GET_LOCATION:
            self.event_poller.respond(self.robot.get_location())
        elif event[0] == GET_BEARING:
            self.event_poller.respond(self.robot.get_bearing())
        elif event[0] == SHOOT:
            self.robot.shoot()
        elif event[0] == TURN_TO:
            self.robot.turn_to(event[1], event[2])
        elif event[0] == MOVE_TO:
            self.robot.move_to(event[1], event[2])
        elif event[0] == GENERATE_TARGETS:
            self.generate_targets(event[1], event[2][0], event[2][1])
        elif event[0] == GET_SHOOTABLE_TARGETS:
            targets = []
            for target in self.world.shootable_targets:
                targets.append((target.position.x, target.position.y))
            self.event_poller.respond(targets)
        elif event[0] == GET_TREADABLE_TARGETS:
            targets = []
            for target in self.world.treadable_targets:
                targets.append((target.position.x, target.position.y))
            self.event_poller.respond(targets)

    def tick(self):
        if not self.robot.is_moving():
            self.handle_event(self.event_poller.poll())
        self.robot.update()
        self.world.update(self.robot)

    def run(self):
        self.gui.mainloop()

    def stop(self):
        self.gui.stop()
        self.event_poller.stop()

    def generate_targets(self, number, proportion_shootable, proportion_treadable):
        for i in range(0, number):
            x = randrange(TARGET_SIZE, CANVAS_WIDTH - TARGET_SIZE)
            y = randrange(TARGET_SIZE, CANVAS_HEIGHT - TARGET_SIZE)
            if i % (proportion_shootable + proportion_treadable) < proportion_shootable:
                self.world.shootable_targets.append(ShootTarget(self.gui.canvas, Vector(x, y)))
            else:
                self.world.treadable_targets.append(TreadTarget(self.gui.canvas, Vector(x, y)))
        self.event_poller.respond()


def main():
    game_instance = GameInstance()
    game_instance.run()

main()
