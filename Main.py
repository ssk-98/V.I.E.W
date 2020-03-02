import cv2
import time
import subprocess
import glob
import face_recognition
import argparse
import pickle

from CaptionGenerator import CaptionGenerator
from subprocess import call


# Incase a PI camera is being used. All the commented code lines pertain to the Pi camera code
#from picamera.array import PiRGBArray
#from picamera import PiCamera

def facerec(image):
    boxes = face_recognition.face_locations(image,model='hog')
    encodings=face_recognition.face_encodings(image, boxes)
    names=[]
    for encoding in encodings:
        matches=face_recognition.compare_faces(data["encodings"],encoding, tolerance = 0.45)
        name="Unknown"
        if True in matches:
            matchedIdxs=[i for (i,b) in enumerate(matches) if b]
            counts={}
            for i in matchedIdxs:
                name=data["names"][i]
                counts[name]=counts.get(name,0)+1
                name=max(counts, key=counts.get)
        names.append(name)
    return names

def tts(text):
    # Creates a subprocess on Linux machines
    # espeak is a function in linux that is used to generate the Text To Speech output
    call(["espeak","-s130 -ven+18 -z",text],stderr = subprocess.DEVNULL)


def caption(frame):
    # Call the caption generator class and seeprates the sentence from the details
    captions = caption_generator.generate(frame)
    cap=[]
    for i in captions:
        cap.append(i["sentence"])
    return cap

if __name__ == '__main__':
    
    # Reading the face data
    data = pickle.loads(open('encoding.pickle', "rb").read())
    
    # Loading the various models.On an average this takes about a min in RPi 3
    
    caption_generator=CaptionGenerator(
        rnn_model_place="../data/caption_en_model40.model",
        cnn_model_place="../data/ResNet50.model",
        dictionary_place="../data/mscoco_caption.json",
        )
    # Used in case of PI camera. However a PI camera does not provide enough resolution for best results
    #camera = PiCamera()
    #camera.resolution = (640,480)
    #camera.framerate = 32
    #rawCapture = PiRGBArray(camera,(640,480))
    #cap1 =cv2.VideoCapture('rtsp://192.168.43.200:4619/h264_ulaw.sdp')
    
    cap = cv2.VideoCapture(0)
    tts("Ready")

    while(True):
        ret, image = cap.read()

    # Display the resulting frame
        cv2.imshow('Frame',image)
        inputkey = cv2.waitKey(1)
        '''
        Await user input to decide the function to be performed
        q     : Quit
        e     : Run face recognition on the image captured
        w     : Generate captions for the image captured
        r     : Run caption generator on the images stored in this folder ( For debug purposes )
        '''
        
        if inputkey == ord('q'):
            tts("goodbye")
            break
        if inputkey == ord('e'):
            tts("Searching for face")
            names = facerec(image)
            for name in names:
                print(name)
                tts(name)
        if inputkey == ord('w'):
            tts("Generating caption")
            captain=caption(image)
            for p in captain:
                text = " ".join(p[1:-1])
                print(text)
                tts(text)
        if inputkey == ord('r'):
            for images in glob.glob("./sample_imgs/*.jpg"):
                print(images)
                img = cv2.imread(images)
                captain=caption(img)
                for p in captain:
                    text = " ".join(p[1:-1])
                    print(text)
                    tts(text)
                    break

        #rawCapture.truncate(0)

    # On quit the capture is released and the CV2 Window is released
    cap.release()
    cv2.destroyAllWindows()
