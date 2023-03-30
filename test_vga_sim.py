import unittest
from vga_sim import *

class TestVGASimUtils(unittest.TestCase):
    def test_time_conversion(self):
        self.assertAlmostEqual(time_conversion(5, "sec", "sec"), 5.0)
        for i in range(0, 100, 10):
            self.assertAlmostEqual(time_conversion(i, "ns", "sec"), i * 1e-9)


    def test_bin_to_color(self):
        # for i in range(1, 5):
        #     self.assertEqual(vga_sim.bin_to_color(0, i), 0)
        #
        # self.assertEqual(vga_sim.bin_to_color(1, 1), 255)
        # self.assertEqual(vga_sim.bin_to_color(3, 2), 255)
        # self.assertEqual(vga_sim.bin_to_color(7, 3), 255)
        pass


    def test_parse_line(self):
        line = "50 ns: 1 1 000 111 00"
        correct = (
            50e-9,
            1,
            1,
            0,
            255,
            0
        )
        for test_val, correct_val in zip(parse_line(line), correct):
            self.assertAlmostEqual(test_val, correct_val)

        # self.assertTupleEqual(vga_sim.parse_line(line), correct)  # Doesn't play nicely with Tuple[float, int, int...] types :(
        # no such thing as self.assertTupleAlmostEqual either :( PEP time?

