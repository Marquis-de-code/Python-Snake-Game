class Point2D:

    def __init__(self, x =0, y=0):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    # Checks if a point shares a location with another point
    def equals(self, point):
        if self.x == point.x and self.y == point.y:
            return True
        return False

