WIDTH = 1260
HEIGHT = 630
FPS = 60
TITLE = " Platformer Game"
FILES = {
    "money": "data/money.txt",
    "level": "data/level.txt",
    "best": "data/best.txt"
}

SCROLL = WIDTH / 4
BG_IMG = 'assets/img/background.png'
TILESIZE = 42
ROWS = int(HEIGHT / TILESIZE)
COLS = int(WIDTH / (TILESIZE / 2))

TOTAL_LEVEL = 10

LEVELS = {
    1: (WIDTH // 2 - 63 * 2 - 4, HEIGHT // 2 - TILESIZE),
    2: (WIDTH // 2 - 63 - 4, HEIGHT // 2 - TILESIZE),
    3: (WIDTH // 2 - 4, HEIGHT // 2 - TILESIZE),
    4: (WIDTH // 2 + 63 - 4, HEIGHT // 2 - TILESIZE),
    5: (WIDTH // 2 + 63 * 2 - 4, HEIGHT // 2 - TILESIZE),
    6: (WIDTH // 2 - 63 * 2 - 4, HEIGHT // 2 + TILESIZE // 2),
    7: (WIDTH // 2 - 63 - 4, HEIGHT // 2 + TILESIZE // 2),
    8: (WIDTH // 2 - 4, HEIGHT // 2 + TILESIZE // 2),
    9: (WIDTH // 2 + 63 - 4, HEIGHT // 2 + TILESIZE // 2),
    10: (WIDTH // 2 + 63 * 2 - 4, HEIGHT // 2 + TILESIZE // 2)
}

BACKGROUND = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: True,
    7: True,
    8: False,
    9: False,
    10: False
}

GRAVITY = 0.8
ANIMATION_COOLDOWN = 200
PLAYER_SPEED = 3
PLAYER_HEALTH = 300
PLAYER_POSITION = [6, 8]

DEFAULT_COLOR = "pink"
COLORS = ["pink", "beige", "yellow", "green", "blue", "pink"]

MENU_COLOR = {
    "pink": "pink",
    "beige": "blanched almond",
    "blue": "light blue",
    "yellow": (255, 255, 153),
    "green": "light green"
}

SOUNDS = {
    "music": 0.1,
    "jump": 0.15,
    "coin": 0.03,
    "key": 0.03,
    "hurt": 0.1,
    "river": 0.1,
    "win": 0.2,
    "click": 0.2
}

ICON = {
    "position": (WIDTH // 2 - TILESIZE * 2 - 4, HEIGHT // 2 - TILESIZE * 4.4 - 10),
    "scale": TILESIZE * 4
}

BUTTONS = {
    "left": {
        "position": [WIDTH // 2 - TILESIZE // 2 - 4 - 117, HEIGHT // 2 - TILESIZE * 3.02 - 10],
        "scale": 1
    },
    "right": {
        "position": [WIDTH // 2 - TILESIZE // 2 - 4 + 124, HEIGHT // 2 - TILESIZE * 3.02 - 10],
        "scale": 1
    },
    "start": {
        "position": [WIDTH // 2 - 143 - 4, HEIGHT // 2 + TILESIZE * 0.1],
        "scale": 1
    },
    "resume": {
        "position": [WIDTH // 2 - 143 - 4, HEIGHT // 2 + TILESIZE * 0.1],
        "scale": 1
    },
    "exit": {
        "position": [WIDTH // 2 - 143 - 4, HEIGHT // 2 + TILESIZE * 2 + 10],
        "scale": 1
    },
    "pause": {
        "position": [WIDTH - (TILESIZE * 5.25), TILESIZE // 2],
        "scale": 1
    },
    "restart": {
        "position": [WIDTH - (TILESIZE * 4), TILESIZE // 2],
        "scale": 1
    },
    "musicon": {
        "position": [WIDTH - (TILESIZE * 2.75), TILESIZE // 2],
        "scale": 1
    },
    "musicoff": {
        "position": [WIDTH - (TILESIZE * 2.75), TILESIZE // 2],
        "scale": 1
    },
    "levels": {
        "position": [WIDTH - (TILESIZE * 1.5), TILESIZE // 2],
        "scale": 1
    }
}

ENEMIES = {
    "pink-slug": {"tile": [230], "range": 3, "speed": 1},
    "blue-slug": {"tile": [290], "range": 3, "speed": 1},
    "fly": {"tile": [320], "range": 25, "speed": 3},
    "pink-worm": {"tile": [324], "range": 2, "speed": 1},
    "bee": {"tile": [354], "range": 4, "speed": 1},
    "mouse": {"tile": [384], "range": 5, "speed": 1},
    "eagle": {"tile": [441], "range": 16, "speed": 2},
    "ghost": {"tile": [445], "range": 7, "speed": 2},
    "spider": {"tile": [470], "range": 2, "speed": 1}
}

SUSPENDED = ["pink-slug", "blue-slug", "pink-worm"]

SLIDES = {
    735: {"range": 3, "speed": 1},
    736: {"range": 3, "speed": 1},
    737: {"range": 3, "speed": 1}
}

TILES = {
    "enemies": [230, 290, 320, 324, 354, 384, 441, 445, 470],
    "slides": [735, 736, 737],
    "flip": [17, 18, 46, 48],
    "obstacle": [1, 2, 3, 4, 32, 34, 38, 39, 121, 122, 123, 124, 152, 154, 158, 159, 191, 192, 301, 302, 303, 304, 332, 481,
                 482, 483, 484, 490, 491, 495, 496, 497, 498, 512, 526, 734, 781, 811],
    "coin": [78],
    "gem": [285],
    "key": [14],
    'exit': [253],
    "river": [11, 13, 40, 42, 548, 550, 578, 580],
    "hazard": [70, 570, 571, 572, 573, 574, 575, 603, 776, 864, 894],
    "wheel": [234],
    "blade-u": [358],
    "blade-l": [748],
    "blade-r": [359, 749],
    "health": [373, 375],
    "decoration": [16, 17, 18, 46, 48, 73, 255, 455, 456, 457, 458, 459, 460, 507, 520, 521, 522, 523, 551, 552, 553, 581, 582,
                   583, 600, 601, 602, 604, 605, 618, 619, 621, 622, 626, 627, 655, 675, 690, 691, 692, 703, 720, 721,
                   722, 733, 750, 751, 752, 761, 780, 782, 807, 810, 812]
}

ITEMS = {
    'Coin': 'assets/img/items/coin.png',
    'Gem': 'assets/img/items/gem.png',
    'Key': 'assets/img/items/key.png'
}
