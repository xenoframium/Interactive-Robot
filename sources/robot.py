from projectile import *
from math import *
from collections import *
from sharedconstants import *

ROBOT_MOVE_INCREMENT = 2
ROBOT_TURN_INCREMENT = 4

RESPOND = "robot_RESPOND"

class Robot:
    def __init__(self, world, canvas, event_poller):
        self.position = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
        self.direction = 0
        self.render_object = RobotRenderComponent(canvas, self.position)
        self.rotation_remaining = 0
        self.movement_remaining = 0
        self.event_poller = event_poller
        self.world = world
        self.canvas = canvas
        self.event_queue = deque()

    def update_rotation(self):
        if self.rotation_remaining != 0:
            if self.rotation_remaining > ROBOT_TURN_INCREMENT:
                self.rotation_remaining -= ROBOT_TURN_INCREMENT
                self.__rotate(ROBOT_TURN_INCREMENT)
            elif self.rotation_remaining < -ROBOT_TURN_INCREMENT:
                self.rotation_remaining += ROBOT_TURN_INCREMENT
                self.__rotate(-ROBOT_TURN_INCREMENT)
            else:
                self.__rotate(self.rotation_remaining)
                self.rotation_remaining = 0


    def update_movement(self):
        if self.movement_remaining != 0:
            if self.movement_remaining > ROBOT_MOVE_INCREMENT:
                self.movement_remaining -= ROBOT_MOVE_INCREMENT
                self.__move(ROBOT_MOVE_INCREMENT)
            elif self.movement_remaining < -ROBOT_MOVE_INCREMENT:
                self.movement_remaining += ROBOT_MOVE_INCREMENT
                self.__move(-ROBOT_MOVE_INCREMENT)
            else:
                self.__move(self.movement_remaining)
                self.movement_remaining = 0

    def update(self):
        if not self.is_moving() and self.event_queue:
            event = self.event_queue.popleft()
            if event[0] == MOVE:
                self.movement_remaining = event[1]
            elif event[0] == ROTATE:
                self.rotation_remaining = event[1]
            elif event[0] == RESPOND:
                self.event_poller.respond()
        self.update_rotation()
        self.update_movement()

    def __rotate(self, angle):
        self.direction -= angle
        self.direction %= 360
        self.render_object.rotate_to(self.direction)

    def __move(self, distance):
        self.position += self.__get_direction_vector() * distance
        self.position.x = max(ROBOT_BODY_SIZE / 2, min(CANVAS_WIDTH - ROBOT_BODY_SIZE / 2, self.position.x))
        self.position.y = max(ROBOT_BODY_SIZE / 2, min(CANVAS_HEIGHT - ROBOT_BODY_SIZE / 2, self.position.y))
        self.render_object.move_to(self.position)

    def __get_direction_vector(self):
        return Vector(0, -1).rot(self.direction)

    def is_moving(self):
        if self.rotation_remaining == 0 and self.movement_remaining == 0:
            return False
        return True

    def rotate(self, angle):
        self.event_queue.append((ROTATE, angle))
        self.event_queue.append((RESPOND,))

    def move(self, distance):
        self.event_queue.append((MOVE, distance))
        self.event_queue.append((RESPOND,))

    def __get_angle_to(self, x, y):
        if (x, y) == self.get_location():
            return
        target_vector = Vector(x, y) - self.position
        target = target_vector / target_vector.magnitude()
        angle = degrees(acos(self.__get_direction_vector().dot(target)))
        if target.cross(self.__get_direction_vector()) < 0:
            angle *= -1
        return angle


    def move_to(self, x, y):
        angle = self.__get_angle_to(x, y)
        self.event_queue.append((ROTATE, angle))
        self.event_queue.append((MOVE, (Vector(x, y) - self.position).magnitude()))
        self.event_queue.append((RESPOND,))

    def turn_to(self, x, y):
        angle = self.__get_angle_to(x, y)
        self.event_queue.append((ROTATE, angle))
        self.event_queue.append((RESPOND,))

    def shoot(self):
        self.world.add_projectile(Projectile(self.canvas, self.position, self.__get_direction_vector()))
        self.event_poller.respond()

    def get_location(self):
        return round(self.position.x, 6), round(self.position.y, 6)

    def get_bearing(self):
        return round(self.direction, 6) % 360
