#!/usr/bin/env python3
from argparse import ArgumentParser
from io import TextIOWrapper
# If you aren't familiar with py, this error is better than reading a traceback
try:
    from PIL import Image
except ImportError:
    print("Error: Run `pip install Pillow` and try again.")
    exit(1)


def time_conversion(value: int, unit_from: str, unit_to: str) -> float:
    """Convert a value between units of time"""
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


def bin_to_color(binary: str) -> int:
    """Maps a binary number to 0-255. 
    Supply the width of the original binary number
    (e.g., "0101" is value of 5, width of 4.)"""
    # Returns a value 0-255 corresponding to the bit depth
    # of the binary number and the value.
    # This is why your rgb values need to be padded to the full bit depth
    return int(int(binary, 2) / int("1" * len(binary), 2) * 255)


def parse_line(line: str):
    """Parses a line from the vga text file.
    Lines tend to look like this:
    `50 ns: 1 1 000 000 00`
    The function returns a tuple of each of these in appropriate data types (see below).
    """
    time, unit, hsync, vsync, r, g, b = line.replace(':', '').split()

    return (
        time_conversion(int(time), unit, "sec"), 
        int(hsync), 
        int(vsync), 
        bin_to_color(r), 
        bin_to_color(g), 
        bin_to_color(b)
    )


def render_vga(file: TextIOWrapper, width: int, height: int, pixel_freq_MHz: float, hbp: int, vbp: int, max_frames: int) -> None:
    # From: http://tinyvga.com/vga-timing/

    # Pixel Clock: ~10 ns, 108 MHz
    pixel_clk = 1e-6 / pixel_freq_MHz 

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
    print('[ ] Resolution:', width, '×', height)

    for vga_line in file:

        if 'U' in vga_line:
            print("Warning: Undefined values")
            continue  # Skip this timestep since it's not valid 

        time, hsync, vsync, red, green, blue = parse_line(vga_line)

        time_last_pixel += time - time_last_line

        if last_hsync == 0 and hsync == 1:
            h_counter = 0

            # Move to the next row, if past back porch
            if back_porch_y_count >= vbp:
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
                vga_output = Image.new('RGB', (width, height), (0, 0, 0))

            if frame_count < max_frames or max_frames == -1:
                print("[+] VSYNC: Decoding frame", frame_count)

                frame_count += 1
                h_counter = 0
                v_counter = 0

                # Set this to zero so we can count up to the actual
                back_porch_y_count = 0

                # Sync on sync pulse
                time_last_pixel = 0

            else:
                print("[ ]", max_frames, "frames decoded")
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
                if back_porch_x_count >= hbp and \
                    back_porch_y_count >= vbp:

                    # Add pixel
                    if h_counter < width and v_counter < height:
                        vga_output.putpixel((h_counter, v_counter),
                                            (red, green, blue))

                # Move to the next pixel, if past back porch
                if back_porch_x_count >= hbp:
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

    with open(args.filename) as file:
        render_vga(file, args.width, args.height, args.px_clk, args.hbp, args.vbp, args.max_frames)

    print("Goodbye.")

if __name__ == "__main__":
    main()

