import sys
import json
from map import Map
from robot import Robot


def save_session(map, route):
    """Saves robot's route and the map to json file"""
    with open('robot_session.json', 'w') as fout:
        json.dump({'route': route, 'map': map}, fout)
        print("Your session was saved to the file 'robot_session.json'.")


def app(x=5, y=5, n=4, offset=2):
    """Entry point to the app"""
    map = Map(x, y, n, offset)
    robot = Robot(map)
    route = robot.run()

    save_session(map.map, route)


if __name__ == '__main__':
    try:
        [x, y, n] = [int(a) for a in sys.argv[1:4]]
        offset = int(sys.argv[4]) if len(sys.argv) > 4 else 2

        if x < 1 or y < 1 or n < 0 or offset < 0 or (x * y) <= n:
            raise BaseException
        else:
            app(x, y, n, offset)

    except BaseException:
        print("Correct arguments: size of map by X, size of map by Y, number of obstacles, offset (optional). "
              "Number of obstacles must be less than X*Y. All the numbers must be positive.")
