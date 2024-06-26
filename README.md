# vga-simulator

Simulate display output of a VGA core by running a testbench.

Original VGA Simulator: https://ericeastwood.com/blog/vga-simulator-getting-started/

Adapted from [pvieito/VGASimulator.py](https://gist.github.com/pvieito/8cdb54a9a03fd36e51c8df6e331a3006)

# Prerequisites
- This project was tested on Python 3.11.2. It is not guaranteed to work on other versions.
- Install dependencies:
```bash
pip install Pillow
```

# Setup
Paste the contents of `log_signals.vhdl` into your VGA core testbench file. 
The process will write a text file with timestamped signal values.

The default filename is `vga_out.txt`.

# Usage
Run `./vga_sim.py --help` for usage instructions.

Or, run via the Python interpreter: `python vga_sim.py --help`

```
❯ ./vga_sim.py --help
usage: Draws images from a corresponding HDL simulation file.

positional arguments:
  filename              Output file from your testbench
  width                 Screen width in pixels (default: 640)
  height                Screen height in pixels (default: 480)
  px_clk                Pixel clock frequency in MHz (default: 25.175)
  hbp                   Length of horizontal back porch in pixels (default: 48)
  vbp                   Length of vertical back porch in pixels (default: 33)

options:
  -h, --help            show this help message and exit
  --max-frames MAX_FRAMES
                        Maximum number of frames to draw. Default: Draw all frames (default: -1)
```

## Examples
The default configuration of the simulator is 640x480 @ 60Hz ([standard](http://tinyvga.com/vga-timing/640x480@60Hz)). Simply run `./vga_sim.py vga_log.txt`
or, `python vga_sim.py vga_log.txt`.

Output images can be saved by using the save command in your image viewer.

To customize resolution/framerate/etc., use the positional command-line arguments specified in `./vga_sim.py --help`.

# Testing
To run unit tests, simply run `python -m unittest` in the root directory of the project.
Test discovery will automatically detect and run tests.

# Contributing
Found a bug? Submit an issue in the Issues pane.

Want to contribute? Draft a pull request with your proposed changes.
