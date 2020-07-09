import subprocess


class Main(object):
    config={}
    voice={}
    
    def __init__(self):
        self.loadconfig()
        self.loadvoice()
        self.writefunction("a")
        subprocess.Popen(['python3','./FaceRec.py',self.getconfig("rnn_model"),self.getconfig("cnn_model"),self.getconfig("dictionary")])
        #if self.getconfig("videoen"):
        #    subprocess.Popen(['python','./Video.py'])
        #else:
        #    subprocess.Popen(['python','./Video.py','1'])
        self.voiceOutEn = int(self.getconfig("voiceouten"))
        self.voiceInEn = int(self.getconfig("voiceinen"))
        self.textOutEn = int(self.getconfig("textouten"))
        self.voiceSpeed = self.getconfig("voicespeed")
        self.modeluse = False
        
    def loadconfig(self):
        configs = open("./config.txt","r")
        for line in configs:
            line = line.rstrip()
            line = line.split("=")
            Main.config[line[0]]= line[1]
        configs.close()
        self.voiceOutEn = int(self.getconfig("voiceouten"))
        self.voiceInEn = int(self.getconfig("voiceinen"))
        self.textOutEn = int(self.getconfig("textouten"))
        self.voiceSpeed = self.getconfig("voicespeed")

    def loadvoice(self):
        voices = open("./voice.txt","r")
        for line in voices:
            line = line.rstrip()
            line = line.split("=")
            Main.voice[line[0]]= line[1:]
        voices.close()
        
    def getconfig(self,conf):
        try: 
            return int(Main.config[conf])
        except:
            return Main.config[conf]
    
    def getcommand(self,voice):
        return Main.voice[voice]

    def stt(self,timeouttype="longanswer"):
        timeout = self.getconfig(timeouttype)
        if self.voiceInEn:
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            while True:
                response = {
                    "success": True,
                    "error": None,
                    "transcription": None
                    }
                with microphone as source:
                    recognizer.pause_threshold = 0.8
                    audio = recognizer.record(source,duration=timeout)
                try:
                    response["transcription"] = recognizer.recognize_google(audio)
                except sr.RequestError:
                    response["success"] = False
                    response["error"] = "API unavailable"
                except sr.UnknownValueError:
                    response["error"] = "Unable to recognize speech"
                if response["transcription"] != None:
                    break
                if not response["success"]:
                    break
                tts("Retry")
            transcription = response["transcription"].lower()
        else:
            transcription = input("").lower()
        self.tts(transcription)
        return transcription
            
    def tts(self,voice):
        if self.voiceOutEn:
            subprocess.call(["espeak", "-s"+self.voiceSpeed+" -ven+18 -z", voice], stderr = subprocess.DEVNULL)
        if self.textOutEn and not self.voiceInEn:
            print(voice)

    def writefunction(self,function):
        Function = open("./Function","w")
        Function.write(function)
        Function.close()

    def readfunction(self):
        Function = open("./Function","r")
        output = Function.readlines()[0]
        Function.close()
        return output


