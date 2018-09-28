import random
from termcolor import colored


class Map:
    CHARS = {
        "*": ("red", []),
        ".": ("white", []),
        "^": ("green", ['dark']),
        "v": ("green", ["dark"]),
        ">": ("green", ["dark"]),
        "<": ("green", ["dark"]),
        "|": ("blue", []),
        "-": ("blue", [])
    }

    def __init__(self, x, y, obstacles=0, offset=2):
        self.size_x = x
        self.size_y = y
        self.offset = offset
        # init map with zeroes
        self.map = [[0] * y for _ in range(x)]
        # set obstacles (1) on the map
        self._generate_obstacles(obstacles)
        # set player's initial position
        self.player = self._set_init_pos()

    def _generate_obstacles(self, N):
        """Generates N random sized obstacles in random locations"""
        i = 0
        while i < N:
            x_obst = random.randint(0, self.size_x-1)
            y_obst = random.randint(0, self.size_y-1)

            delta = min(self.size_x - x_obst, self.size_y - y_obst, self.size_x // 2) - 1
            delta_size = random.randint(0, delta)
            part_of_map = [self.map[i][y_obst:(y_obst + delta_size + 1)] for i in range(x_obst, x_obst + delta_size + 1)]

            if all(cell == 0 for row in part_of_map for cell in row):
                for x in range(x_obst, x_obst + delta_size + 1):
                    for y in range(y_obst, y_obst + delta_size + 1):
                        # if not self.map[x][y]:
                        self.map[x][y] = 1
                i += 1

    def _set_init_pos(self):
        """Sets initial position of the robot (in the center of the map but away from obstacles)"""
        x = self.size_x // 2
        y = self.size_y // 2

        while self.map[x][y]:
            i = 1
            coords = [(x-i, y), (x+i, y), (x, y-i), (x, y+i), (x-i, y-i), (x+i, y-i), (x-i, y+i), (x+i, y+i)]
            for xx, yy in coords:
                if not self.map[xx][yy]:
                    return xx, yy
            i += 1
        return x, y

    def render(self, robot_pos, robot_dir, whole_map=False):
        """Renders the whole map in the beginning of session and part of the map after each command to the robot"""
        # clear previous player's position
        self.map[self.player[0]][self.player[1]] = 0
        # save new one
        self.player = robot_pos
        # determine robot's symbol
        robot = '^'
        if robot_dir == 90:
            robot = '>'
        elif robot_dir == 180:
            robot = 'v'
        elif robot_dir == 270:
            robot = '<'
        # set robot on map
        self.map[self.player[0]][self.player[1]] = robot

        self._draw_map(whole_map)

    def _draw_map(self, whole=False):
        s = ''
        x, y = self.player

        x_coord = range(-1, self.size_x + 1) if whole else range(x - self.offset, x + self.offset + 1)
        y_coord = range(-1, self.size_y + 1) if whole else range(y - self.offset, y + self.offset + 1)

        for i in x_coord:
            for j in y_coord:
                # draw no playground
                if self.size_x < i or i < -1 or self.size_y < j or j < -1:
                    char = self._make_colored(' ')
                # draw horizontal border
                elif i == -1 or i == self.size_x:
                    if j == -1 or j == self.size_y:
                        char = self._make_colored(' ')
                    else:
                        char = self._make_colored('-')
                # draw vertical border
                elif j == -1 or j == self.size_y:
                    char = self._make_colored('|')
                # draw empty cells
                elif self.map[i][j] == 0:
                    char = self._make_colored('.')
                # draw obstacles
                elif self.map[i][j] == 1:
                    char = self._make_colored('*')
                # draw robot's position
                else:
                    char = self._make_colored(self.map[i][j])
                s += char + self._make_colored(' ')
            s += '\n'

        print(s)

    def _make_colored(self, ch):
        """Makes the map colored"""
        default = ("white", [])
        color, attrs = self.CHARS.get(ch, default)
        return colored(ch, color, attrs=attrs)
