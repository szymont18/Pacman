import pygame


class TextureFactory:
    def __init__(self,FIELD_SIZE):
        self.images = dict()
        self.FIELD_SIZE = FIELD_SIZE

    def load(self, path: str,size_x,size_y):
        if path == None:
            raise Exception(path + " is not a valid path for TextureFactory/load")

        image = None
        if (path in self.images.keys()):
            image = self.images.get(path)
            return image
        else:
            image = pygame.transform.scale(pygame.image.load(path), (size_x, size_y))
            self.images[path] = image
            return image
