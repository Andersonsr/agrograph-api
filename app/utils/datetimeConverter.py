from datetime import datetime
from app.utils.constants import DATE_FORMAT, TIME_FORMAT


def datetimeCreator(dateString):
    formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d/%m/%y", "%m/%d/%y",
               "%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d", "%d-%m-%y", "%m-%d-%y", TIME_FORMAT]
    separators = [' ', ', ']

    if not isinstance(dateString, str):
        return False

    for dateFormat in formats:
        try:
            return datetime.strptime(dateString, dateFormat)
        except ValueError:
            for separator in separators:
                if dateFormat != TIME_FORMAT:
                    try:
                        return datetime.strptime(dateString, dateFormat + separator + TIME_FORMAT)
                    except ValueError:
                        pass

    return False


def convertDatetime(dateString, outputFormat):
    dateObj = datetimeCreator(dateString)
    if not dateObj or (dateObj.year == 1900 and outputFormat == DATE_FORMAT):
        return None
    try:
        return dateObj.strftime(outputFormat)
    except ValueError:
        return None


if __name__ == "__main__":
    print(convertDatetime('10/11/22 22:00:00', DATE_FORMAT))
    print(convertDatetime('22:00:00', TIME_FORMAT))
    print(convertDatetime('22:00', TIME_FORMAT))
    print(convertDatetime('22:00:00', DATE_FORMAT))
    print(convertDatetime('10-11-2020', DATE_FORMAT))

