#!/usr/bin/env python

import argparse
import sys

import lanelet2.io
import lanelet2.projection


def print_layer(layer, layer_name):
    print("IDs in " + layer_name)
    print(sorted([elem.id for elem in layer]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Path to the input osm file")
    parser.add_argument("--has-id", type=int, help="Check if the ID is present in the map")
    args = parser.parse_args()

    projector = lanelet2.projection.MercatorProjector(lanelet2.io.Origin(49, 8))
    lanelet_map = lanelet2.io.load(args.filename, projector)

    layers = {
        "Points": lanelet_map.pointLayer,
        "Line Strings": lanelet_map.lineStringLayer,
        "Polygons": lanelet_map.polygonLayer,
        "Lanelets": lanelet_map.laneletLayer,
        "Areas": lanelet_map.areaLayer,
        "Regulatory Elements": lanelet_map.regulatoryElementLayer,
    }

    for layer_name, layer in layers.items():
        if not args.has_id:
            print_layer(layer, layer_name)
        else:
            for elem in layer:
                if elem.id == args.has_id:
                    print("Found ID " + str(elem.id) + " in layer " + layer_name)
                    sys.exit(0)
    if args.has_id:
        print("ID " + args.has_id + " not in map")
