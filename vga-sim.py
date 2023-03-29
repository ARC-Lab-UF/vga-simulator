#!/usr/bin/env python3
"""VGASimulator.py - Pedro José Pereira Vieito © 2016
  View VGA output from a VHDL simulation.

  Ported from VGA Simulator:
  https://github.com/MadLittleMods/vga-simulator
  by Eric Eastwood <contact@ericeastwood.com>

  More info about how to generate VGA output from VHDL simulation here:
  http://ericeastwood.com/blog/8/vga-simulator-getting-started
"""
from argparse import ArgumentParser
# If you aren't familiar with py, this error is better than reading a traceback
try:
    from PIL import Image
except ImportError:
    print("Error: Run `pip install Pillow` and try again.")
    exit(1)

def time_conversion(unit_from: str, unit_to: str, value: int) -> float:
    seconds_to = {
        "fs": 1e-15,
        "ps": 1e-12,
        "ns": 1e-9,
        "us": 1e-6,
        "ms": 1e-3,
        "s": 1,
        "sec": 1,
        "min": 60,
        "hr": 3600,
    }
    return seconds_to[unit_from] / seconds_to[unit_to] * value


def bin_to_color(binary):
    # Returns a value 0-255 corresponding to the bit depth
    # of the binary number and the value.
    # This is why your rgb values need to be padded to the full bit depth
    return int(int(binary, 2) / int("1" * len(binary), 2) * 255)


def parse_line(line: str):
    # 50 ns: 1 1 000 000 00
    time, unit, hsync, vsync, r, g, b = line.replace(':', '').split()

    return (
        time_conversion(unit, "sec", int(time)), 
        int(hsync), 
        int(vsync), 
        bin_to_color(r), 
        bin_to_color(g), 
        bin_to_color(b)
    )


def render_vga(file, frames_limit):

    vga_file = open(file, 'r')

    # From: http://tinyvga.com/vga-timing/
    res_x = 640
    res_y = 480

    # Pixel Clock: ~10 ns, 108 MHz
    pixel_clk = 39.7219464e-9

    back_porch_x = 48
    back_porch_y = 33

    h_counter = 0
    v_counter = 0

    back_porch_x_count = 0
    back_porch_y_count = 0

    last_hsync = -1
    last_vsync = -1

    time_last_line = 0      # Time from the last line
    time_last_pixel = 0     # Time since we added a pixel to the canvas

    frame_count = 0

    vga_output = None

    print('[ ] VGA Simulator')
    print('[ ] Resolution:', res_x, '×', res_y)

    for vga_line in vga_file:

        if 'U' in vga_line:
            print("Warning: Undefined values")
            continue  # Skip this timestep since it's not valid 

        time, hsync, vsync, red, green, blue = parse_line(vga_line)

        time_last_pixel += time - time_last_line

        if last_hsync == 0 and hsync == 1:
            h_counter = 0

            # Move to the next row, if past back porch
            if back_porch_y_count >= back_porch_y:
                v_counter += 1

            # Increment this so we know how far we are
            # after the vsync pulse
            back_porch_y_count += 1

            # Set this to zero so we can count up to the actual
            back_porch_x_count = 0

            # Sync on sync pulse
            time_last_pixel = 0

        if last_vsync == 0 and vsync == 1:

            # Show frame or create new frame
            if vga_output:
                vga_output.show("VGA Output")
            else:
                vga_output = Image.new('RGB', (res_x, res_y), (0, 0, 0))

            if frame_count < frames_limit or frames_limit == -1:
                print("[+] VSYNC: Decoding frame", frame_count)

                frame_count += 1
                h_counter = 0
                v_counter = 0

                # Set this to zero so we can count up to the actual
                back_porch_y_count = 0

                # Sync on sync pulse
                time_last_pixel = 0

            else:
                print("[ ]", frames_limit, "frames decoded")
                exit(0)

        if vga_output and vsync:

            # Add a tolerance so that the timing doesn't have to be bang on
            tolerance = 5e-9
            if time_last_pixel >= (pixel_clk - tolerance) and \
                time_last_pixel <= (pixel_clk + tolerance):
                # Increment this so we know how far we are
                # After the hsync pulse
                back_porch_x_count += 1

                # If we are past the back porch
                # Then we can start drawing on the canvas
                if back_porch_x_count >= back_porch_x and \
                    back_porch_y_count >= back_porch_y:

                    # Add pixel
                    if h_counter < res_x and v_counter < res_y:
                        vga_output.putpixel((h_counter, v_counter),
                                            (red, green, blue))

                # Move to the next pixel, if past back porch
                if back_porch_x_count >= back_porch_x:
                    h_counter += 1

                # Reset time since we dealt with it
                time_last_pixel = 0

        last_hsync = hsync
        last_vsync = vsync
        time_last_line = time

def main():
    parser = ArgumentParser("VGA Simulator", "Draws images from a corresponding HDL simulation file.")
    parser.add_argument("filename", help="Output file from your testbench", type=str)
    parser.add_argument("width", help="Screen width in pixels", type=int)
    parser.add_argument("height", help="Screen height in pixels", type=int)
    parser.add_argument("px_clk", help="Pixel clock frequency in MHz", type=float)
    parser.add_argument("hbp", help="Length of horizontal back porch in pixels", type=int)
    parser.add_argument("vbp", help="Length of vertical back porch in pixels", type=int)
    parser.add_argument("--max-frames", help="Maximum number of frames to draw. Default: Draw all frames", type=int, required=False, default=-1)

    args = parser.parse_args()

    with open(args.filename) as f:
        lines = f.readlines()

    render_vga(args.filename, args.max_frames)

    print("Goodbye.")

if __name__ == "__main__":
    main()

