class Robot:
    COMMANDS = {
        'left': {0: (0, -1), 90: (-1, 0), 180: (0, 1), 270: (1, 0)},
        'l': {0: (0, -1), 90: (-1, 0), 180: (0, 1), 270: (1, 0)},

        'right': {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)},
        'r': {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)},

        'up': {0: (-1, 0), 90: (0, 1), 180: (1, 0), 270: (0, -1)},
        'u': {0: (-1, 0), 90: (0, 1), 180: (1, 0), 270: (0, -1)},

        'down': {0: (1, 0), 90: (0, -1), 180: (-1, 0), 270: (0, 1)},
        'd': {0: (1, 0), 90: (0, -1), 180: (-1, 0), 270: (0, 1)},

        'turn 90': 90,
        't 90': 90,

        'turn 180': 180,
        't 180': 180
    }

    def __init__(self, map):
        self.map = map
        self.cur_pos = self.map.player
        self.direction = 0
        self.route = [self.cur_pos + (self.direction,)]

    def run(self):
        """Interactive session with a robot"""
        print("Robot is represented by '^' symbol on the map:")
        # draw the whole map before the game
        self.map.render(self.cur_pos, self.direction, whole_map=True)

        print("Hello! I'm a robot and I know several commands: left, right, up, down, turn 90, turn 180.\n"
              "The short form (l, r, t 90, etc.) is also valid. To quit type 'quit' or 'q'.\n"
              "Type in any command: ")

        while True:
            cmd = input().lower()

            if cmd in self.COMMANDS:
                self._execute_cmd(cmd)
                self.map.render(self.cur_pos, self.direction)
                self.route.append(self.cur_pos + (self.direction,))

            elif cmd in ['quit', 'q']:
                print('Bye!')
                return self.route

            else:
                print("I don't know this command. Try another one.")

    def _execute_cmd(self, cmd):
        if cmd in ['turn 90', 'turn 180', 't 90', 't 180']:
            self._rotate(cmd)
        else:
            self._move(cmd)

    def _rotate(self, cmd):
        direc = self.direction
        self.direction += self.COMMANDS[cmd]
        if self.direction == 360:
            self.direction = 0

        print(f'Rotation: {direc} --> {self.direction}')

    def _move(self, cmd):
        (x, y) = self.cur_pos

        delta_x, delta_y = self.COMMANDS[cmd][self.direction]
        new_x, new_y = x + delta_x, y + delta_y

        # check obstacle in (new_x, new_y)
        if 0 <= new_x < self.map.size_x and 0 <= new_y < self.map.size_y and not self.map.map[new_x][new_y]:
            self.cur_pos = (new_x, new_y)

        print(f'Step: ({x},{y}) --> ({self.cur_pos[0]},{self.cur_pos[1]})')
