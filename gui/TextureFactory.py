import pygame

class TextureFactory:
    def __init__(self):
        self.images = dict()

    def load(self, path: str):
        if path == None:
            raise Exception(path + " is not a valid path for TextureFactory/load")

        image = None
        if(path in self.images.keys()):
            image = self.images.get(path)
            return image
        else:
            image = pygame.transform.scale(pygame.image.load(path), (42, 42))
            self.images[path] = image
            return image


