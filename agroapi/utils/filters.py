from agroapi.models import UserProfile, Location, Variable, Measurement, Date
from shapely.geometry import Polygon, Point
from datetime import datetime
from .constants import dateFormat, timeFormat


def filterByLocation(measurements, data):
    response = []
    pointsArray = []

    if data is None:
        return measurements

    if len(data) < 3:
        return measurements

    try:
        for e in data:
            pointsArray.append((e.longitude, e.latitude))

    except TypeError:
        return measurements

    except AttributeError:
        return measurements

    polygon = Polygon(pointsArray)

    for e in measurements:
        location = e.where.all()[0]
        if polygon.contains(Point(location.longitude, location.latitude)):
            response.append(e)
    return response


def filterByDate(measurements, dateMin, dateMax):
    response = []
    if dateMin is None and dateMax is None:
        return measurements

    for e in measurements:
        keepIt = True
        date = e.when.all()[0].date
        if dateMin is not None:
            if datetime.strptime(dateMin, dateFormat) > date:
                keepIt = False

        if dateMax is not None:
            if datetime.strptime(dateMax, dateFormat) < date:
                keepIt = False

        if keepIt:
            response.append(e)

    return response

