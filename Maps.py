import herepy
import re
import time
import speech_recognition as sr
from STT import stt_min,tts


class Maps(Main):

    def __init__(self):
        self.modes = {'walk':[herepy.RouteMode.pedestrian,herepy.RouteMode.shortest],'bus':[herepy.RouteMode.publicTransport,herepy.RouteMode.fastest],'car':[herepy.RouteMode.car,herepy.RouteMode.fastest,herepy.RouteMode.traffic_enabled]}
        self.api_key = self.getconfig("api")#"NuWLrM7oE23-PKjQWHD79izu0aFFvYdEu7wZV0SanSE"
        self.max_radius = self.getconfig("maxradius")*1000 #Enter in KM
        self.geocoderApi = herepy.GeocoderApi(self.api_key)
        self.geocoderAutoCompleteApi = herepy.GeocoderAutoCompleteApi(self.api_key)
        self.routingApi = herepy.RoutingApi(self.api_key)
        self.geocoderReverseApi = herepy.GeocoderReverseApi(self.api_key)
        self.placesApi = herepy.PlacesApi(self.api_key)

    def ui(coordinates,address,MOT):
        
        details = [getloc()]
        if coordinates == None:
            destination = None
            ''' If address is not provided asks for address and checks if it is
                a pinned location
            '''
            if address == None:
                tts("Enter an address : ")
                address = stt_min(5)
                tts(address)
            markers = open('marker.log','r')
            for line in markers:
                temp = line.strip().split(",")
                if address == temp[0]:
                    destination = [temp[1],temp[2]]
                    break
            markers.close()
            if destination == None:
                destination = getlatlong(address)   
        else:
            destination = coordinates
        details.append(destination)
        if destination == None:
            return None
        if MOT == None:
            while True:
                tts("Choose mode of travel walk,bus,car : ")
                MOT = stt_min(3)
                if MOT in modes:
                    break
                else:
                    tts("retry")
            tts(MOT)
        details.append(modes[MOT])
        return details


    def getloc():
        # Read data from gps
        coordinates = [13.031505,77.635815]
        return coordinates

    def getproximity(next_loc):
        '''
        Code to be implemented once GPS module is used
        if abs(getloc()[1]-next_loc[1])<0.00001 and abs(getloc()[0]-next_loc[0])<0.0001:
            return False
        else:
            return True
        '''
        time.sleep(1)
        return False

    def getroute(details):
        if details == None:
            tts("Unable to find location")
            return None
        try:
            response = routingApi.pedastrian_route(details[0],details[1],details[2]).as_dict()
            route = response["response"]["route"][0]["leg"][0]["maneuver"]
            info  = response["response"]["route"][0]["summary"]["text"]
            info = re.sub("<.*?>",'',info)
            tts("Number of steps :"+str(len(route)))
            tts("Info :"+str(info))
            for i in route:
                start_nav = True
                instruction = re.sub("<.*?>",'',i["instruction"])
                tts(instruction)
                if route.index(i)==len(route)-1:
                    break
                while start_nav:
                    next_loc = [i["position"]["latitude"],i["position"]["longitude"]]
                    start_nav = getproximity(next_loc)
                    time.sleep(0.5)
        except:
            tts("Unable to generate route")

    def getlatlong(destination):
        try:
            response = geocoderAutoCompleteApi.address_suggestion(destination, getloc(),max_radius).as_dict()
            if len(response["items"])==0:
                tts("No matches found")
                return None
            for i in range(min(3,len(response["items"]))):
                tts("Confirm destination: ")
                tts(response["items"][i]["title"])
                
                ans = stt_min(2)
                if not ans =="no":
                    coordinates = response["items"][i]["position"]
                    return [coordinates["lat"],coordinates["lng"]]
            tts("Provide better search input")
            return None
        except:
            tts("Unable to find location")
            return None

    def reverse_geocode():
        try:
            response = geocoderReverseApi.retrieve_addresses(getloc()).as_dict()
            address = response["items"][0]["title"]
            tts(address)
        except:
            tts("Unable to find location")

    def locate(item):          
        try:
            response = placesApi.onebox_search(getloc(),item).as_dict()
            items = response["items"]
            count = 0
            for item in items:
                coordinates = item["position"]
                if "tags" in item.keys() and "id" in item["tags"][0].keys():
                    tts(item["title"]+" "+str(item["distance"])+" meters, "+" ,".join(j["id"] for j in item["tags"]))
                else:
                    tts(item["title"]+" "+str(item["distance"])+" meters")
                if count == 3 :
                    tts("Please Input better search key")
                    return None
                tts("Do you want to navigate or see next option : ")
                state = stt_min(3)
                count = count + 1
                if state == "navigate":
                    return [coordinates['lat'],coordinates['lng']]
                elif state =="cancel":
                    return None
                time.sleep(0.5)
            return None
        except:
            return None
        

    def maps():
        tts("Maps Started")
        run = True
        while run:
            task = stt_min(3)
            tts(task)
            task = task.split(" ")
            if task[0] == 'route':
                if task[-1] in modes:
                    if len(task) >= 5:
                        details = ui(None," ".join(task[2:-2]),task[-1])
                        getroute(details)
                        run = False
                    else:
                        tts("incorrect command")
                else:
                    tts("Unrecognised mode of travel")
            elif task == ['where','am','i']:
                reverse_geocode()
                run = False
            elif task == ['pin','location']:
                tts('Enter marker name: ')
                name = stt_min(3)
                tts("marker added for "+name)
                markers = open('marker.log','r')
                lines = markers.readlines()
                markers.close()
                markers = open('marker.log','w')
                lines = [name+","+str(getloc()[0])+","+str(getloc()[1])+"\n"]+lines
                markers.writelines(lines)
                markers.close()
                run = False
            elif task[-2:] == ['near','me']:
                coordinates = locate(" ".join(task[:-2]))
                if coordinates == None:
                    tts("Search cancelled")
                else:
                    details = ui(coordinates,None,None)
                    getroute(details)
                    run = False
            elif task == ["help"]:
                tts("commands available, route to place name in vehicle, places near me, whereami, pin location")
            elif task == ['cancel'] or task ==['exit']:
                run = False
            else :
                tts("Retry")
            
        
                
            
