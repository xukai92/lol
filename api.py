"""
API for fetching mastery page from a given summoner.
"""


import json
import urllib
import confidential


API_KEY = confidential.API_KEY


def filterJSONDict(jsonDict):
    """
    Filter a JSON dictionary by checking if there is no response
    :param jsonDict: a dictionary from JSON response
    :return: returns None if reponse is not found, else the original dict
    """
    if jsonDict.has_key('status'):  # If the dictionary has a top level key
        return None                 # called "status", it means it doesn't
    else:                           # get the information needed
        return jsonDict


def getSummoners(params):
    """
    Fetch summoners' information
    :param params: {"region": "...", "summonerNames": "..."}
    :return: {
                u'{nameInLowercase}': {
                    u'profileIconId'    :   ...,
                    u'summonerLevel'    :   ...,
                    u'revisionDate'     :   ...,
                    u'id'               :   ...,
                    u'name'             :   ...
                }
             }
    """
    url = 'https://{region}.api.pvp.net' \
          '/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     summonerNames=params["summonerNames"],     # multiple summoner names should be
                     api_key=API_KEY)                           # in a form of "name1,name2"
    response = urllib.urlopen(url)          # get response from API
    responseStr = response.read()           # read the response into string
    jsonDict = json.loads(responseStr)      # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def getMatchList(params):
    """
    Fetch summoner's match list
    :param params: {"region": "...", "summonerId": "..."}
    :return: {
                "matches": [
                    {
                        "lane": "MID",
                        "champion": 38,
                        "platformId": "EUW1",
                        "season": "SEASON2015",
                        "region": "EUW",
                        "matchId": 2120255420,
                        "queue": "RANKED_SOLO_5x5",
                        "role": "SOLO",
                        "timestamp": 1432334472308
                    }
                    ...
                ]
             }
    """
    url = 'https://{region}.api.pvp.net' \
          '/api/lol/{region}/v2.2/matchlist/by-summoner/{summonerId}' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     summonerId=params["summonerId"],
                     api_key=API_KEY)
    response = urllib.urlopen(url)      # get response from API
    responseStr = response.read()       # read the response into string
    jsonDict = json.loads(responseStr)  # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def filterMatchListByChampion(matchList, championId):
    """
    :param matchList: match list to be filtered
    :param championId: champion ID
    :return: filtered match list
    """
    filterMatchList = {"matches": []}
    for matchDict in matchList["matches"]:
        if matchDict["champion"] == championId:     # if champion ID equals
            filterMatchList["matches"].append(matchDict)
    return filterMatchList


def getMatchByMatchId(params):
    """
    :param params: {"region": "...", "matchId": "..."}
    :return: {
                  "queueType": "RANKED_SOLO_5x5",
                  "matchVersion": "5.9.0.318",
                  "platformId": "EUW1",
                  "season": "SEASON2015",
                  "region": "EUW",
                  "matchId": 2120255420,
                  "mapId": 11,
                  "matchCreation": 1432334472308,
                  "teams": [...],
                  "participants": [
                    {
                      "stats": {...},
                      "championId": 91,
                      "participantId": 1,
                      "runes": [...],
                      "highestAchievedSeasonTier": "PLATINUM",
                      "masteries": [
                        {
                          "masteryId": 4111,
                          "rank": 1
                        },
                        ...
                      ],
                      "spell2Id": 14,
                      "teamId": 100,
                      "timeline": {...},
                      "spell1Id": 4
                    },
                    ...
                  ],
                  "matchMode": "CLASSIC",
                  "matchDuration": 2171,
                  "participantIdentities": [
                    {
                        "player": {
                        "profileIcon": 19,
                        "summonerId": 27952221,
                        "matchHistoryUri": "/v1/stats/player_history/EUW1/31819470",
                        "summonerName": "Malm"
                      },
                      "participantId": 1
                    },
                    ...
                  ],
                  "matchType": "MATCHED_GAME"
             }
    """
    url = 'https://{region}.api.pvp.net' \
          '/api/lol/{region}/v2.2/match/{matchId}' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     matchId=params["matchId"],
                     api_key=API_KEY)
    response = urllib.urlopen(url)      # get response from API
    responseStr = response.read()       # read the response into string
    jsonDict = json.loads(responseStr)  # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def getChampionInfo(params):
    """
    Get all champion info
    :param params: {"region": "..."}
    :return: {
                "data": {
                    "MonkeyKing": {
                      "title": "the Monkey King",
                      "id": 62,
                      "key": "MonkeyKing",
                      "name": "Wukong"
                    },
                    ...
                },
                "version": "6.8.1",
                "type": "champion"
             }
    """
    url = 'https://global.api.pvp.net' \
          '/api/lol/static-data/{region}/v1.2/champion' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     api_key=API_KEY)
    response = urllib.urlopen(url)      # get response from API
    responseStr = response.read()       # read the response into string
    jsonDict = json.loads(responseStr)  # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def championId2Name(championId, region="euw"):
    """
    Map champion ID to champion name.
    :param championId: champion ID
    :param region: region
    :return: champion name
    """
    championInfo = getChampionInfo({"region": region})
    if championInfo:
        for championName in championInfo["data"].keys():    # see getChampionInfo() for JSON response structure
            if championInfo["data"][championName]["id"] == championId:
                return championName
        return None
    else:
        return None


