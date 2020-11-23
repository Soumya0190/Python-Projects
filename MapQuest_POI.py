import urllib.parse #formats location details to url
import urllib.request #requests url from MapQuest & gets response
import json #converts response to json

class MapQuest:
    
    def __init__(self, API_key):
        self.API_key = API_key
        self._BASE_URL = "http://open.mapquestapi.com/directions/v2/route"

    def totalDistance(self, locations: list) -> float:
        if len(locations) == 0 or len(locations) == 1 or len(locations) == None:
            return 0
        else:
            total_distance = 0
            for num in range(len(locations) - 1):
                query_parameters = [('key', self.API_key), ('from', locations[num]),
                                    ('to', locations[num + 1])]

                webName = urllib.parse.urlencode(query_parameters, True)
                requestUrl = self._BASE_URL + "?" + webName
                opened = urllib.request.urlopen(requestUrl)
                response = json.load(opened)
                distance = response["route"]["distance"]
                
                total_distance += distance
            
            return total_distance
            
        
    def totalTime(self, locations: list) -> int:
        if len(locations) == 0 or len(locations) == 1 or len(locations) == None:
            return 0
        else:
            total_time = 0
            for num in range(len(locations) - 1):
                query_parameters = [('key', self.API_key), ('from', locations[num]),
                                    ('to', locations[num + 1])]

                webName = urllib.parse.urlencode(query_parameters, True)
                requestUrl = self._BASE_URL + "?" + webName
                opened = urllib.request.urlopen(requestUrl)
                response = json.load(opened)
                time = response["route"]["time"]
                
                total_time += time

            return total_time


    def directions(self, locations: list) -> str:
        if len(locations) == 0 or len(locations) == 1 or len(locations) == None:
            return ''
        else:
            lst = []
            string = ""
            for num in range(len(locations) - 1):
                query_parameters = [('key', self.API_key), ('from', locations[num]),
                                    ('to', locations[num + 1])]

                webName = urllib.parse.urlencode(query_parameters, True)
                requestUrl = self._BASE_URL + "?" + webName
                opened = urllib.request.urlopen(requestUrl)
                response = json.load(opened)
                

                for dictionary in response["route"]["legs"]:
                    for direction in dictionary["maneuvers"]:
                        lst.append(direction["narrative"])
                        
            for ind in range(len(lst)):
                string = string + lst[ind] + '\n'
                    
            return string
            

        
    def pointOfInterest(self, locations: str, keyword: str, results: int) -> list:
        baseUrl = 'https://www.mapquestapi.com/search/v4/place'
        resourceURL = 'http://www.mapquestapi.com/geocoding/v1/address'
        lst = []

        query_parameters1 = [('key', self.API_key), ('location', locations)]
        webName1 = urllib.parse.urlencode(query_parameters1, True)
        requestUrl1 = resourceURL + "?" + webName1
        opened1 = urllib.request.urlopen(requestUrl1)
        response1 = json.load(opened1)
        latitude = response1["results"][0]["locations"][0]["latLng"]["lat"]
        longitude = response1["results"][0]["locations"][0]["latLng"]["lng"]
       
        string = str(longitude) + "," + str(latitude)
        query_parameters2 = [('location', string),
                             ('sort', 'distance'), ('key', self.API_key),
                             ('pageSize', results), ('q', keyword)]
        webName2 = urllib.parse.urlencode(query_parameters2, True)
        requestUrl2 = baseUrl + "?" + webName2
        opened2 = urllib.request.urlopen(requestUrl2)
        response2 = json.load(opened2)
        for result in response2["results"]:
            lst.append(result["displayString"])
        
        return lst
            
            
            


