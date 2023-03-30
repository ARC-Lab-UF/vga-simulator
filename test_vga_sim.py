import unittest
vga_sim = __import__("vga-sim")

class TestVGASimUtils(unittest.TestCase):
    def test_time_conversion(self):
        self.assertAlmostEqual(vga_sim.time_conversion("sec", "sec", 5), 5.0)
        for i in range(0, 100, 10):
            self.assertAlmostEqual(vga_sim.time_conversion("ns", "sec", i), i * 1e-9)


    def test_bin_to_color(self):
        self.assertEqual(vga_sim.bin_to_color("000"), 0)
        self.assertEqual(vga_sim.bin_to_color("00"), 0)

        self.assertEqual(vga_sim.bin_to_color("111"), 255)
        self.assertEqual(vga_sim.bin_to_color("11"), 255)


    def test_parse_line(self):
        line = "50 ns: 1 1 000 000 00"
        correct = (
            50e-9,
            1,
            1,
            0,
            0,
            0
        )
        for test_val, correct_val in zip(vga_sim.parse_line(line), correct):
            self.assertAlmostEqual(test_val, correct_val)

        # self.assertTupleEqual(vga_sim.parse_line(line), correct)  # Doesn't play nicely with Tuple[float, int, int...] types :(
        # no such thing as self.assertTupleAlmostEqual either :( PEP time?

