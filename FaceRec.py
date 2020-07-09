import cv2
import time
import subprocess
import glob
import face_recognition
import argparse
import pickle
from CaptionGenerator import CaptionGenerator
from STT import tts,stt_min

def video_features(caption_generator,data):
    while True:
        tts("Choose a mode")
        operation = stt_min(3)
        if operation == "exit" or operation =="quit":
            tts("Exiting Video")
            break
        elif operation ==("face"):
            tts("Searching for face")
            for images in glob.glob("./face_imgs/*"):
                print(images)
                img = cv2.imread(images)
                names = facerec(img,data)
                for name in names:
                    tts(name)
            break
        elif operation == "caption":
            tts("Generating caption")
            for images in glob.glob("./caption_imgs/*.jpg"):
                print(images)
                img = cv2.imread(images)
                captions=caption(img,caption_generator)
                for p in captions:
                    text = " ".join(p[1:-1])
                    tts(text)
            break
        else:
            tts("retry")

    

def facerec(image,data):
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


def caption(frame,caption_generator):
    # Call the caption generator class and seeprates the sentence from the details
    captions = caption_generator.generate(frame)
    cap=[]
    for i in captions:
        cap.append(i["sentence"])
    return cap
