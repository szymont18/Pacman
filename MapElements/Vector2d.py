import pygame


class Vector2d:
    FIELD_SIZE = None

    def __init__(self, y, x):
        self.x = x
        self.y = y

    @staticmethod
    def set_field_size(new_field_size):
        Vector2d.FIELD_SIZE = new_field_size

    def convert_to_index(self):
        return self.y // Vector2d.FIELD_SIZE, self.x // Vector2d.FIELD_SIZE

    def get_coords(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
