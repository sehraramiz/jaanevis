from jaanevis.domain import geojson as geo

LAT, LONG = 30.0, 50.0
COUNTRY = "IR"


def test_geojson_point_init() -> None:
    coordinates = (LONG, LAT)
    point = geo.GeoJsonPoint(coordinates=coordinates)

    assert point.coordinates == coordinates
    assert point.type == "Point"


def test_geojson_feature_init() -> None:
    geometry = geo.GeoJsonPoint(coordinates=(LONG, LAT))
    feature = geo.GeoJsonFeature(geometry=geometry)

    assert feature.type == "Feature"
    assert feature.geometry == geometry
