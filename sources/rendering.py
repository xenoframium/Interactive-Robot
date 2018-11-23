from vector import Vector

ROBOT_BODY_SIZE = 20
ROBOT_POINTER_LENGTH = 12
ROBOT_POINTER_INITIAL_BEARING = 0


class Renderable:
    def __init__(self, canvas, location, id):
        self.canvas = canvas
        self.first_vertex_location = location
        self.id = id

    def move_to(self, destination):
        movement_vector = destination - self.first_vertex_location
        self.canvas.move(self.id, movement_vector.x, movement_vector.y)
        new_location = self.canvas.coords(self.id)
        self.first_vertex_location = Vector(new_location[0], new_location[1])

    def show(self):
        self.canvas.itemconfigure(self.id, state='normal')

    def hide(self):
        self.canvas.itemconfigure(self.id, state='hidden')

    def coords(self, coords):
        return self.canvas.coords(self.id, coords)

    def destroy(self):
        self.canvas.delete(self.id)


class CircleRenderable(Renderable):
    def __init__(self, canvas, location, size, fill="white", outline="black"):
        half_size_vector = Vector(size / 2, size / 2)
        top_left = location - half_size_vector
        bottom_right = location + half_size_vector
        self.size = size
        self.first_vertex_location = top_left
        self.canvas = canvas
        self.id = canvas.create_oval(top_left.x, top_left.y, bottom_right.x, bottom_right.y, fill=fill, outline=outline)

    def move_to(self, destination):
        super(CircleRenderable, self).move_to(Vector(destination.x - self.size / 2, destination.y - self.size / 2))


class PointerRenderable(Renderable):
    def __init__(self, canvas, location, length, bearing):
        self.length = length
        self.first_vertex_location = location
        self.canvas = canvas
        pointer_tip = self.first_vertex_location + Vector(0, -1).rot(bearing) * self.length
        self.id = canvas.create_line(location.x, location.y, pointer_tip.x, pointer_tip.y)

    def rotate_to(self, bearing):
        pointer_tip = self.first_vertex_location + Vector(0, -1).rot(bearing) * self.length
        start_location = self.first_vertex_location
        super(PointerRenderable, self).coords((start_location.x, start_location.y, pointer_tip.x, pointer_tip.y))


class RobotRenderComponent:
    def __init__(self, canvas, location):
        self.body = CircleRenderable(canvas, location, ROBOT_BODY_SIZE, fill="green")
        self.pointer = PointerRenderable(canvas, location, ROBOT_POINTER_LENGTH, ROBOT_POINTER_INITIAL_BEARING)

    def move_to(self, location):
        self.body.move_to(location)
        self.pointer.move_to(location)

    def rotate_to(self, bearing):
        self.pointer.rotate_to(bearing)

    def show(self):
        self.body.show()
        self.pointer.show()

    def hide(self):
        self.body.hide()
        self.pointer.hide()
