from app.model.models import UserProfile
from neomodel import db


def readUserMeasurements(uid):
    profile = UserProfile.nodes.get_or_none(uid=uid)
    if profile is not None:
        return profile.measurements.all()
    return None


def readMeasurementsQuery(uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax, varNames):
    query = "CALL spatial.intersects('layer', {} ) YiELD node " \
            "OPTIONAL MATCH (v:Variable)<-[oq:What]-(m:Measurement)-[o:Where]->(node)" \
            "WITH m, v MATCH (m)<-[p:Measurements]-(u:User) WHERE u.email = '$email'" \
            "RETURN DISTINCT v.tipo" \
            "ORDER BY v.tipo" \
            ""
    db.cypher_query(query)

    return

