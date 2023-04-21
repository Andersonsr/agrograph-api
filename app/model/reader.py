from app.model.models import UserProfile
from neomodel import db


def readUserMeasurements(uid):
    profile = UserProfile.nodes.get_or_none(uid=uid)
    if profile is not None:
        return profile.measurements.all()
    return None


def readMeasurementsQuery(uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax, varNames):
    query = ""
    db.cypher_query(query)

    return

