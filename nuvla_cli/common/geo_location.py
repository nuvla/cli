"""

"""
import re
import logging
from typing import List, Tuple
import random

import shapefile
from shapely.geometry import shape, Point
from nuvla.api import Api as NuvlaAPI

logger: logging.Logger = logging.getLogger(__name__)


def locate_nuvlaedge(nuvla: NuvlaAPI, location: Tuple, nuvlaedge_uuid: str):
    """

    :param nuvla:
    :param location:
    :param nuvlaedge_uuid:
    :return:
    """
    nuvla.edit(nuvlaedge_uuid, data={'location': location})


def generate_random_coordinate(count: int, country: str,
                               shp_location: str = 'data/geo/'
                                                   'World_Countries.shp') -> List[Tuple]:
    """
    Inspired by
    https://gis.stackexchange.com/questions/164005/getting-random-coordinates-based-on-country
    :param count:
    :param country:
    :param shp_location:
    :return:
    """
    logger.info(f'Gathering {count} random locations in {country}')

    # reading shapefile with pyshp library
    shapes = shapefile.Reader(shp_location)

    # getting feature(s) that match the country name
    country = [s for s in shapes.records() if country in s][0]

    # getting feature(s)'s id of that match
    country_id = int(re.findall(r'\d+', str(country))[0])

    shape_records = shapes.shapeRecords()
    feature = shape_records[country_id].shape.__geo_interface__

    shp_geom = shape(feature)

    minx, miny, maxx, maxy = shp_geom.bounds

    random_locations: List[Tuple] = []
    for i in range(count):
        while True:
            p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if shp_geom.contains(p):
                random_locations.append((p.x, p.y))
                break

    return random_locations
