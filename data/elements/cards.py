# Pygame Packages
import pygame

# General Packages
import os

# Import Settings
import settings


class TextCard(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, text, padding=25):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width, self.height = self.get_card_size()
        self.text = text
        self.padding = padding
        self.font_size = self.set_font_size()
        self.font = pygame.font.Font(
            os.path.join("data", "fonts", "Poppins-Regular.ttf"), self.font_size
        )
        self.update()

    def update(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(settings.BLACK))
        border_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(
            self.image,
            pygame.Color(settings.BLACK),
            border_rect,
            width=0,
            border_radius=15,
        )

        inner_rect = border_rect.inflate(-6, -6)
        pygame.draw.rect(
            self.image, pygame.Color(settings.GREY), inner_rect, border_radius=12
        )
        lines = self.wrap_text(self.text, self.width - 2 * self.padding)
        font_height = self.font.size("Tg")[1]
        y = self.padding
        for line in lines:
            text = self.font.render(line, True, pygame.Color(settings.WHITE))
            self.image.blit(text, (self.padding, y))
            y += font_height

        self.rect = self.image.get_rect()
        self.rect.x = (self.screen_width - self.width) // 2
        self.rect.y = (self.screen_height - self.height) // 2

    def wrap_text(self, text, width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            if self.font.size(current_line + word)[0] < width:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def set_font_size(self):
        font_size = self.screen_width // 45
        return font_size

    def get_card_size(self):
        card_padding_x = self.screen_width // 7
        card_padding_y = self.screen_height // 13

        width = self.screen_width - (card_padding_x * 2)
        height = self.screen_height - (card_padding_y * 2)

        return width, height


class ImageTextCard(pygame.sprite.Sprite):
    def __init__(
        self, screen_width, screen_height, image_path, text, position, padding=25
    ):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width, self.height = self.get_card_size()
        self.text = text
        self.padding = padding
        self.pad_x = self.get_image_padx()
        self.position = position
        self.font_size = self.set_font_size()
        self.font = pygame.font.Font(
            os.path.join("data", "fonts", "Poppins-Regular.ttf"), self.font_size
        )
        self.image_path = image_path
        self.update()

    def update(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(settings.BLACK))
        border_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(
            self.image,
            pygame.Color(settings.BLACK),
            border_rect,
            width=0,
            border_radius=15,
        )

        inner_rect = border_rect.inflate(-6, -6)
        pygame.draw.rect(
            self.image, pygame.Color(settings.GREY), inner_rect, border_radius=12
        )

        # Load image and blit it onto the card surface
        image = pygame.image.load(self.image_path).convert_alpha()
        image_rect = image.get_rect(centerx=self.width / 2, top=self.padding)
        self.image.blit(image, image_rect)

        # Blit the text onto the card surface
        lines = self.wrap_text(self.text, self.width - 2 * self.padding)
        font_height = self.font.size("Tg")[1]
        y = image_rect.bottom + self.padding
        for line in lines:
            text = self.font.render(line, True, pygame.Color(settings.WHITE))
            self.image.blit(text, (self.padding, y))
            y += font_height

        self.rect = self.image.get_rect()

        if self.position == "left":
            self.rect.x = self.pad_x
        elif self.position == "center":
            self.rect.x = (self.screen_width - self.width) // 2
        elif self.position == "right":
            self.rect.x = self.screen_width - self.pad_x - self.width

        self.rect.y = (self.screen_height - self.height) // 2

    def wrap_text(self, text, width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            if self.font.size(current_line + word)[0] < width:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def get_image_padx(self):
        padx = self.screen_width // 35

        return padx

    def set_font_size(self):
        font_size = self.screen_width // 45
        return font_size

    def get_card_size(self):
        card_padding_x = self.screen_width // 35
        card_padding_y = self.screen_height // 35

        width = self.screen_width // 3.5
        height = self.screen_height // 1.2

        return width, height
