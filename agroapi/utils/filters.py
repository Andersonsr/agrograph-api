from shapely.geometry import Polygon, Point
from datetime import datetime
import json
from ..model.reader import readUserMeasurements
from ..utils.constants import dateFormat, timeFormat
from .comparator import checkTime, checkValue


def filterByLocation(measurements=None, polygonData=None):
    response = []
    pointsArray = []

    if polygonData is None:
        return measurements

    if len(polygonData) < 3:
        return measurements

    try:
        for point in polygonData:
            pointsArray.append((point["longitude"], point["latitude"]))

    except TypeError:
        return measurements

    polygon = Polygon(pointsArray)

    for measurement in measurements:
        location = measurement.location.all()[0]
        if polygon.contains(Point(location.longitude, location.latitude)):
            response.append(measurement)
    return response


def filterByDate(measurements=None, dateMin=None, dateMax=None, timeMin=None, timeMax=None):
    response = []
    if dateMin is None and dateMax is None:
        return measurements

    for measurement in measurements:
        keepIt = True
        date = measurement.date.all()[0].date
        if dateMin is not None:
            keepIt = datetime.strptime(dateMin, dateFormat) < date
            if datetime.strptime(dateMin, dateFormat) == date:
                keepIt = checkTime(timeMin, timeMax, measurement.time)

        if dateMax is not None:
            keepIt = datetime.strptime(dateMax, dateFormat) > date
            if datetime.strptime(dateMax, dateFormat) == date:
                keepIt = checkTime(timeMin, timeMax, measurement.time)

        if keepIt:
            response.append(measurement)

    return response


def applyALlFilters(email=None, uid=None, polygon=None, dateMin=None, dateMax=None, valueMin=None, valueMax=None,
                    timeMin=None, timeMax=None, varNames=None):
    data = []
    measurements = readUserMeasurements(email, uid)
    # if polygon is not None:
    #     measurements = filterByLocation(measurements, json.loads(polygon))
    #
    # measurements = filterByDate(measurements, dateMin, dateMax, timeMin, timeMax)

    for measurement in measurements:

        variables = measurement.variables.all()
        varArray = []
        for variable in variables:
            if (varNames is None or variable.name in varNames) and checkValue(variable, valueMin, valueMax):
                varData = {
                    "variable": variable.name,
                    "value": variable.value,
                    "unit": variable.unit
                }
                varArray.append(varData)

        if len(varArray) > 0:
            info = {
                "longitude": measurement.location.all()[0].longitude,
                "latitude": measurement.location.all()[0].latitude,
                "date": measurement.date.all()[0].date.strftime(dateFormat),
                "variables": varArray
            }
            data.append(info)

    return json.dumps(data)

