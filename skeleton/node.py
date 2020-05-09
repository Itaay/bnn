class Node:
    def __init__(self, offset, space, parent=None):
        self.offset = offset
        self.direction = space.start_direction()
        self.parent = parent
        self.space = space

    def location(self):
        if self.parent is not None:
            origin = self.parent.location()

            relative_offset = self.space.rotate(self.parent.direction, self.offset)

            position = origin + relative_offset#   self.space.rotate(self.direction, relative_offset)
            return position
        return self.offset

    def move(self, offset):
        self.offset += offset
