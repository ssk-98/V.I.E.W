import cv2
import time
import subprocess
import face_recognition
import pickle
import sys
import os

from CaptionGenerator import CaptionGenerator


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
    return cap[0]

def main():
    face_data = pickle.loads(open('./encoding.pickle', "rb").read())
    caption_generator=CaptionGenerator(
        rnn_model_place=sys.argv[1],
        cnn_model_place=sys.argv[2],
        dictionary_place=sys.argv[3],
        )
    print("Caption generator Model loaded")
    while True:
        f = open("./Function","r")
        try:
            command = f.readlines()[0]
        except:
            command = "a"
        f.close()
        if command == "q":
            break
        elif command == "r":
            img = cv2.imread("./frame.jpg")
            names = facerec(img,face_data)
            f=open("./Output.txt","w+")
            f.write(",".join(names))
            f.close()
            f=open("./Function","w+")
            f.write("a")
            f.close()
        elif command == "c":
            img = cv2.imread("./frame.jpg")
            captions=caption(img,caption_generator)
            f=open("./Output.txt","w+")
            f.write(" ".join(captions[1:-1]))
            f.close()
            f=open("./Function","w+")
            f.write("a")
            f.close()
        time.sleep(2)
            

if __name__ == "__main__":
    main()
