import pygame


class CalibrationLoader:
    def __init__(self):
        pass

    def load_image(self, filename, width, height, position):
        image = pygame.image.load(filename)
        image_size = self.get_image_size(width, height)
        image = pygame.transform.scale(image, image_size)

        padding = self.get_image_padx(width)

        if position == "left":
            rect = image.get_rect(midleft=(padding, height / 2))
        elif position == "right":
            rect = image.get_rect(midright=(width - padding, height / 2))

        return image, rect

    def get_image_size(self, width, height):
        image_width = width // 4
        image_height = height // 2

        return image_width, image_height

    def get_image_padx(self, width):
        padx = width // 45

        return padx


class StimuliImage:
    def __init__(self):
        pass

    def load_image(self, filename, width, height, position):
        image = pygame.image.load(filename)
        image_size = self.get_image_size(width, height)
        image = pygame.transform.scale(image, image_size)

        padding = self.get_image_padx(width)

        if position == "left":
            rect = image.get_rect(midleft=(padding, height / 2))
        elif position == "right":
            rect = image.get_rect(midright=(width - padding, height / 2))

        return image, rect

    def get_image_size(self, width, height):
        image_width = width // 4
        image_height = height // 2

        return image_width, image_height

    def get_image_padx(self, width):
        padx = width // 50

        return padx


class FeedbackImage:
    def __init__(self):
        pass

    def load_image(self, filename, width, height, position):
        image = pygame.image.load(filename)
        image_size = self.get_image_size(width, height)
        image = pygame.transform.scale(image, image_size)

        padding = self.get_image_padx(width)

        if position == "left":
            rect = image.get_rect(midleft=(padding, height / 2))
        elif position == "right":
            rect = image.get_rect(midright=(width - padding, height / 2))

        return image, rect

    def get_image_size(self, width, height):
        image_width = width // 4
        image_height = height // 2

        return image_width, image_height

    def get_image_padx(self, width):
        padx = width // 50

        return padx
