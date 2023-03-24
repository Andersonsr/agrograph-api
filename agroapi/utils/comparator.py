from datetime import datetime
from ..utils.constants import dateFormat, timeFormat


def checkTime(timeMin=None, timeMax=None, time=None):
    if timeMin is not None and timeMax is not None:
        return datetime.strptime(timeMin, timeFormat) <= datetime.strptime(time, timeFormat) \
               <= datetime.strptime(timeMax, timeFormat)

    if timeMin is not None:
        return datetime.strptime(timeMin, timeFormat) <= datetime.strptime(time, timeFormat)

    if timeMax is not None:
        return datetime.strptime(timeMax, timeFormat) >= datetime.strptime(time, timeFormat)

    return True


def checkValue(value=None, valueMin=None, valueMax=None):
    if valueMin is None and valueMax is None:
        return True
    if valueMin is not None and valueMax is not None:
        return float(valueMin) <= value <= float(valueMax)
    if valueMin is not None:
        return value >= float(valueMin)
    if valueMax is not None:
        return value <= float(valueMax)

