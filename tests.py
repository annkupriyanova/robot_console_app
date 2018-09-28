import io
import sys
import unittest
import unittest.mock
from robot import Robot
from map import Map


class RobotTest(unittest.TestCase):
    def setUp(self):
        self.map = Map(10, 10, 0)
        self.robot = Robot(self.map)

    def test_rotate(self):
        self.robot._rotate('turn 90')
        self.assertEqual(90, self.robot.direction)

        self.robot._rotate('t 90')
        self.assertEqual(180, self.robot.direction)

        self.robot._rotate('t 180')
        self.assertEqual(0, self.robot.direction)

    def test_move_in_vertical_dir(self):
        prev_pos = self.robot.cur_pos
        self.robot._move('up')
        self.assertEqual((1, 0), self._delta_pos(prev_pos, self.robot.cur_pos))

        prev_pos = self.robot.cur_pos
        self.robot._move('left')
        self.assertEqual((0, 1), self._delta_pos(prev_pos, self.robot.cur_pos))

        prev_pos = self.robot.cur_pos
        self.robot._move('down')
        self.assertEqual((-1, 0), self._delta_pos(prev_pos, self.robot.cur_pos))

        prev_pos = self.robot.cur_pos
        self.robot._move('right')
        self.assertEqual((0, -1), self._delta_pos(prev_pos, self.robot.cur_pos))

    def test_move_in_horizontal_dir(self):
        self.robot._rotate('t 90')

        prev_pos = self.robot.cur_pos
        self.robot._move('up')
        self.assertEqual((0, -1), self._delta_pos(prev_pos, self.robot.cur_pos))

        prev_pos = self.robot.cur_pos
        self.robot._move('left')
        self.assertEqual((1, 0), self._delta_pos(prev_pos, self.robot.cur_pos))

        prev_pos = self.robot.cur_pos
        self.robot._move('down')
        self.assertEqual((0, 1), self._delta_pos(prev_pos, self.robot.cur_pos))

        prev_pos = self.robot.cur_pos
        self.robot._move('right')
        self.assertEqual((-1, 0), self._delta_pos(prev_pos, self.robot.cur_pos))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_run_quit(self, mock_stdout):
        user_input = 'quit'
        with unittest.mock.patch('builtins.input', side_effect=user_input):
            self.robot.run()
            self.assertTrue('Bye!' in mock_stdout.getvalue())

        sys.stdout = sys.__stdout__

    @staticmethod
    def _delta_pos(prev_pos, cur_pos):
        return prev_pos[0]-cur_pos[0], prev_pos[1]-cur_pos[1]


if __name__ == '__main__':
    unittest.main()
