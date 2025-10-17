import argparse
import os
from .heatmap import Heatmap

def float_0_90(value):
    f = float(value)
    if not 0 <= f <= 90:
        raise argparse.ArgumentTypeError(f"{value} must be between 0 and 90")
    return f

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("topLeftX", type=float_0_90, help="Angle in degrees (0–90)")
    parser.add_argument("topLeftY", type=float_0_90, help="Angle in degrees (0–90)")
    parser.add_argument("bottomRightX", type=float_0_90, help="Angle in degrees (0–90)")
    parser.add_argument("bottomRightY", type=float_0_90, help="Angle in degrees (0–90)")

    parser.add_argument("-r", "--resolution", type=int)

    args = parser.parse_args()

    if args.resolution != None:
        res = args.resolution
    else:
        res = 5

    heatmap = Heatmap((args.topLeftX, args.topLeftY), (args.bottomRightX, args.bottomRightY), res)
    heatmap.genGrid()
    print("fetching data...", end="\r")
    heatmap.fetchData()
    print(" " * 20, end="\r")
    heatmap.renderMap()
    print("\ndone!", end="\r")
    print(" " * 5, end="\r")

if __name__ == "__main__":
    main()