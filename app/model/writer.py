from datetime import datetime
from ..utils.hasher import hashIt
from app.model.models import UserProfile, Location, Variable, Measurement, Date
from ..utils.constants import DATE_FORMAT, TIME_FORMAT
from app.utils.datetimeConverter import convertDatetime


def getOrCreateVariable(name, unit, value, category):
    if Variable.nodes.get_or_none(name=name, unit=unit, value=value, category=category) is None:
        return Variable(name=name, unit=unit, value=value, category=category).save()

    return Variable.nodes.get(name=name, unit=unit, value=value, category=category)


def getOrCreateDate(date):
    if Date.nodes.get_or_none(date=datetime.strptime(date, DATE_FORMAT)) is None:
        return Date(date=datetime.strptime(date, DATE_FORMAT)).save()

    return Date.nodes.get(date=datetime.strptime(date, DATE_FORMAT))


def getOrCreateLocation(longitude, latitude):
    if Location.nodes.get_or_none(latitude=latitude, longitude=longitude) is None:
        return Location(latitude=latitude, longitude=longitude).save()

    return Location.nodes.get(latitude=latitude, longitude=longitude)


def writeMeasurement(longitude, latitude, name, value, unit, date, time, category, uid):
    profile = UserProfile.nodes.get(uid=uid)
    date = convertDatetime(date, DATE_FORMAT)
    if time is not None:
        time = convertDatetime(time, TIME_FORMAT)

    if Measurement.nodes.get_or_none(hash=hashIt(date, time, uid, latitude, longitude)) is None:
        if time is not None:
            timeToInsert = datetime.strptime(time, TIME_FORMAT)
            digest = hashIt(date, time, uid, latitude, longitude)
            measurement = Measurement(hash=digest, time=timeToInsert)
        else:
            measurement = Measurement(hash=hashIt(date, time, uid, latitude, longitude))

        measurement.save()
        profile.measurements.connect(measurement)
        measurement.location.connect(getOrCreateLocation(longitude, latitude))
        measurement.date.connect(getOrCreateDate(date))
        measurement.variables.connect(getOrCreateVariable(name, unit, value, category))

    else:
        measurement = Measurement.nodes.get(hash=hashIt(date, time, uid, latitude, longitude))
        measurement.variables.connect(getOrCreateVariable(name, unit, value, category))
        measurement.save()


