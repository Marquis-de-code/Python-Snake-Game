# food.py is a module to store the food class. The food class is a 2D point that has the ability to check if its
# location is shared with a
from point2D import Point2D
from random import randint


class Food:

    def __init__(self, canvas, total_offset, px_size, width, height, snake):
        self.location = None
        self.RELATIVE_OFFSET = 4
        self.new_random_location(width, height, snake)
        self.id = self.init_id(canvas, total_offset, px_size)

    @staticmethod
    def location_is_empty(location, snake):
        for segment in snake.body:
            if location.equals(segment):
                return True
        return False

    def new_random_location(self, width, height, snake):
        location_is_not_valid = True
        proposed_location = None
        while location_is_not_valid:
            proposed_location = Point2D(randint(0, width), randint(0, height))
            location_is_not_valid = self.location_is_empty(proposed_location, snake)
        self.location = proposed_location

    def canvas_coords(self, total_offset, px_size):
        x = self.location.x*px_size + total_offset
        y = self.location.y*px_size + total_offset
        return (x+self.RELATIVE_OFFSET, y+self.RELATIVE_OFFSET,
                x+px_size-self.RELATIVE_OFFSET, y+px_size-self.RELATIVE_OFFSET)

    def init_id(self, canvas, total_offset, px_size):
        return canvas.create_oval(self.canvas_coords(total_offset, px_size),
                                  fill='green')

    def draw(self, canvas, total_offset, px_size):
        canvas.coords(self.id, self.canvas_coords(total_offset, px_size))
