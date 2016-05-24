import urllib
import json

class CheckOnline():
    def get_response(self, type):
        if type == "summoner":
            url = 'https://{region}.api.pvp.net' \
                  '/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}' \
                  '?api_key={api_key}'
            url = url.format(region=self.region,
                             summonerNames=self.summonerNames,
                             api_key=self.API_KEY)
            return urllib.urlopen(url)
        elif type == "game":
            url = 'https://{region}.api.pvp.net' \
                  '/observer-mode/rest/consumer/getSpectatorGameInfo' \
                  '/{platformId}/{summonerId}' \
                  '?api_key={api_key}'
            url = url.format(region=self.region,
                             platformId=self.platformId,
                             summonerId=self.summonerId,
                             api_key=self.API_KEY)
            return urllib.urlopen(url)
        elif type == "champion":
            url = 'https://global.api.pvp.net' \
                  '/api/lol/static-data/{region}/v1.2/champion/{id}' \
                  '?api_key={api_key}'
            url = url.format(region=self.region,
                             id=self.championId,
                             api_key=self.API_KEY)
            return urllib.urlopen(url)

    def check(self, argv):
        message_dict = [{"type": "error",
                         "message": "Summoner name not found."},
                        {"type": "error",
                         "message": "Summoner is NOT in game."},
                        {"type": "error",
                         "message": "Reigion unsupported. Please try euw, na or kr."}]
        if len(argv) >= 2 + 1:
            self.API_KEY = 'e54b0b52-0552-4de2-86f5-68a8dadd25c1'
            platformId_dict = {"euw": "EUW1", "na": "NA1", "kr": "KR"}

            self.region = argv[1]
            if self.region in platformId_dict.keys():
                self.summonerNames = ""
                for i in range(2, len(argv)):
                    self.summonerNames += argv[i]

                response = self.get_response("summoner")
                response_str = response.read()
                if response_str[0] != "{":
                    return message_dict[0]
                else:
                    data = json.loads(response_str)
                    if self.summonerNames.lower() not in data.keys():
                        return message_dict[0]
                    self.summonerId = data[self.summonerNames.lower()]["id"]
                    self.platformId = platformId_dict[self.region]

                    response = self.get_response("game")
                    response_str = response.read()
                    if response_str[0] != "{":
                        return message_dict[1]
                    else:
                        data = json.loads(response_str)
                        if "gameMode" not in data.keys():
                            return message_dict[1]
                        gameMode = data["gameMode"]
                        gameType = data["gameType"]
                        for participant in data["participants"]:
                            if participant["summonerId"] == self.summonerId:
                                summonerName = participant["summonerName"]
                                self.championId = participant["championId"]
                                response = self.get_response("champion")
                                data = json.loads(response.read())
                                championName = data['name']

                        output = "User |{summonerName}| is playing "\
                                 "|{championName}| in a |{gameMode} {gameType}|."
                        output = output.format(summonerName=summonerName,
                                               championName=championName,
                                               gameMode=gameMode,
                                               gameType=gameType)
                        return {"type": "message", "message": output}
            else:
                return message_dict[2]
