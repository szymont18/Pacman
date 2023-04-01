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
        else:
            image = pygame.image.load(path)
            self.images[path] = image

        image_adjusted = pygame.transform.scale(image,(540,540))
        return image_adjusted


