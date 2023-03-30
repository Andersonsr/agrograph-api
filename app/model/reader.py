from app.model.models import UserProfile
from neomodel import db


def readUserMeasurements(email, uid):
    profile = UserProfile.nodes.get_or_none(email=email)
    if profile is not None:
        return profile.measurements.all()
    return None


def readMeasurementsQuery(email, uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax, varNames):
    query = ""
    db.cypher_query(query)

    return

