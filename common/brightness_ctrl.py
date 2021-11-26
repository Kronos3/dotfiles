#!/usr/bin/env python3

import subprocess

# Linear brightness control is not so nice because
# at the lowest light levels, changes in screen brightness
# will have a larger effect. At higher light levels, small
# changes will remain unnoticed.
# This lookup table is a log scale for 13 step brightness control
# with a factor of 1.4 on increase.
BRIGHTNESS_LUT = [0, 1, 2, 3, 5, 7, 10, 14, 20, 28, 40, 56, 79, 100]


def main(args):
    assert len(args) == 1, f"Invalid number of arguments: expected 1 got {len(args)}"

    # Check if we are incrementing or decrementing
    assert args[0] in ("+", "-"), f"Invalid argument {args[0]}: expected +/-"
    incrementing = args[0] == "+"

    # Check the current brightness level
    check = subprocess.run(["brightnessctl", "--machine"], stdout=subprocess.PIPE)
    assert check.returncode == 0, "Failed to execute brightnessctl"

    _, _, current, percent, max_level = check.stdout.decode().split(",")

    # Remove the '%' at the end (and convert to int)
    percent = int(percent[:-1])

    # Find the closest bucket
    closest_idx = 0
    closest_delta = percent
    for i, bucket in enumerate(BRIGHTNESS_LUT):
        current_delta = abs(bucket - percent)
        if current_delta < closest_delta:
            closest_delta = current_delta
            closest_idx = i

    if incrementing:
        next_idx = closest_idx + 1
        if next_idx >= len(BRIGHTNESS_LUT):
            # Don't go past the end
            next_idx = len(BRIGHTNESS_LUT) - 1

    else:
        next_idx = closest_idx - 1
        if next_idx < 0:
            next_idx = 0

    subprocess.run(["brightnessctl", "set", f"{BRIGHTNESS_LUT[next_idx]}%"], check=True)

    return 0


if __name__ == "__main__":
    import sys
    exit(main(sys.argv[1:]))
