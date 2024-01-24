import requests

import json
import datetime
from itertools import groupby


def planetConvert(planetCode):
    planet = 0
    planetCode = planetCode.lower()
    if(planetCode == "mercury"):
        planet = "199"
    elif(planetCode == "venus"):
        planet = "299"
    elif(planetCode == "moon"):
        planet = "301"
    elif(planetCode == "mars"):
        planet = "499"
    elif(planetCode == "jupiter"):
        planet = "599"
    elif(planetCode == "saturn"):
        planet = "699"
    elif(planetCode == "uranus"):
        planet = "799"
    elif(planetCode == "neptune"):
        planet = "899"
    elif(planetCode == "sun"):
        planet = "10"

    return planet
def getDate():
    
    dates = []
    dates.append(datetime.datetime.today().strftime ('%Y-%m-%d %H:00'))
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(hours=6)

    dates.append(NextDay_Date.strftime ('%Y-%m-%d %H:00'))


    return dates



# Generates the api call to horizions using the current date and the given planet
# TODO Add a function that interprets the different planets and bodies into horizons codes
def genAPICall(planet):
    dates = getDate()
   # apiURL = "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='499'&OBJ_DATA=NO&MAKE_EPHEM='YES'&EPHEM_TYPE=O&SKIP_DAYLT='NO'&SITE_COORD='-79.37942, 43.67040 0.1'&COORD_TYPE='GEODETIC'&CENTER='coord@ 399'&START_TIME='2023-07-24 UT-4'&STOP_TIME='2023-07-25'&STEP_SIZE='1m'&QUANTITIES='4'&APPARENT='REFRACTED'"
    apiURL = "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='" + planet + "'&OBJ_DATA=NO&MAKE_EPHEM='YES'&EPHEM_TYPE=O&SKIP_DAYLT='NO'&SITE_COORD='-79.37942, 43.67040 0.1'&COORD_TYPE='GEODETIC'&CENTER='coord@ 399'&START_TIME='" + dates[0] + " UT-4'&STOP_TIME='" + dates[1] + "'&STEP_SIZE='1m'&QUANTITIES='4'&APPARENT='REFRACTED'"
    
    #apiURL = "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='1998-067A'&OBJ_DATA=NO&MAKE_EPHEM='YES'&EPHEM_TYPE=O&SKIP_DAYLT='NO'&SITE_COORD='-79.37942, 43.67040 0.1'&COORD_TYPE='GEODETIC'&CENTER='coord@ 399'&START_TIME='" + dates[0] + " UT-4'&STOP_TIME='" + dates[1] + "'&STEP_SIZE='1m'&QUANTITIES='4'&APPARENT='REFRACTED'"

    #1998-067A
    return apiURL

def jsonRequest(apiURL):
    horizonsResponse = requests.get(apiURL)

    responseContent = horizonsResponse.content

    jsonResponse = json.loads(responseContent)

    horizionsData = jsonResponse['result']


    return horizionsData


def efphemCut(horizionsData):

    # finds the $$SOE or start of ephemris tag that notes the begining of the data
    efphemBegin = horizionsData.find("$$SOE") + 5

    # finds the $$EOE or end of ephemris tag that notes the end of the data
    efphemEnd = horizionsData.find("$$EOE")
    #Cuts the response data down to only the ephem data
    efphemData = horizionsData[efphemBegin: efphemEnd]

    efphemData.strip()


    # splits all the parts of the efphem data based on spaces 
    efphemData = efphemData.split(" ")

    #Filters out all empty indexs from ephemList
    efphemData = list(filter(None, efphemData))

    #Pops the first index out which is always empty
    efphemData.pop(0)

    efphemDataFiltered = []
    for c in range (len(efphemData)):
        if efphemData[c].isalpha() == False and '*' not in efphemData[c]:
            efphemData[c] = efphemData[c].strip()
            efphemDataFiltered.append(efphemData[c])

    return efphemDataFiltered

def efphemBreak(efphemDataFiltered):
    
    efphemFinal = [efphemDataFiltered[i:i+4] for i in range(0, len(efphemDataFiltered), 4)]


    for x in efphemFinal:
        del x[0]
    
    # for x in efphemFinal:
    #     x[1] = float(x[1])
    #     x[2] = float(x[2])

    return efphemFinal


def jsonDumps(efphemFinal):
    ephemDict = {}
    ephemDict.update({"data":efphemFinal})


    jsonDumped = json.dumps(ephemDict)
    
  

    return jsonDumped


def horizonsMainRun(planetCode):
    planet = planetConvert(planetCode)
    apiURL = genAPICall(planet)
    horizionsData = jsonRequest(apiURL)
    efphemDataFiltered = efphemCut(horizionsData)

    efphemFinal = efphemBreak(efphemDataFiltered)
    
    
    dumpedJsonFin = jsonDumps(efphemFinal)

    
    return dumpedJsonFin






