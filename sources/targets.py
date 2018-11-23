from rendering import *

TARGET_SIZE = 5


class ShootTarget:
    def __init__(self, canvas, location):
        self.render_object = CircleRenderable(canvas, location, TARGET_SIZE, fill="red")
        self.position = location

    def destroy(self):
        self.render_object.destroy()


class TreadTarget:
    def __init__(self, canvas, location):
        self.render_object = CircleRenderable(canvas, location, TARGET_SIZE, fill="yellow")
        self.position = location

    def destroy(self):
        self.render_object.destroy()