# vga-simulator

Simulate display output of a VGA core by running a testbench.

Original VGA Simulator: https://www.ericeastwood.com/lab/vga-simulator/

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
❯ ./vga_sim.py -h
usage: Draws images from a corresponding HDL simulation file.

positional arguments:
  filename              Output file from your testbench
  width                 Screen width in pixels
  height                Screen height in pixels
  px_clk                Pixel clock frequency in MHz
  hbp                   Length of horizontal back porch in pixels
  vbp                   Length of vertical back porch in pixels

options:
  -h, --help            show this help message and exit
  --max-frames MAX_FRAMES
                        Maximum number of frames to draw. Default: Draw all frames
```

## Examples
To run a 640x480 @60Hz ([standard](http://tinyvga.com/vga-timing/640x480@60Hz)), run `./vga_sim.py vga_log.txt 640 480 25.175 48 33`
or, `python vga_sim.py vga_log.txt 640 480 25.175 48 33`

Output images can be saved by using the save command in your image viewer.

# Testing
To run unit tests, simply run `python -m unittest` in the root directory of the project.
Test discovery will automatically detect and run tests.

# Contributing
Found a bug? Submit an issue in the Issues pane.

Want to contribute? Draft a pull request with your proposed changes.
