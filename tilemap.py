from settings import *
from sprites import Item, Obstacle, Decoration, Exit, River, Danger, Enemy, Hazard, Slide

img_list = []


class World:

    def __init__(self, game):

        self.game = game

        self.obstacle_list = []

    def process_data(self, data):

        self.length = len(data[0]) * TILESIZE

        for y, row in enumerate(data):

            for x, tile in enumerate(row):

                if tile >= 0:

                    if tile in TILES["obstacle"]:
                        obstacle = Obstacle(tile, x * TILESIZE, y * TILESIZE)
                        self.obstacle_list.append(obstacle)

                    elif tile in TILES["slides"]:
                        slide = Slide(self.game, tile, x * TILESIZE, y * TILESIZE)
                        self.game.slide_group.add(slide)

                    elif tile in TILES["coin"]:
                        item = Item(self.game, 'Coin', x * TILESIZE, y * TILESIZE)
                        self.game.item_group.add(item)

                    elif tile in TILES["gem"]:
                        item = Item(self.game, 'Gem', x * TILESIZE, y * TILESIZE)
                        self.game.item_group.add(item)

                    elif tile in TILES["key"]:
                        item = Item(self.game, 'Key', x * TILESIZE, y * TILESIZE)
                        self.game.item_group.add(item)

                    elif tile in TILES["decoration"]:
                        decoration = Decoration(self.game, tile, x * TILESIZE, y * TILESIZE)
                        self.game.decoration_group.add(decoration)

                    elif tile in TILES["river"]:
                        water = River(self.game, tile, x * TILESIZE, y * TILESIZE)
                        self.game.river_group.add(water)

                    elif tile in TILES["exit"]:
                        exit = Exit(self.game, tile, x * TILESIZE, y * TILESIZE)
                        self.game.exit_group.add(exit)

                    elif tile in TILES["hazard"]:
                        hazard = Hazard(self.game, tile, x * TILESIZE, y * TILESIZE)
                        self.game.danger_group.add(hazard)

                    elif tile in TILES["wheel"]:
                        danger = Danger(self.game, "wheel", 0, x * TILESIZE, y * TILESIZE)
                        self.game.danger_group.add(danger)

                    elif tile in TILES["blade-u"]:
                        danger = Danger(self.game, "blade", 0, x * TILESIZE, y * TILESIZE)
                        self.game.danger_group.add(danger)

                    elif tile in TILES["blade-l"]:
                        danger = Danger(self.game, "blade", 90, x * TILESIZE, y * TILESIZE)
                        self.game.danger_group.add(danger)

                    elif tile in TILES["blade-r"]:
                        danger = Danger(self.game, "blade", 270, x * TILESIZE, y * TILESIZE)
                        self.game.danger_group.add(danger)

                    elif tile in TILES["enemies"]:
                        for enemy in ENEMIES:
                            if tile in ENEMIES[enemy]["tile"]:
                                enemy = Enemy(self.game, enemy, x * TILESIZE, y * TILESIZE)
                                self.game.enemy_group.add(enemy)

    def draw(self):

        for tile in self.obstacle_list:
            tile.rect[0] += self.game.screen_scroll

            self.game.screen.blit(tile.image, tile.rect)
