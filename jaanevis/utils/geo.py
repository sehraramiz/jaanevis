"""utils for geographical calculations"""

import reverse_geocode


def get_country_from_latlong(lat: float, long: float) -> str | None:
    loc_data = reverse_geocode.search([(lat, long)])
    if not loc_data:
        return None
    return loc_data[0]["country_code"]


if __name__ == "__main__":
    print(get_country_from_latlong(30, 50))
