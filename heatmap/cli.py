#!/usr/bin/env python3

import argparse
import os
from .heatmap import Heatmap

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("topLeftX", type=float)
    parser.add_argument("topLeftY", type=float)
    parser.add_argument("bottomRightX", type=float)
    parser.add_argument("bottomRightY", type=float)

    parser.add_argument("-r", "--resolution", type=int)

    args = parser.parse_args()

    if args.resolution != "None":
        res = args.resolution
    else:
        res = 5

    heatmap = Heatmap((args.topLeftX, args.topLeftY), (args.bottomRightX, args.bottomRightY), res)
    heatmap.genGrid()
    print("fetching data...", end="\r", flush=True)
    heatmap.fetchData()
    print(" " * 16, end="\r")
    heatmap.renderMap()
    print("\ndone!", end="\r")
    print(" " * 5, end="\r")