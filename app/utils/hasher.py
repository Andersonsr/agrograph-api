from hashlib import sha256


def hashIt(date, time, uid, latitude, longitude):
    if time is None:
        string = date + uid + str(latitude) + str(longitude)
    else:
        string = date + time + uid + str(latitude) + str(longitude)
    hasher = sha256()
    hasher.update(string.encode())
    return hasher.hexdigest()


if __name__ == '__main__':
    print(hashIt('10/10/2010', '10:45:00', 1, 0.2, 0.3))
