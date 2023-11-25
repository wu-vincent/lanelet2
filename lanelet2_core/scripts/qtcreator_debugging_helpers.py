# this file contains functions needed by qtcreator to provide a better introspection into lanelet's objects.
# simply specify its path in qtCreator under Options->Debugger->Locals&Expressionts->Extra debugging helpers.
from dumper import Children, SubItem


def get_vector_size(vector_value):
    inner_type = vector_value.type[0]
    (start, finish, alloc) = vector_value.split("ppp")
    size = int((finish - start) / inner_type.size())
    return size


def get_map_size(map_value):
    (compare, stuff, parent, left, right, size) = map_value.split("pppppp")
    return size


def get_unordered_map_size(value):
    try:
        # gcc ~= 4.7
        size = value["_M_element_count"].integer()
        start = value["_M_before_begin"]["_M_nxt"]
    except (BaseException,):
        try:
            # libc++ (Mac)
            size = value["_M_h"]["_M_element_count"].integer()
            start = value["_M_h"]["_M_bbegin"]["_M_node"]["_M_nxt"]
        except (BaseException,):
            try:
                # gcc 4.9.1
                size = value["_M_h"]["_M_element_count"].integer()
                start = value["_M_h"]["_M_before_begin"]["_M_nxt"]
            except (BaseException,):
                # gcc 4.6.2
                size = value["_M_element_count"].integer()
                start = value["_M_buckets"].dereference()
    return size


def display_string_value(d, value):
    inner_type = value.type[0]
    (data, size) = value.split("pI")
    d.check(0 <= size)  # and size <= alloc and alloc <= 100*1000*1000)
    d.putCharArrayHelper(data, size, inner_type, d.currentItemFormat(), makeExpandable=False)


def qdump__lanelet__LineString2d(d, value):
    data = value["constData_"]["_M_ptr"].dereference()
    d.putValue(data["id"].integer())
    d.putNumChild(4)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("id", data["id"])
            d.putSubItem("inverted", value["inverted_"])
            d.putSubItem("attributes", data["attributes"])
            d.putSubItem("points", data["points_"])


def qdump__lanelet__ConstLineString2d(d, value):
    qdump__lanelet__LineString2d(d, value)


def qdump__lanelet__LineString3d(d, value):
    data = value["constData_"]["_M_ptr"].dereference()
    d.putValue(data["id"].integer())
    d.putNumChild(4)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("id", data["id"])
            d.putSubItem("inverted", value["inverted_"])
            d.putSubItem("attributes", data["attributes"])
            d.putSubItem("points", data["points_"])


def qdump__lanelet__ConstLineString3d(d, value):
    qdump__lanelet__LineString3d(d, value)


def qdump__lanelet__Polygon3d(d, value):
    qdump__lanelet__LineString3d(d, value)


def qdump__lanelet__ConstPolygon3d(d, value):
    qdump__lanelet__ConstLineString3d(d, value)


def qdump__lanelet__Polygon2d(d, value):
    qdump__lanelet__LineString2d(d, value)


def qdump__lanelet__ConstPolygon2d(d, value):
    qdump__lanelet__ConstLineString2d(d, value)


def qdump__lanelet__Point3d(d, value):
    data = value["constData_"]["_M_ptr"].dereference()
    d.putValue(data["id"].integer())
    d.putNumChild(6)
    if d.isExpanded():
        p = data["point"]
        with Children(d):
            (x, y, z) = p.split("ddd")
            with SubItem(d, "x"):
                d.putValue(x)
                d.putType("double")
            with SubItem(d, "y"):
                d.putValue(y)
                d.putType("double")
            with SubItem(d, "z"):
                d.putValue(z)
                d.putType("double")
            d.putSubItem("id", data["id"])
            d.putSubItem("attributes", data["attributes"])
            d.putSubItem("point2d_", data["point2d_"])


def qdump__lanelet__Point2d(d, value):
    qdump__lanelet__Point3d(d, value)


def qdump__lanelet__ConstPoint3d(d, value):
    qdump__lanelet__Point3d(d, value)


def qdump__lanelet__ConstPoint2d(d, value):
    qdump__lanelet__Point3d(d, value)


def qdump__lanelet__Lanelet(d, value):
    data = value["constData_"]["_M_ptr"].dereference()
    d.putValue(data["id"].integer())
    d.putNumChild(8)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("id", data["id"])
            d.putSubItem("attributes", data["attributes"])
            d.putSubItem("leftBound", data["leftBound_"])
            d.putSubItem("rightBound", data["rightBound_"])
            d.putSubItem("regulatoryElements", data["regulatoryElements_"])
            d.putSubItem("centerline", data["centerline_"])
            d.putSubItem("inverted", value["inverted_"])


def qdump__lanelet__ConstLanelet(d, value):
    qdump__lanelet__Lanelet(d, value)


def qdump__lanelet__Area(d, value):
    data = value["constData_"]["_M_ptr"].dereference()
    d.putValue(data["id"].integer())
    d.putNumChild(7)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("id", data["id"])
            d.putSubItem("attributes", data["attributes"])
            d.putSubItem("outerBound", data["outerBound_"])
            d.putSubItem("innerBounds", data["innerBounds_"])
            d.putSubItem("regulatoryElements", data["regulatoryElements_"])
            d.putSubItem("outerBoundPolygon", data["outerBoundPolygon_"])
            d.putSubItem("innerBoundPolygons", data["innerBoundPolygons_"])


def qdump__lanelet__ConstArea(d, value):
    qdump__lanelet__Area(d, value)


def qdump__lanelet__CompoundPolygon3d(d, value):
    data = value["data_"]["_M_ptr"].dereference()

    d.putItemCount(get_vector_size(data["ls_"]))
    if d.isExpanded():
        with Children(d):
            d.putSubItem("data", data)


def qdump__lanelet__HybridMap(d, value):
    d.putItemCount(get_map_size(value["m_"]))
    d.putNumChild(2)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("map", value["m_"])
            d.putSubItem("vector", value["v_"])


def qdump__lanelet__Attribute(d, value):
    display_string_value(d, value["value_"])
    d.putNumChild(2)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("cache_", value["cache_"])
            d.putSubItem("value_", value["value_"])


def qdump__lanelet__RegulatoryElement(d, value):
    data = value["constData_"]["_M_ptr"].dereference()
    d.putValue(data["id"].integer())
    d.putNumChild(3)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("id", data["id"])
            d.putSubItem("attributes", data["attributes"])
            d.putSubItem("parameters", data["parameters"])


def qdump__lanelet__PrimitiveLayer(d, value):
    umap = value["elements_"]
    d.putItemCount(get_unordered_map_size(umap))
    d.putNumChild(2)
    if d.isExpanded():
        with Children(d):
            d.putSubItem("elements", umap)
            d.putSubItem("tree", value["tree_"])
