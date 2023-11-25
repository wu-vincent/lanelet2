#!/usr/bin/env python

import argparse

import lanelet2.io
import lanelet2.projection


def make_positive(layer):
    for elem in layer:
        if elem.id < 0:
            elem.id = layer.uniqueId()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Path to the input osm file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("output", help="Path to results", nargs="?")
    group.add_argument("-i", "--inplace", action="store_true", help="Overwrite input file")
    args = parser.parse_args()

    if args.inplace:
        args.output = args.filename

    projector = lanelet2.projection.MercatorProjector(lanelet2.io.Origin(49, 8))
    lanelet_map = lanelet2.io.load(args.filename, projector)

    make_positive(lanelet_map.pointLayer)
    make_positive(lanelet_map.lineStringLayer)
    make_positive(lanelet_map.polygonLayer)
    make_positive(lanelet_map.laneletLayer)
    make_positive(lanelet_map.areaLayer)
    make_positive(lanelet_map.regulatoryElementLayer)

    lanelet2.io.write(args.output, lanelet_map, projector)
