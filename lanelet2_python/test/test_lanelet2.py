import unittest

from lanelet2.core import (
    AttributeMap,
    getId,
    BasicPoint2d,
    Point3d,
    LineString3d,
    Lanelet,
    TrafficLight,
    createMapFromLanelets,
)
from lanelet2.geometry import distance, intersects2d, boundingBox2d, to2D, intersection


def get_attributes():
    return AttributeMap({"key": "value"})


def get_point():
    return Point3d(getId(), 0, 0, 0, get_attributes())


def get_line_string():
    return LineString3d(getId(), [get_point(), get_point()], get_attributes())


def get_lanelet():
    return Lanelet(getId(), get_line_string(), get_line_string(), get_attributes())


def get_regelem():
    return TrafficLight(getId(), AttributeMap(), [get_line_string()], get_line_string())


def get_lanelet_map():
    lanelet = get_lanelet()
    lanelet.addRegulatoryElement(get_regelem())
    return createMapFromLanelets([lanelet])


def check_primitive_id(test_class, primitive):
    primitive.id = 30
    test_class.assertEqual(primitive.id, 30)


def check_primitive_attributes(test_class, primitive):
    lenBefore = len(primitive.attributes)
    primitive.attributes["newkey"] = "newvalue"
    test_class.assertEqual(lenBefore + 1, len(primitive.attributes))
    test_class.assertTrue("newkey" in primitive.attributes)
    test_class.assertEqual(primitive.attributes["newkey"], "newvalue")
    del primitive.attributes["newkey"]
    test_class.assertFalse("newkey" in primitive.attributes)


class LaneletApiTestCase(unittest.TestCase):
    def test_lanelet_id(self):
        check_primitive_id(self, get_lanelet())

    def test_lanelet_attributes(self):
        check_primitive_attributes(self, get_lanelet())

    def test_lanelet_modification(self):
        lanelet = get_lanelet()
        bound = get_line_string()
        lanelet.leftBound = bound
        self.assertEqual(bound, lanelet.leftBound)

    def test_lanelet_regelem(self):
        regelem = get_regelem()
        llt = get_lanelet()
        llt.addRegulatoryElement(regelem)
        self.assertEqual(len(llt.trafficLights()), 1)
        self.assertEqual(len(llt.trafficSigns()), 0)
        self.assertEqual(len(llt.regulatoryElements), 1)


class LaneletMapApiTestCase(unittest.TestCase):
    def test_lanelet_map_basic(self):
        map = get_lanelet_map()
        self.assertEqual(len(map.laneletLayer), 1)
        self.assertEqual(len(map.regulatoryElementLayer), 1)

    def test_lanelet_map_search(self):
        map = get_lanelet_map()
        nearest = map.laneletLayer.nearest(BasicPoint2d(0, 0), 1)
        self.assertEqual(len(nearest), 1)
        self.assertTrue(map.laneletLayer.exists(nearest[0].id))


class GeometryApiTestCase(unittest.TestCase):
    def test_distance_p2p(self):
        self.assertEqual(distance(get_point(), get_point()), 0)

    def test_distance_basic_p2p(self):
        self.assertEqual(distance(get_point().basicPoint(), get_point()), 0)

    def test_distance_l2l(self):
        self.assertEqual(distance(get_line_string(), get_line_string()), 0)

    def test_distance_llt2llt(self):
        self.assertEqual(distance(get_lanelet(), get_lanelet()), 0)

    def test_intersects_l2l(self):
        self.assertTrue(intersects2d(to2D(get_line_string()), to2D(get_line_string())))

    def test_bounding_box_line(self):
        bbox = boundingBox2d(to2D(get_line_string()))
        self.assertEqual(bbox.min.x, 0)

    def test_intersection_l2l(self):
        point_list = intersection(to2D(get_line_string()), to2D(get_line_string()))
        self.assertEqual(point_list[0].x, 0.0)
        self.assertEqual(point_list[0].y, 0.0)


if __name__ == "__main__":
    unittest.main()
