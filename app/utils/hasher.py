import random
from datetime import datetime
from hashlib import sha256
from app.utils.constants import DATETIME_FORMAT
from random import Random


def hashIt(date, time, uid, latitude, longitude):
    if time is None:
        string = date + uid + str(latitude) + str(longitude)
    else:
        string = date + time + uid + str(latitude) + str(longitude)
    hasher = sha256()
    hasher.update(string.encode())
    return hasher.hexdigest()


def tokenize(timestamp, mail):
    randomizer = Random()
    string = timestamp + mail + str(randomizer.randint(1, 9999999))
    hasher = sha256()
    hasher.update(string.encode())
    return hasher.hexdigest()


if __name__ == '__main__':
    print(hashIt('10/10/2010', '10:45:00', '1', 0.2, 0.3))
    print(tokenize(datetime.now().strftime(DATETIME_FORMAT), 'silenciobruno@homipeixe.com'))
