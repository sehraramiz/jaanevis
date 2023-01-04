from jaanevis.domain import geojson as geo


def test_geojson_point_init() -> None:
    lat = 1.0
    long = 2.0
    coordinates = (long, lat)
    point = geo.GeoJsonPoint(coordinates=coordinates)

    assert point.coordinates == coordinates
    assert point.type == "Point"


def test_geojson_feature_init() -> None:
    geometry = geo.GeoJsonPoint(coordinates=(2.0, 1.0))
    feature = geo.GeoJsonFeature(geometry=geometry)

    assert feature.type == "Feature"
    assert feature.geometry == geometry
