import sys
import csv
import pygame
from pygame import mixer, font
from settings import *
from sprites import Character
from tilemap import World
from buttons import Button, Level


class Game:

    def __init__(self):

        pygame.init()
        mixer.init()
        font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)

        pygame.display.set_caption(TITLE)

        pygame.display.set_icon(pygame.image.load(f'assets/img/icon/{DEFAULT_COLOR}.png').convert_alpha())

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        self.clock = pygame.time.Clock()

        self.load()

    def load(self):

        self.player_color = DEFAULT_COLOR

        self.data()
        self.menu()
        self.audio()

        self.bg = pygame.transform.scale(pygame.image.load(f'assets/img/background/{self.player_max_level}.png').convert_alpha(),
                                         (COLS * TILESIZE, HEIGHT))

        self.label_font = pygame.font.Font('assets/font/FredokaOne.ttf', 24)

        self.screen_scroll = 0
        self.bg_scroll = 0
        self.start_game = False
        self.restart_game = False
        self.play_game = True
        self.game_music = True
        self.choose_level = False

        self.enemy_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.river_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.danger_group = pygame.sprite.Group()
        self.slide_group = pygame.sprite.Group()

        self.player = Character(self, self.player_color, TILESIZE * PLAYER_POSITION[0], TILESIZE * PLAYER_POSITION[1],
                                PLAYER_SPEED)

        world_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)

        with open(f'assets/map/map{self.player_max_level}_tiles.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        self.world = World(self)
        self.world.process_data(world_data)

    def menu(self):

        left_image = pygame.image.load('assets/img/button/left.png').convert_alpha()
        right_image = pygame.image.load('assets/img/button/right.png').convert_alpha()
        start_image = pygame.image.load('assets/img/button/start.png').convert_alpha()
        resume_image = pygame.image.load('assets/img/button/resume.png').convert_alpha()
        exit_image = pygame.image.load('assets/img/button/exit.png').convert_alpha()
        pause_image = pygame.image.load('assets/img/button/pause.png').convert_alpha()
        restart_image = pygame.image.load('assets/img/button/restart.png').convert_alpha()
        musicon_image = pygame.image.load('assets/img/button/musicon.png').convert_alpha()
        musicoff_image = pygame.image.load('assets/img/button/musicoff.png').convert_alpha()

        leftl_image = pygame.image.load('assets/img/button/left_l.png').convert_alpha()
        rightl_image = pygame.image.load('assets/img/button/right_l.png').convert_alpha()
        startl_image = pygame.image.load('assets/img/button/start_l.png').convert_alpha()
        resumel_image = pygame.image.load('assets/img/button/resume_l.png').convert_alpha()
        exitl_image = pygame.image.load('assets/img/button/exit_l.png').convert_alpha()
        pausel_image = pygame.image.load('assets/img/button/pause_l.png').convert_alpha()
        restartl_image = pygame.image.load('assets/img/button/restart_l.png').convert_alpha()
        musiconl_image = pygame.image.load('assets/img/button/musicon_l.png').convert_alpha()
        musicoffl_image = pygame.image.load('assets/img/button/musicoff_l.png').convert_alpha()
        levels_image = pygame.image.load('assets/img/button/levels.png').convert_alpha()
        levelsl_image = pygame.image.load('assets/img/button/levels_l.png').convert_alpha()

        self.left_button = Button(self, BUTTONS["left"]["position"][0], BUTTONS["left"]["position"][1],
                                  left_image, leftl_image, BUTTONS["left"]["scale"])
        self.right_button = Button(self, BUTTONS["right"]["position"][0], BUTTONS["right"]["position"][1],
                                   right_image, rightl_image, BUTTONS["right"]["scale"])
        self.start_button = Button(self, BUTTONS["start"]["position"][0], BUTTONS["start"]["position"][1], start_image,
                                   startl_image,
                                   BUTTONS["start"]["scale"])
        self.resume_button = Button(self, BUTTONS["resume"]["position"][0], BUTTONS["resume"]["position"][1],
                                    resume_image,
                                    resumel_image, BUTTONS["resume"]["scale"])
        self.exit_button = Button(self, BUTTONS["exit"]["position"][0], BUTTONS["exit"]["position"][1], exit_image,
                                  exitl_image,
                                  BUTTONS["exit"]["scale"])
        self.pause_button = Button(self, BUTTONS["pause"]["position"][0], BUTTONS["pause"]["position"][1], pause_image,
                                   pausel_image, BUTTONS["pause"]["scale"])
        self.restart_button = Button(self, BUTTONS["restart"]["position"][0], BUTTONS["restart"]["position"][1],
                                     restart_image, restartl_image, BUTTONS["restart"]["scale"])
        self.musicon_button = Button(self, BUTTONS["musicon"]["position"][0], BUTTONS["musicon"]["position"][1],
                                     musicon_image, musiconl_image, BUTTONS["musicon"]["scale"])
        self.musicoff_button = Button(self, BUTTONS["musicoff"]["position"][0], BUTTONS["musicoff"]["position"][1],
                                      musicoff_image, musicoffl_image, BUTTONS["musicoff"]["scale"])
        self.levels_button = Button(self, BUTTONS["levels"]["position"][0], BUTTONS["levels"]["position"][1],
                                    levels_image, levelsl_image, BUTTONS["levels"]["scale"])

        self.label_image = pygame.transform.scale(pygame.image.load('assets/img/button/empty.png').convert_alpha(),
                                                  (168, 42))

        self.level_buttons = []

        for i in range(TOTAL_LEVEL):
            self.level_buttons.append(Level(self, i + 1, LEVELS[i + 1][0], LEVELS[i + 1][1]))

        self.dashboard_image = pygame.image.load('assets/img/button/dashboard.png').convert_alpha()
        self.dashboard = {
            "image": self.dashboard_image,
            "position": (WIDTH // 2 - self.dashboard_image.get_width() / 2 + 2,
                         HEIGHT // 2 - self.dashboard_image.get_height() / 2 + 2)
        }

        self.panel_image = pygame.image.load('assets/img/button/panel.png').convert_alpha()
        self.panel = {
            "image": self.panel_image,
            "position": (WIDTH // 2 - self.panel_image.get_width() / 2 + 4,
                         HEIGHT // 2 - self.panel_image.get_height() / 2 + 2)
        }

        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.icons = {
            "pink": pygame.transform.scale(pygame.image.load(f'assets/img/icon/game/pink.png').convert_alpha(),
                                           (ICON["scale"], ICON["scale"])),
            "beige": pygame.transform.scale(pygame.image.load(f'assets/img/icon/game/beige.png').convert_alpha(),
                                            (ICON["scale"], ICON["scale"])),
            "blue": pygame.transform.scale(pygame.image.load(f'assets/img/icon/game/blue.png').convert_alpha(),
                                           (ICON["scale"], ICON["scale"])),
            "yellow": pygame.transform.scale(pygame.image.load(f'assets/img/icon/game/yellow.png').convert_alpha(),
                                             (ICON["scale"], ICON["scale"])),
            "green": pygame.transform.scale(pygame.image.load(f'assets/img/icon/game/green.png').convert_alpha(),
                                            (ICON["scale"], ICON["scale"]))
        }

        self.icon = self.icons[self.player_color]

    def audio(self):

        mixer.music.load('assets/audio/music.wav')
        mixer.music.set_volume(SOUNDS["music"])
        mixer.music.play(-1, 0.0, 5000)

        self.click_sound = pygame.mixer.Sound('assets/audio/click.wav')
        self.click_sound.set_volume(SOUNDS["click"])

        self.jump_sound = pygame.mixer.Sound('assets/audio/jump.wav')
        self.jump_sound.set_volume(SOUNDS["jump"])

        self.coin_sound = pygame.mixer.Sound('assets/audio/coin.wav')
        self.coin_sound.set_volume(SOUNDS["coin"])

        self.key_sound = pygame.mixer.Sound('assets/audio/key.wav')
        self.key_sound.set_volume(SOUNDS["key"])

        self.hurt_sound = pygame.mixer.Sound('assets/audio/death.wav')
        self.hurt_sound.set_volume(SOUNDS["hurt"])

        self.river_sound = pygame.mixer.Sound('assets/audio/river.wav')
        self.river_sound.set_volume(SOUNDS["river"])

        self.win_sound = pygame.mixer.Sound('assets/audio/win.wav')
        self.win_sound.set_volume(SOUNDS["win"])

    def data(self):

        try:

            with open(FILES["level"], "r") as file:

                self.level = int(file.readline().strip())

        except FileNotFoundError:

            with open(FILES["level"], "w") as f:

                f.write("1")

                self.level = 1

        try:

            with open(FILES["best"], "r") as file:

                self.player_max_level = int(file.readline().strip())

        except FileNotFoundError:

            with open(FILES["best"], "w") as f:

                f.write(f"{self.level}")

                self.player_max_level = self.level

    def run(self):

        self.playing = True

        while self.playing:

            self.clock.tick(FPS)

            if self.start_game:
                self.update()

                self.display()

            self.events()

    def update(self):

        self.player.animate()

        if self.player.alive:

            if self.player.level_complete:
                self.complete()

        else:

            self.death()

        self.player.update()

    def complete(self):

        with open(FILES["money"], "w") as file:

            file.write(f"{self.player.money}")

        self.level += 1

        if self.level <= TOTAL_LEVEL:
            with open(FILES["level"], "w") as file:
                file.write(f"{self.level}")

        if TOTAL_LEVEL >= self.level > self.player_max_level:
            with open(FILES["best"], "w") as file:
                file.write(f"{self.level}")
            self.player_max_level = self.level

        self.bg_scroll = 0

        if self.level <= TOTAL_LEVEL:
            self.bg = pygame.transform.scale(
                pygame.image.load(f'assets/img/background/{self.level}.png').convert_alpha(),
                (COLS * TILESIZE, HEIGHT))

        self.restart()

    def death(self):

        self.screen_scroll = 0

        if self.restart_game:
            self.restart_game = False
            self.bg_scroll = 0

            self.restart()

    def map(self):

        if BACKGROUND[self.level]:
            self.screen.blit(self.bg, ((0 * self.bg.get_width()) - self.bg_scroll, 0))
        else:
            self.screen.blit(self.bg, (0, 0))

        self.world.draw()

    def display(self):

        self.map()

        self.decoration_group.update()
        self.decoration_group.draw(self.screen)

        self.slide_group.update(self.player)

        self.item_group.update(self.player)
        self.item_group.draw(self.screen)

        self.exit_group.update(self.player)
        self.exit_group.draw(self.screen)

        self.danger_group.update(self.player)
        self.danger_group.draw(self.screen)

        self.enemy_group.update(self.player)

        self.player.draw()

        self.river_group.update(self.player)
        self.river_group.draw(self.screen)

        if self.pause_button.draw(self.screen):
            self.start_game = False
            self.play_game = False
        if self.restart_button.draw(self.screen):
            self.restart()
            self.start_game = False

        if self.game_music and self.musicoff_button.draw(self.screen):
            self.mute()

        if not self.game_music and self.musicon_button.draw(self.screen):
            self.unmute()

        if self.player.money > 9999:
            self.player.money = 9999

        self.screen.blit(self.label_image, (TILESIZE // 2, TILESIZE // 2))
        coin_text = self.label_font.render(f'COIN: {self.player.money}', True, "white")
        self.screen.blit(coin_text, [TILESIZE // 2 + 23, TILESIZE // 2 + 6.5])

        if self.levels_button.draw(self.screen) and not self.choose_level:

            self.choose_level = True

        if self.choose_level:

            self.screen.blit(self.dim_screen, (0, 0))

            self.screen.blit(self.panel["image"], self.panel["position"])

            level_text = self.label_font.render('GAME LEVELS', True, "white")
            self.screen.blit(level_text, [WIDTH // 2 - TILESIZE * 2, HEIGHT // 4 - 7])

            for button in self.level_buttons:
                action, level = button.draw(self.screen)
                if action:
                    self.level = level
                    self.choose_level = False
                    self.bg_scroll = 0
                    self.bg = pygame.transform.scale(
                            pygame.image.load(f'assets/img/background/{self.level}.png').convert_alpha(),
                            (COLS * TILESIZE, HEIGHT))
                    self.restart()

        pygame.display.flip()

    def mute(self):

        mixer.music.pause()
        self.click_sound.set_volume(0)
        self.jump_sound.set_volume(0)
        self.coin_sound.set_volume(0)
        self.key_sound.set_volume(0)
        self.hurt_sound.set_volume(0)
        self.river_sound.set_volume(0)
        self.win_sound.set_volume(0)
        self.game_music = False

    def unmute(self):

        mixer.music.unpause()
        self.click_sound.set_volume(SOUNDS["click"])
        self.jump_sound.set_volume(SOUNDS["jump"])
        self.coin_sound.set_volume(SOUNDS["coin"])
        self.key_sound.set_volume(SOUNDS["key"])
        self.hurt_sound.set_volume(SOUNDS["hurt"])
        self.river_sound.set_volume(SOUNDS["river"])
        self.win_sound.set_volume(SOUNDS["win"])
        self.game_music = True

    def events(self):

        self.start()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT:
                    self.player.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = True
                if event.key == pygame.K_UP and self.player.alive:
                    self.player.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = False

    def start(self):

        if not self.start_game:

            bg = self.screen.fill(MENU_COLOR[self.player_color])

            dashboard = self.screen.blit(self.dashboard["image"], self.dashboard["position"])

            if self.play_game:

                if self.start_button.draw(self.screen):
                    self.start_game = True

                if self.left_button.draw(self.screen):

                    if self.player_color == COLORS[0]:
                        self.player_color = COLORS[-2]
                    else:
                        self.player_color = COLORS[COLORS.index(self.player_color) - 1]

                    self.icon = self.icons[self.player_color]

                    self.bg_scroll = 0
                    self.restart()

                if self.right_button.draw(self.screen):

                    self.player_color = COLORS[COLORS.index(self.player_color) + 1]

                    self.icon = self.icons[self.player_color]

                    self.bg_scroll = 0
                    self.restart()

            else:

                if self.resume_button.draw(self.screen):
                    self.start_game = True
                    self.play_game = True

            if self.exit_button.draw(self.screen):
                self.quit()

            self.screen.blit(self.icon, ICON["position"])

            pygame.display.update(
                [bg, dashboard, self.left_button, self.right_button, self.start_button, self.resume_button,
                 self.exit_button])

    def restart(self):

        world_data = self.reset()

        if self.level <= TOTAL_LEVEL:
            with open(f'assets/map/map{self.level}_tiles.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)

            self.world = World(self)
            self.world.process_data(world_data)

            self.player = Character(self, self.player_color, TILESIZE * PLAYER_POSITION[0],
                                    TILESIZE * PLAYER_POSITION[1], PLAYER_SPEED)

        else:

            self.quit()

    def reset(self):

        self.enemy_group.empty()
        self.item_group.empty()
        self.decoration_group.empty()
        self.river_group.empty()
        self.exit_group.empty()
        self.danger_group.empty()
        self.slide_group.empty()

        world_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)

        return world_data

    def quit(self):

        pygame.quit()

        sys.exit()


game = Game()

game.start()

while True:

    game.run()
