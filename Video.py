import cv2
import sys

def video_cap(VideoEn):
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        if VideoEn:
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
        f=open("./Function","r")
        command = f.readlines()[0]
        f.close()
        if command == "f":
            cv2.imwrite("./frame.jpg", frame)
            f=open("./Function","w")
            f.write("a")
            f.close()
        if command == "q":
            break
    cap.release()
    if VideoEn:
        cv2.destroyAllWindows()

    
if __name__ == "__main__" :
    if len(sys.argv) > 1:
        VideoEn = False
    else:
        VideoEn = True
    video_cap(VideoEn)