def genChampionDict(region="euw"):
    """
    Generate champion dictionary.
    :param region: region
    :return: {championName: championId}
    """
    championInfo = getChampionInfo({"region": region})
    if championInfo:
        championDict = {}
        for championName in championInfo["data"].keys():
            championDict[championName] = championInfo["data"][championName]["id"]
        return championDict
    else:
        return None


def getMasteryInfo(params):
    """
    Get mastery info, including master ID, name and image.
    :param params: {"region": "..."}
    :return: {
                "data": {
                    "6142": {
                      "description": [
                        "Deal 2.5% increased damage to targets with impaired movement (slow, stun, root, taunt, etc.)"
                      ],
                      "id": 6142,
                      "name": "Oppressor",
                      "image": {
                        "w": 48,
                        "full": "6121.png",
                        "sprite": "mastery0.png",
                        "group": "gray_mastery",
                        "h": 48,
                        "y": 384,
                        "x": 240
                      }
                    },
                    ...
                },
                ,
                "version": "6.8.1",
                "type": "mastery"
             }
    """
    url = 'https://global.api.pvp.net' \
          '/api/lol/static-data/euw/v1.2/mastery?masteryListData=image&' \
          'api_key={api_key}'
    url = url.format(region=params["region"],
                     api_key=API_KEY)
    response = urllib.urlopen(url)      # get response from API
    responseStr = response.read()       # read the response into string
    jsonDict = json.loads(responseStr)  # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def genMasteryDict(region="euw"):
    """
    Generate mastery dictionary.
    :param region:
    :return: {masteryId: {"name": masteryName, "description": [...]}}
    """
    masteryInfo = getMasteryInfo({"region": region})
    if masteryInfo:
        masteryDict = {}
        for masteryId in masteryInfo["data"].keys():
            masteryDict[int(masteryId)] = masteryInfo["data"][masteryId]
        return masteryDict
    else:
        return None


def formatMasteries(masteries):
    """
    Format masteries to render to .html
    :param masteries: masteries
    :return:
    """
    masterySet = set()
    for mastery in masteries:
        masterySet.add(mastery["masteryId"])
    return masterySet


def printJSONDict(jsonDict):
    """
    Print a nested dictionary in a pretty way
    :param jsonDict: JSON dictionary
    """
    print json.dumps(jsonDict, sort_keys=False, indent=2)


def getMasteriesBySummonerAndChampion(summonerName, championName, region="euw"):
    """
    Find a summoner's latest mastery page of given champion
    :param summonerName: summoner's name
    :param championName: champion name
    :param region: region
    :return: the mastery page
    """
    # Champion name to ID
    championDict = genChampionDict()
    championId = championDict[championName]  # name to ID

    # Get summoner's ID
    summonerDict = getSummoners({"region": region, "summonerNames": summonerName})
    if summonerDict:
        nameInLowerCase = list(summonerDict)[0]
        summonerId = summonerDict[nameInLowerCase]["id"]
    else:
        return None

    # Get summoner's match list
    matchList = getMatchList({"region": region, "summonerId": summonerId})
    if matchList:
        # Get summoner's match ID list by specifying champion ID
        filteredMatchList = filterMatchListByChampion(matchList, championId)
        matchIdList = [match["matchId"] for match in filteredMatchList["matches"]]
        latestMatchID = matchIdList[0]  # get the lastest one
    else:
        return None

    # Get match by match ID
    match = getMatchByMatchId({"region": region, "matchId": latestMatchID})
    if match:
        # Get masteries by champion ID
        for participant in match["participants"]:
            if participant["championId"] == championId:
                return participant["masteries"]
    else:
        return None


def printMasteriesOfASummonerWithAChampion(summonerName, championName, region="euw"):
    """
    Print formatted masteries.
    This function is only for test purpose.
    :param summonerName: summoner name
    :param championName: champion name
    :param region: region
    """
    print "Summoner |{summonerName}| is recently playing |{championName}| with masteries:".format(
        summonerName=summonerName,
        championName=championName
    )

    masteries = getMasteriesBySummonerAndChampion(summonerName, championName, region)
    masteryDict = genMasteryDict()
    for mastery in masteries:
        print "{masterName} * {rank}:\n  {description}".format(
            masterName=masteryDict[mastery["masteryId"]]["name"],
            rank=mastery["rank"],
            description=masteryDict[mastery["masteryId"]]["description"][mastery["rank"] - 1]
        )
        print "  [img] http://ddragon.leagueoflegends.com/cdn/6.9.1/img/mastery/{image}".format(
            image=masteryDict[mastery["masteryId"]]["image"]["full"]
        )


def main():
    # cd = genChampionDict()
    # cns = cd.keys()
    # cns.sort()
    # for cn in cns:
    #     print '                  <option value="{cn}">{cn}</option>'.format(
    #         cn=cn
    #     )

    # printMasteriesOfASummonerWithAChampion("Hide on bush", "Corki", "kr")
    masteries = getMasteriesBySummonerAndChampion("Hide on bush", "Corki", "kr")
    print formatMasteries(masteries)

if __name__ == "__main__":
    main()
