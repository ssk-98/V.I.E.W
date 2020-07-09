import pickle
import subprocess
from subprocess import call

from CaptionGenerator import CaptionGenerator
#from Maps import maps
from STT import stt,tts
from DistanceMeasurement import measurement
from OCR import ocr
from FaceRec import facerec,caption


class Main:
    def __init__(self):
        self.face_data = pickle.loads(open('./encoding.pickle', "rb").read())
        self.config={}
        self.voice={}
        configs = open("./config.txt","r")
        for line in configs:
            line = line.rstrip()
            line = line.split("=")
            self.config[line[0]]= line[1]
        configs.close()
        voices = open("./Voice.txt","r")
        for line in voices:
            line = line.rstrip()
            line = line.split("=")
            self.voice[line[0]]= str(line[1:])
        voices.close()
        self.caption_generator=CaptionGenerator(
        rnn_model_place=self.getconfig("rnn_model"),
        cnn_model_place=self.getconfig("cnn_model"),
        dictionary_place=self.getconfig("dictionary"),
        )
        print("Loading done starting subprocess")
        subprocess.call('./Video.py')
        
    def getconfig(self,conf):
        return self.config[conf]
    
    def getvoice(self,voice):
        return self.voice[voice]

    def loop(self):
        while True:
            tts(self.getvoice("mainloop"))
            operation = stt(int(self.getconfig("shortanswer")))
            tts(operation)
            if operation == self.getvoice("maps"):
                maps()
            if operation == self.getvoice("facerec"):
                print("face")
            if operation == self.getvoice("ocr"):
                print("ocr")
            if operation in self.getvoice("exit"):
                Function.open("./Function")
                Function.write("q")
                Function.close()
                return 

if __name__ == '__main__':
    start = Main()
    start.loop()

