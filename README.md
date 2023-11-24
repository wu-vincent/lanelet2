# Lanelet2x

Lanelet2x is a fork of lanelet2 library with all dependencies on ROS1, ROS2 or Catkin removed to create a standalone and
cross-platform library.

[![CI](https://github.com/wu-vincent/lanelet2x/actions/workflows/ci.yaml/badge.svg)](
https://github.com/wu-vincent/lanelet2x/actions/workflows/ci.yaml)
[![CD](https://github.com/wu-vincent/lanelet2x/actions/workflows/cd.yaml/badge.svg)](
https://github.com/wu-vincent/lanelet2x/actions/workflows/cd.yaml)
[![PyPI - Version](https://img.shields.io/pypi/v/lanelet2x)](
https://pypi.org/project/lanelet2x)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/lanelet2x)](
https://pypi.org/project/lanelet2x)
![PyPI - Python Version](
https://img.shields.io/pypi/pyversions/lanelet2x?logo=python&logoColor=white)

## Overview

Lanelet2 is a C++ library for handling map data in the context of automated driving. It is designed to utilize
high-definition map data in order to efficiently handle the challenges posed to a vehicle in complex traffic scenarios.
Flexibility and extensibility are some of the core principles to handle the upcoming challenges of future maps.

Features:

- **2D and 3D** support
- **Consistent modification**: if one point is modified, all owning objects see the change
- Supports **lane changes**, routing through areas, etc.
- **Separated routing** for pedestrians, vehicles, bikes, etc.
- Many **customization points** to add new traffic rules, routing costs, parsers, etc.
- **Simple convenience functions** for common tasks when handling maps
- **Accurate Projection** between the lat/lon geographic world and local metric coordinates
- **IO Interface** for reading and writing e.g. _osm_ data formats (this does not mean it can deal with _osm maps_)
- **Python** bindings for the whole C++ interface
- **Boost Geometry** support for all thinkable kinds of geometry calculations on map primitives
- Released under the [**BSD 3-Clause license**](LICENSE)
- Support **Windows**, **Linux** and **MacOS**

![](lanelet2_core/doc/images/lanelet2_example_image.png)

Lanelet2 is the successor of the old [liblanelet](https://github.com/phbender/liblanelet/tree/master/libLanelet) that
was developed in 2013. If you know Lanelet1, you might be interested
in [reading this](lanelet2_core/doc/Lanelet1Compability.md).

## Documentation

You can find more documentation in the individual packages and in doxygen comments. Here is an overview on the most
important topics:

- [Here](lanelet2_core/doc/LaneletPrimitives.md) is more information on the basic primitives that make up a Lanelet2
  map.
- [Read here](lanelet2_core/doc/Architecture.md) for a primer on the **software architecture** of lanelet2.
- There is also some [documentation](lanelet2_core/doc/GeometryPrimer.md) on the geometry calculations you can do with
  lanelet2 primitives.
- If you are interested in Lanelet2's **projections**, you will find
  more [here](lanelet2_projection/doc/Map_Projections_Coordinate_Systems.md).
- To get more information on how to create valid maps, see [here](lanelet2_maps/README.md).

## Installation

### PyPI

Lanelet2x can be installed from PyPI.

```
pip install lanelet2x
```

### Using Docker

- [ ] **TODO**: We are currently working on the Docker container

### Manual installation

At least **C++14** is required.

### Dependencies

* `Boost` (from 1.58)
* `eigen3`
* `pugixml` (for lanelet2_io)
* `boost-python, python2 or python3` (for lanelet2_python)
* `geographiclib` (for lanelet2_projection)

### Building

We use Conan 2.0 to manage all C++ dependencies, first clone the project:

```bash
git clone https://github.com/wu-vincent/lanelet2x.git
cd lanelet2x
```

Install conan from PyPI and create a profile:

```bash
pip install -r requirements.txt
conan profile detect
```

Now we are ready to build

```bash
conan create . --build=missing
```

## Examples

Examples and common use cases in both C++ and Python can be found [here](lanelet2_examples/README.md).

## Packages

* **lanelet2** is the meta-package for the whole lanelet2 framework
* **lanelet2_core** implements the basic library with all the primitives, geometry calculations and the LanletMap object
* **lanelet2_io** is responsible for reading and writing lanelet maps
* **lanelet2_traffic_rules** provides support to interpret the traffic rules encoded in a map
* **lanelet2_projection** for projecting maps from WGS84 (lat/lon) to local metric coordinates
* **lanelet2_routing** implements the routing graph for routing or reachable set or queries as well as collision
  checking
* **lanelet2_maps** provides example maps and functionality to visualize and modify them easily in JOSM
* **lanelet2_matching** provides functions to determine in which lanelet an object is/could be currently located
* **lanelet2_python** implements the python interface for lanelet2
* **lanelet2_validation** provides checks to ensure a valid lanelet2 map
* **lanelet2_examples** contains tutorials for working with Lanelet2 in C++ and Python

## Citation

If you are using Lanelet2 for scientific research, we would be pleased if you would cite
our [publication](http://www.mrt.kit.edu/z/publ/download/2018/Poggenhans2018Lanelet2.pdf):

```latex
@inproceedings{poggenhans2018lanelet2,
  title     = {Lanelet2: A High-Definition Map Framework for the Future of Automated Driving},
  author    = {Poggenhans, Fabian and Pauls, Jan-Hendrik and Janosovits, Johannes and Orf, Stefan and Naumann, Maximilian and Kuhnt, Florian and Mayr, Matthias},
  booktitle = {Proc.\ IEEE Intell.\ Trans.\ Syst.\ Conf.},
  year      = {2018},
  address   = {Hawaii, USA},
  owner     = {poggenhans},
  month     = {November},
  Url={http://www.mrt.kit.edu/z/publ/download/2018/Poggenhans2018Lanelet2.pdf}
}
```

