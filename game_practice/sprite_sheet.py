import pygame

class sprite_sheet:
    def __init__(self, _file_path, _name_hint=""):
        """
        Class that reads a 2d sprite sheet path.
        Can be used to read sprite sheet easily into pygame app.
        """
        self.sheet = pygame.image.load(_file_path, _name_hint).convert()

        # a bunch of directional names so user can save one time and use without reblitting
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.up_left = None
        self.down_left = None
        self.up_right = None
        self.down_right = None

    def image_at(self, rectangle):
        """
        Load specific image at pygame.Rect or int 4-tuple location in the sheet.
        """
        sprite_rect = pygame.Rect(rectangle)
        img = pygame.Surface(sprite_rect.size).convert()

        # draw the chosen sprite onto the img
        img.blit(self.sheet, (0,0), sprite_rect)

        return img