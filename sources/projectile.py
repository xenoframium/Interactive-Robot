from rendering import *
from GUI import *

PROJECTILE_MOVEMENT_INCREMENT = 5
PROJECTILE_SIZE = 5


class Projectile:
    def __init__(self, canvas, source, direction_vector):
        self.position = source
        self.direction_vector = direction_vector
        self.render_object = CircleRenderable(canvas, source, PROJECTILE_SIZE, fill="blue", outline="blue")
        self.is_alive = True

    def is_in_canvas(self):
        if self.position.x > CANVAS_WIDTH + PROJECTILE_SIZE:
            return False
        if self.position.y > CANVAS_HEIGHT + PROJECTILE_SIZE:
            return False
        if self.position.x + PROJECTILE_SIZE < 0:
            return False
        if self.position.y + PROJECTILE_SIZE < 0:
            return False
        return True

    def should_despawn(self):
        return not self.is_in_canvas()

    def destroy(self):
        self.render_object.destroy()
        self.is_alive = False

    def update(self):
        self.position += self.direction_vector * PROJECTILE_MOVEMENT_INCREMENT
        self.render_object.move_to(self.position)
