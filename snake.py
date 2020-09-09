import random
from point2D import Point2D

class Snake:

    def __init__(self, width, height):
        self.LENGTH_INCREMENT = 4
        self.RELATIVE_OFFSET = 1
        self.length = self.LENGTH_INCREMENT
        self.body = []
        self.body_IDs = []
        self.last_direction = 'Up'
        self.next_direction = None
        self.random_starting_locations(width, height)

    # Gives snake a valid random starting point always facing upwards
    def random_starting_locations(self, width, height):
        starting_x = random.randint(0, width)
        starting_y = random.randint(self.length, height-self.length)
        for i in range(self.length):
            self.body.append(Point2D(starting_x, starting_y + i))

    # Checks if snake's head shares a location with the food object
    def ate_food(self, food):
        if self.body[0].equals(food.location):
            self.length += self.LENGTH_INCREMENT
            return True
        return False

    # Method to change the direction that the snake will head
    def change_direction(self, e):
        blocked_direction = {
            'Up': 'Down',
            'Right': 'Left',
            'Down': 'Up',
            'Left': 'Right'
        }
        proposed_direction = e.keysym
        if proposed_direction in blocked_direction:
            if proposed_direction != blocked_direction[self.last_direction]:
                self.next_direction = e.keysym

    # Method to update the position of the snake based on it's next direction
    def move(self):
        if self.next_direction != None:
            direction_to_coords = {
            'Up': Point2D(self.body[0].x, self.body[0].y - 1),
            'Right': Point2D(self.body[0].x + 1, self.body[0].y),
            'Down': Point2D(self.body[0].x, self.body[0].y + 1),
            'Left': Point2D(self.body[0].x - 1, self.body[0].y)
            }
            if len(self.body) == self.length:
                self.body.pop()
            self.body.insert(0, direction_to_coords.get(self.next_direction))
            self.last_direction = self.next_direction

    # Method that checks if the snake has run into a wall
    def crashed_into_wall(self, width, height):
        x = self.body[0].x
        y = self.body[0].y
        if x < 0 or width < x or y < 0 or height < y:
            return True
        return False

    # Method that checks if snake has run into itself
    def crashed_into_self(self):
        for i in range(len(self.body)-1):
            for j in range(i+1, len(self.body)):
                if self.body[i].equals(self.body[j]):
                    return True
        return False

    # Method to translate the snakes game coordinates to canvas coordinates
    def body_segment_canvas_coords(self, index, px_offset, px_size):
        x = self.body[index].x * px_size+px_offset
        y = self.body[index].y * px_size+px_offset
        return (x+self.RELATIVE_OFFSET, y+self.RELATIVE_OFFSET,\
            x+px_size-self.RELATIVE_OFFSET, y+px_size-self.RELATIVE_OFFSET)

    def score(self):
        return str(self.length // self.LENGTH_INCREMENT - 1)

    # Method to draw the snake to the canvas
    def draw(self, canvas, px_offset, px_size):
        # Loops through snake body points
        for i in range(len(self.body)):
            coords = self.body_segment_canvas_coords(i, px_offset, px_size)
            if i > len(self.body_IDs)-1:
                self.body_IDs.append(canvas.create_oval(coords, fill='white'))
            else:
                canvas.coords(self.body_IDs[i],coords)

    def __str__(self):
        return 'Snake: x=' + str(self.body[0].x) + ', y=' + str(self.body[0].y)
