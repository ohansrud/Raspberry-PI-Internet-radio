from pprint import pprint
from bson import ObjectId
from pymongo import MongoClient
from utils import *
client = MongoClient('localhost', 27017)

db = client.radio

stations = db.stations
post_data = [
    {
        "station": "NDR-2",
        "desc": "Nord-Deutsche Radio",
        "logo": "http://db.radioline.fr/pictures/radio_0e62e5fb859c362c86fb1fafbee10e73/logo200.jpg",
        "stream": "https://ndr-dg-ndr-https-fra-dtag-cdn.sslcast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3"
    },
    {
        "station": "N-JOY",
        "desc": "N-JOY Deutschland",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Njoy-logo.svg/1200px-Njoy-logo.svg.png",
        "stream": "https://ndr-dg-ndr-https-dus-dtag-cdn.sslcast.addradio.de/ndr/njoy/live/mp3/128/stream.mp3",
        "playing": True
    }
]


# [{'_id': ObjectId('5d96cf6374fece3b5c98513b'), 'station': 'NDR-2', 'desc': 'Nord-Deutsche Radio', 'logo': 'http://db.radioline.fr/pictures/radio_0e62e5fb859c362c86fb1fafbee10e73/logo200.jpg', 'stream': 'https://ndr-dg-ndr-https-fra-dtag-cdn.sslcast.addradio.de/ndr/ndr2/niedersachsen/mp3/128/stream.mp3'},
#  {'_id': ObjectId('5d96cf6374fece3b5c98513c'), 'station': 'N-JOY', 'desc': 'N-JOY Deutschland', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Njoy-logo.svg/1200px-Njoy-logo.svg.png', 'stream': 'https://ndr-dg-ndr-https-dus-dtag-cdn.sslcast.addradio.de/ndr/njoy/live/mp3/128/stream.mp3', 'playing': True}]

# post = {'id': 2}

# result = db.current.insert_one(post)
# console_logger(result)


def getAllStations():
    result = db.stations.find()
    return list(result)


def getStationById(id):
    return db.stations.find_one({'_id': id})

def getCurrentStation():
    result = db.stations.find_one({'playing': True})
    if(result == None):
        console_logger('No stations with Playing found. Return first on list')
        result = db.stations.find_one()
    return result


def getNextStation(current):
    stationId = current['_id']
    console_logger(stationId)

    result = db.stations.find_one({'_id':{'$gt': stationId} })
    if(result == None):
        console_logger('Next station not found. Returning to first station.')
        result = db.stations.find_one()
    return result


def setAllToFalse():
    val = {'$set': {'playing': False}}
    res = db.stations.update_many({}, val)
    console_logger('All set to false')
    console_logger(res)


def setToPlaying(station):
    val = {'$set': {'playing': True}}
    console_logger(station)
    q = {'_id': station['_id']}

    res = db.stations.update_one(q, val)
    console_logger('Set to True')
    console_logger(res.modified_count)


def playNext():
    current = getCurrentStation()
    setAllToFalse()
    console_logger(current)
    console_logger('Setting next station...')
    nextStation = getNextStation(current)
    console_logger('Next station found...')
    console_logger(nextStation)

    setToPlaying(nextStation)
