import pygame


class Button:

    def __init__(self, game, x, y, image, imagel, scale):

        self.game = game

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.imagel = pygame.transform.scale(imagel, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):

        action = False

        pos = pygame.mouse.get_pos()
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y

        if self.rect.collidepoint(*pos) and self.mask.get_at(pos_in_mask) and not self.game.choose_level:

            surface.blit(self.imagel, (self.rect.x, self.rect.y))

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
                self.game.click_sound.play()

        else:

            surface.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class Level:

    def __init__(self, game, level, x, y):

        self.game = game

        self.level = level

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/img/button/level.png').convert_alpha()
        self.imagel = pygame.image.load('assets/img/button/level_l.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.clicked = False

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):

        action = False

        pos = pygame.mouse.get_pos()
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y

        if self.rect.collidepoint(*pos) and self.mask.get_at(pos_in_mask):

            surface.blit(self.imagel, (self.rect.x, self.rect.y))

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:

                if self.level <= self.game.player_max_level:
                    action = True
                self.clicked = True
                self.game.click_sound.play()

        else:

            surface.blit(self.image, (self.rect.x, self.rect.y))

        if self.level <= self.game.player_max_level:
            level_text = self.game.label_font.render(f'{self.level}', True, "white")
        else:
            level_text = self.game.label_font.render('X', True, "white")
        surface.blit(level_text, (self.x - level_text.get_width() // 2, self.y - level_text.get_height() // 2))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action, self.level
