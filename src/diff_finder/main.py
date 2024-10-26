import os
from tinytag import TinyTag
import numpy as np
from time import perf_counter

print(os.getcwd())
DOWNLOADS_DIRECTORY_PATH = '/Users/theobernier/Music/Téléchargements'

ITUNES_DIRECTORY = '/Users/theobernier/Music/iTunes/iTunes Media/Music'

global tracksProcessed
global batchCounter
global batchSize
global averageProcessingTimeIn
global batchTimes
global totalTracks

tracksProcessed = 0
batchCounter = 0
batchSize = 100
averageProcessingTimeInS = 0
batchTimes = []


def getTrackName(filePath):
    try:
        if os.stat(filePath).st_size > 40 * 1024 * 1024:
            return None
        start = perf_counter()
        audio = TinyTag.get(filePath)
        end = perf_counter()
        globals()['tracksProcessed'] += 1
        globals()['batchCounter'] += 1
        globals()['batchTimes'].append(end - start)
        if globals()['batchCounter'] >= globals()['batchSize']:
            batchAverage = np.mean(batchTimes)
            print('tracks processed', globals()['tracksProcessed'], ' ---- ', round(globals()['tracksProcessed']/globals()['totalTracks']*100, 1), '%')
            globals()['averageProcessingTimeInS'] = np.average([globals()['averageProcessingTimeInS'], batchAverage],
                                                               weights=[globals()['tracksProcessed'],
                                                                        globals()['batchSize']])
            print(globals()['averageProcessingTimeInS'])
            globals()['batchCounter'] = 0
            globals()['batchTimes'] = []

        return audio.title
    except:
        return None


# trackname = getTrackName(os.path.join(DOWNLOADS_DIRECTORY_PATH, 'Richar OBrien - Science Fiction, Double Feature.mp3'))


def buildFullPath(dirPath, fileName):
    return os.path.join(dirPath, fileName)


def getAllFilesInDirectory(directoryPath):
    filePaths = []
    for (dirpath, dirnames, filenames) in os.walk(directoryPath):
        filePaths.extend(
            [buildFullPath(dirpath, filename) if filename.endswith('.mp3') else None for filename in filenames])

    return list(filter(lambda a: a is not None, filePaths))


def removeNone(array):
    return list(filter(lambda a: a is not None, array))


allDowloadedFiles = getAllFilesInDirectory(DOWNLOADS_DIRECTORY_PATH)
allItunesFiles = getAllFilesInDirectory(ITUNES_DIRECTORY)

print('number of downloaded tracks ', len(allDowloadedFiles))
print('number of iTunes tracks ', len(allItunesFiles))
totalTracks = len(allDowloadedFiles) + len(allItunesFiles)

trackTitlesDownload = removeNone([getTrackName(trackPath) for trackPath in allDowloadedFiles])
trackTitlesItunes = removeNone([getTrackName(trackPath) for trackPath in allItunesFiles])


def getElementsFromAthatAreNotInB(a, b):
    return list(set(np.unique(a)) - set(np.unique(b)))


print(getElementsFromAthatAreNotInB(trackTitlesDownload, trackTitlesItunes))
