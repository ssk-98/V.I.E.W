import herepy
import re
import time
import speech_recognition as sr


from Main import Main


class Maps(Main):

    def __init__(self):
        self.modes = {'walk':[herepy.RouteMode.pedestrian,herepy.RouteMode.shortest],'bus':[herepy.RouteMode.publicTransport,herepy.RouteMode.fastest],'car':[herepy.RouteMode.car,herepy.RouteMode.fastest,herepy.RouteMode.traffic_enabled]}
        self.api_key = self.getconfig("maps_api")#"NuWLrM7oE23-PKjQWHD79izu0aFFvYdEu7wZV0SanSE"
        self.max_radius = self.getconfig("maxradius")*1000 #Enter in KM
        self.geocoderApi = herepy.GeocoderApi(self.api_key)
        self.geocoderAutoCompleteApi = herepy.GeocoderAutoCompleteApi(self.api_key)
        self.routingApi = herepy.RoutingApi(self.api_key)
        self.geocoderReverseApi = herepy.GeocoderReverseApi(self.api_key)
        self.placesApi = herepy.PlacesApi(self.api_key)
        self.current_coordinates = [0,0]
        self.loadconfig()

    def ui(self,coordinates,MOT):
        details = [self.getlocation()]
        if coordinates == None:
            destination = None
            ''' If address is not provided asks for address and checks if it is
                a pinned location
            '''
            if address == None:
                self.tts("Enter an address : ")
                address = self.stt("longanswer")
            markers = open('marker.log','r')
            for line in markers:
                temp = line.strip().split(",")
                if address == temp[0]:
                    destination = [temp[1],temp[2]]
                    break
            markers.close()
            if destination == None:
                destination = self.getlatlong(address)   
        else:
            destination = coordinates
        details.append(destination)
        if destination == None:
            return None
        if MOT == None:
            while True:
                tts("Choose mode of travel walk,bus,car : ")
                MOT = self.stt("shortanswer")
                if MOT in modes:
                    break
                else:
                    self.tts("retry")
        details.append(modes[MOT])
        return details


    def getlocation(self):
        # Read data from gps
        self.current_coordinates = [13.031505,77.635815]
        return self.current_coordinates

    def getroute(self,details):
        if details == None:
            self.tts("Unable to find location")
            return None
        try:
            response = routingApi.pedastrian_route(details[0],details[1],details[2]).as_dict()
            route = response["response"]["route"][0]["leg"][0]["maneuver"]
            info  = response["response"]["route"][0]["summary"]["text"]
            info = re.sub("<.*?>",'',info)
            self.tts("Number of steps :"+str(len(route)))
            self.tts("Info :"+str(info))
            for i in route:
                start_nav = True
                instruction = re.sub("<.*?>",'',i["instruction"])
                self.tts(instruction)
                if route.index(i)==len(route)-1:
                    break
                while start_nav:
                    next_loc = [i["position"]["latitude"],i["position"]["longitude"]]
                    start_nav = self.getproximity(next_loc)
                    time.sleep(0.5)
        except:
            self.tts("Unable to generate route")

    def getlatlong(self,destination):
        try:
            response = self.geocoderAutoCompleteApi.address_suggestion(destination, getloc(),max_radius).as_dict()
            if len(response["items"])==0:
                self.tts("No matches found")
                return None
            for i in range(min(3,len(response["items"]))):
                self.tts("Confirm destination: ")
                self.tts(response["items"][i]["title"])
                
                ans = self.stt("shortanswer")
                if not ans =="no":
                    coordinates = response["items"][i]["position"]
                    return [coordinates["lat"],coordinates["lng"]]
            self.tts("Provide better search input")
            return None
        except:
            self.tts("Unable to find location")
            return None

    def reverse_geocode(self):
        try:
            response = self.geocoderReverseApi.retrieve_addresses(self.getlocation()).as_dict()
            address = response["items"][0]["title"]
            self.tts(address)
        except:
            self.tts("Unable to find location")

    def locate(self,item):          
        try:
            response = self.placesApi.onebox_search(self.getlocation(),item).as_dict()
            items = response["items"]
            count = 0
            for item in items:
                coordinates = item["position"]
                if "tags" in item.keys() and "id" in item["tags"][0].keys():
                    self.tts(item["title"]+" "+str(item["distance"])+" meters, "+" ,".join(j["id"] for j in item["tags"]))
                else:
                    self.tts(item["title"]+" "+str(item["distance"])+" meters")
                if count == 3 :
                    self.tts("Please Input better search key")
                    return None
                self.tts("Do you want to navigate or see next option : ")
                state = self.stt("veryshortanswer")
                count = count + 1
                if state == "navigate":
                    return [coordinates['lat'],coordinates['lng']]
                elif state =="cancel":
                    return None
                time.sleep(0.5)
            return None
        except:
            return None
        

    def mapsloop(self):
        self.tts("mapsstart")
        run = True
        while run:
            self.tts("mapschoice")
            task = self.stt("shortanswer")
            task = task.split(" ")
            if task[0] == 'route':
                if len(task) >= 5:
                    self.ui(None," ".join(task[2:-2]),task[-1])
                else:
                    self.ui(None," ".join(task[2:-2]),None)
            elif task == ['where','am','i']:
                self.reverse_geocode()
            elif task == ['pin','location']:
                self.tts('Enter marker name: ')
                name = self.stt("shortanswer")
                self.tts("marker added for "+name)
                markers = open('marker.log','r')
                lines = markers.readlines()
                markers.close()
                markers = open('marker.log','w')
                lines = [name+","+str(getloc()[0])+","+str(getloc()[1])+"\n"]+lines
                markers.writelines(lines)
                markers.close()
                run = False
            elif task[-2:] == ['near','me']:
                self.locate(" ".join(task[:-2]))
            elif task[0] in self.getcommand("help"):
                self.tts("mapshelp")
            elif task[0] in self.getcommand("exit"):
                run = False
            else :
                self.tts("unknowncommand")
            
        
                
            
